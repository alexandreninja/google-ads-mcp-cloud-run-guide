# 03 · OAuth and secrets: identify, authorize, and store

[Português](../../guides/OAUTH-AND-SECRETS.md) · [Index](../README.md)

Think of three objects: the Client ID identifies the application; the Client Secret is its confidential credential; consent authorizes a person to access their Google Ads accounts. The Cloud Run service account accesses Firestore and Secret Manager, but does not gain access to ads accounts just because it exists in Google Cloud.

This page is part of step 6 in the [deployment](../getting-started/DEPLOY.md). `PROJECT_ID` and `RUNTIME_SA_EMAIL` must already be set. Use **the same project for OAuth and runtime** in this lab: Google Ads API access level is linked to the project that issues the OAuth credentials.

## Before deployment: prepare the Google application

1. In the project Console, open **Google Auth Platform**. In earlier interfaces: **APIs & Services → OAuth consent screen**.
2. Under **Branding**, set a recognizable name, support email, and contact. Do not use an institutional brand without authorization.
3. Under **Audience**, select the permitted audience type. For a personal external lab, keep **Testing** and add your email as a test user. **Internal** applies only to Google Workspace organizations that allow this use.
4. Under **Data Access**, check the scopes required by upstream: `openid`, `https://www.googleapis.com/auth/userinfo.email`, `https://www.googleapis.com/auth/userinfo.profile`, and `https://www.googleapis.com/auth/adwords`. The last one is **not a read-only scope**. Verification may be required depending on audience, use, and organizational policy.
5. Under **Clients**, create a **Web application** client. Store the Client ID and Client Secret securely. The final URL does not exist yet: create the client and add the redirect URI after deployment. Do not choose a desktop app for this web flow.

~~~bash
# The Client ID is not the secret; replace it with your application's identifier.
export OAUTH_CLIENT_ID="SEU_CLIENT_ID.apps.googleusercontent.com"
~~~

**Checkpoint:** a web client in the correct project, a limited audience, and an identity with access to the chosen Google Ads account. Consent does not grant an API access level that the project does not already have.

## Create secrets from values without storing them in shell history

Run this in **Bash in Cloud Shell**, outside any screen recording or sharing session. Do not enable `set -x`. Do not paste credentials into chat, an issue, a versioned file, or directly as a command argument. `read -s` receives the credential without displaying it; only the variable reference is kept in history.

~~~bash
read -r -s -p "OAuth Client Secret: " TASK_OAUTH_SECRET
printf '\n'
printf '%s' "$TASK_OAUTH_SECRET" | gcloud secrets create \
  google-ads-mcp-oauth-client-secret --data-file=- \
  --replication-policy=automatic --project="$PROJECT_ID"
unset TASK_OAUTH_SECRET

# Generate random keys and send them to Secret Manager without displaying them.
python3 -c 'import secrets; print(secrets.token_urlsafe(48), end="")' | \
  gcloud secrets create google-ads-mcp-jwt-signing-key --data-file=- \
  --replication-policy=automatic --project="$PROJECT_ID"
python3 -c 'import secrets; print(secrets.token_urlsafe(48), end="")' | \
  gcloud secrets create google-ads-mcp-storage-key --data-file=- \
  --replication-policy=automatic --project="$PROJECT_ID"

for SECRET_NAME in google-ads-mcp-oauth-client-secret google-ads-mcp-jwt-signing-key google-ads-mcp-storage-key; do
  gcloud secrets add-iam-policy-binding "$SECRET_NAME" \
    --member="serviceAccount:$RUNTIME_SA_EMAIL" \
    --role=roles/secretmanager.secretAccessor --project="$PROJECT_ID"
  gcloud secrets versions list "$SECRET_NAME" \
    --filter='state:ENABLED' --format='value(name)' --project="$PROJECT_ID"
done
~~~

**Checkpoint before deployment:** all three names exist and have **version 1** enabled; the runtime identity can access them. The list shows metadata, not contents. If a secret already existed, pause and check its version; do not overwrite it automatically. The deployment pins `:1`; use another number only after reviewing the configuration.

The JWT key keeps signatures consistent across restarts. The storage key protects OAuth records in the backend. Changing these keys affects stored authorizations/sessions; see [rotation during operations](OPERATIONS.md).

**Now return to step 7 of the deployment guide.** The next section depends on the `SERVICE_URL` assigned by Cloud Run.

## After deployment: register the callback

~~~bash
# Display only the redirect URI; it contains no credentials.
printf '%s/auth/callback\n' "$SERVICE_URL"
~~~

Return to the web OAuth client and add the exact output under **Authorized redirect URIs**. Save it. The `/auth/callback` path is the default for the `GoogleProvider`/FastMCP used in this baseline; upstream does not override it in `ads_mcp/coordinator.py`.

| Address | Use |
| --- | --- |
| `SERVICE_URL` | HTTPS base URL, without `/mcp` |
| `SERVICE_URL/auth/callback` | Server callback registered in Google OAuth |
| `SERVICE_URL/mcp` | Endpoint provided to the MCP client |
| Local VS Code/Codex callback | Managed by the client and proxy; do not register random ports in this guide's Google OAuth client |

If the interface requires a JavaScript origin, use the HTTPS base URL without a path. An origin does not replace a redirect URI. Scheme, hostname, path, and trailing slash must match; differences cause `redirect_uri_mismatch`.

External apps in Testing may issue refresh tokens that expire after seven days when they request scopes beyond basic identity; this server requests `adwords`. A new authorization may be needed. Leaving Testing requires reviewing audience, verification, and governance, not just changing a selector. See the [official references](../REFERENCES.md) if the interface or policy changes.

**Final checkpoint:** the base URL configured in Cloud Run and the registered callback point to the same service. Complete [validation with a client](VALIDATION.md).

[← Deployment](../getting-started/DEPLOY.md) · [Validation →](VALIDATION.md)
