# OAuth persistence: migrate from memory to Firestore

[Português](../../guides/OAUTH-PERSISTENCE.md) · [Index](../README.md)

## Why sign-in is lost

Cloud Run retains service configuration, not process memory. With `GOOGLE_ADS_MCP_STORAGE_TYPE=memory`, replacing an instance may erase state needed to use an authorization. Google authorization and MCP HTTP sessions have distinct lifecycles. Firestore preserves OAuth state; it does not preserve HTTP streams or prevent token revocation.

## 1. Inventory and prerequisites

This procedure migrates an existing service; for a fresh deployment, follow [DEPLOY](../getting-started/DEPLOY.md). Use an authorized environment, review [costs](COSTS.md), and prepare a rollback. Run commands individually and stop on errors. Define PROJECT_ID, REGION, SERVICE, RUNTIME_SA_EMAIL (runtime, not build identity), IMAGE (new prepared image), STORAGE_SECRET (dedicated secret name), and PREVIOUS_REVISION (previous ready revision) with your own values. Do not publish IDs, tokens, raw logs, or internal names.

~~~bash
gcloud run services describe "$SERVICE" --project="$PROJECT_ID" --region="$REGION" --format='value(status.latestReadyRevisionName,spec.template.spec.serviceAccountName,spec.template.spec.containers[0].image)'
gcloud firestore databases list --project="$PROJECT_ID"
~~~

Inspect the storage configuration in Console without exposing secret values. Enable the Firestore API only with authorization if disabled.

## 2. Database and IAM

Only if no suitable database exists, create the database below. Choose the location before creation. The first eligible database may qualify for free usage; check freeTier in the response. Do not enable backups/PITR/managed TTL without reviewing costs.

~~~bash
gcloud firestore databases create --project="$PROJECT_ID" --database='(default)' --location="$REGION" --type=firestore-native --delete-protection
~~~

Grant data access conditioned on the database:

~~~bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$RUNTIME_SA_EMAIL" --role=roles/datastore.user \
  --condition="expression=resource.name==\"projects/$PROJECT_ID/databases/(default)\",title=McpFirestoreAccess,description=OAuth persistent storage"
~~~

This condition does not isolate collections within one database. Do not grant broad administrative roles to work around errors. Verify effective access during authentication.

## 3. Prepare the image and key

Package 0.0.6 provides the Firestore extra. Use the guide helper on a clean pinned checkout or review the existing deployment Dockerfile; change only the install line to `RUN uv pip install --system ".[firestore]"`. Preserve the read-only profile, other adaptations, and previous image. Build with a new tag as described in [DEPLOY](../getting-started/DEPLOY.md). Verify success and record the digest. Do not send credentials in the build context.

If no dedicated key exists, generate it directly into Secret Manager (do not rerun if the secret already exists; verify its version and preserve the existing key).

~~~bash
python3 -c 'import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(),end="")' | \
  gcloud secrets create "$STORAGE_SECRET" --project="$PROJECT_ID" --replication-policy=automatic --data-file=-
gcloud secrets add-iam-policy-binding "$STORAGE_SECRET" --project="$PROJECT_ID" \
  --member="serviceAccount:$RUNTIME_SA_EMAIL" --role=roles/secretmanager.secretAccessor
~~~

The Fernet key protects OAuth content at the application layer; preserve it across revisions, separately from the JWT key. Use the correct secret version in deployment. Rotating or losing the key may invalidate persisted state.

## 4. Migrate without replacing other configuration

Verify IMAGE and STORAGE_SECRET; this example assumes enabled version 1. Preserve base URL, OAuth Client ID, Client Secret, JWT key, runtime identity, tool profile, and execution limits.

~~~bash
gcloud run services update "$SERVICE" --project="$PROJECT_ID" --region="$REGION" \
  --image="$IMAGE" \
  --update-env-vars="GOOGLE_ADS_MCP_STORAGE_TYPE=firestore,GOOGLE_ADS_MCP_STORAGE_FIRESTORE_PROJECT=$PROJECT_ID,GOOGLE_ADS_MCP_STORAGE_FIRESTORE_DATABASE=(default)" \
  --update-secrets="GOOGLE_ADS_MCP_STORAGE_ENCRYPTION_KEY=$STORAGE_SECRET:1"
~~~

Check that the revision is ready and receives traffic. Reconnect the client once: old in-memory state is not migrated automatically.

## 5. Test persistence

List authorized accounts with customers_list_accessible_customers. In Firestore Studio, verify the presence of mcp-jti-mappings, mcp-refresh-tokens, and mcp-upstream-tokens collections. The __encrypted_data__ format was observed in a JTI mapping record; do not open or copy secret contents. Record expiry does not guarantee Google authorization validity.

During a maintenance window, create another revision using the same image and keys. The variable below is only a test marker.

~~~bash
gcloud run services update "$SERVICE" --project="$PROJECT_ID" --region="$REGION" \
  --update-env-vars="OAUTH_PERSISTENCE_TEST=$(date -u +%Y%m%dT%H%M%SZ)"
~~~

Confirm that the new revision receives 100% of traffic. Repeat the query without manually reconnecting OAuth. The client may need to reestablish MCP transport automatically. Record success or failure and test renewal after access token expiry separately. Check whether the OAuth app is in testing mode, which may limit refresh token lifetime.

## 6. Rollback

If needed, route traffic to the previous revision after verifying that it remains available and safe.

~~~bash
gcloud run services update-traffic "$SERVICE" --project="$PROJECT_ID" --region="$REGION" \
  --to-revisions="$PREVIOUS_REVISION=100"
~~~

If the previous revision used memory, new authorization may be necessary. Do not delete the database or keys as part of rollback.

## Evidence and limits

On 2026-11-24, an existing deployment of package 0.0.6, upstream commit 7452a9d49e3d350403f2610cd7125c60f6d05264, was migrated from memory to Firestore; build and deployment succeeded, three read tools were preserved, records were observed in the database, and two accounts were returned before and after a new revision with no reported manual reconnection. This demonstrates access continuity across revisions in that experiment, not renewal after expiry, persistence of every record type, compatibility with all clients, or zero cost. The original guide pins a different commit; we do not claim that its full procedure was executed.

Sources: [tested storage implementation](https://github.com/googleads/google-ads-mcp/blob/7452a9d49e3d350403f2610cd7125c60f6d05264/ads_mcp/auth_storage.py), [Firestore pricing](https://cloud.google.com/firestore/pricing), [Cloud Run](https://cloud.google.com/run/docs).

[Validation](VALIDATION.md) · [Operations](OPERATIONS.md)
