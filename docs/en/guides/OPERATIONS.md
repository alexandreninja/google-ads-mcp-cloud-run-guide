# 06 · Operations and maintenance

This service combines Cloud Run, OAuth, the Google Ads API, and state storage. Review these layers whenever code or configuration changes.

## Routine checks

- [ ] Record the upstream commit, resolved dependency versions, and deployed image digest.
- [ ] Review upstream changes before rebuilding; do not update the pin automatically to main or a moving tag.
- [ ] Confirm that tools_config.yaml allows only customers, search, and metadata; inspect tools/list after every new revision.
- [ ] Track Cloud Run status, latency, restarts, HTTP errors, and concurrency saturation.
- [ ] Track authorization errors, the project's Google Ads API access level, and operation usage.
- [ ] Check all three secrets: the OAuth Client Secret, JWT key, and OAuth storage key. Rotating JWT invalidates previous signatures; changing the storage key affects access to encrypted state.
- [ ] Limit the runtime account to the Firestore access and secret access it needs.
- [ ] Review costs and retention for Cloud Run, Firestore, Artifact Registry, Cloud Build, Secret Manager, and Cloud Logging.
- [ ] Keep the previous image digest and compatible secret versions available for rollback.

## State and availability

Firestore preserves OAuth state across instances and restarts. It does not preserve in-memory MCP sessions, open SSE connections, or subscriptions/listen streams. After an instance restarts, the client may need to reconnect and initialize a new session.

This evaluation setup allows at most one instance. It limits capacity and does not provide high availability. A minimum of zero instances allows idle instances to stop and can increase startup latency. A minimum of one keeps a warm instance as a target, at additional cost, but does not prevent restarts. Cloud Run session affinity is best effort; do not use it as a persistence mechanism.

The upstream keeps stateful HTTP for compatibility with newer and older Streamable HTTP clients. Do not enable stateless_http without testing the intended clients: it removes the GET/SSE flow used by some of them. OAuth storage and MCP transport sessions are different kinds of state. The guide's 300-second request timeout also requires streaming clients to reconnect after five minutes.

## Inspect the service

~~~bash
# Inspect the active revision and deployed configuration.
gcloud run services describe "$SERVICE" --region="$REGION"

# List revisions to investigate an issue and plan a rollback.
gcloud run revisions list \
  --service="$SERVICE" \
  --region="$REGION"

# Look up recent builds.
gcloud builds list --limit=10
~~~

Use Cloud Logging with a service-name filter and the time window you need. Audit events include tool names, account identifiers, and execution status. Although some sensitive arguments are redacted, logs remain operational data that needs protection. Do not copy query responses or logs into public issues.

## Update and roll back

1. Read the upstream changes and release notes. Check transport, tools, OAuth, and storage for the new commit.
2. Build from the pinned commit and record build provenance and the published image digest.
3. Deploy a new revision while retaining the previous image digest.
4. Sign in with a test MCP client, inspect tools/list, and run a non-destructive query against an authorized account.
5. Check logs, errors, and reconnection after restarts before directing users to the new revision.
6. If the change regresses, route traffic back to the previous revision with compatible Secret Manager version numbers.

This guide injects an independent storage key. Rotating the Client Secret or JWT key therefore does not automatically change Firestore's application encryption key. Handle each secret separately: a Client Secret update requires a revision compatible with the OAuth client; JWT rotation may require sign-in again; storage-key rotation requires a plan to migrate state or obtain new authorizations. The backend does not automatically migrate data between keys.

## Close the lab

First confirm the project, service, and region. To remove only the Cloud Run service, run the command below and review the CLI confirmation:

~~~bash
gcloud run services delete "$SERVICE" --region="$REGION" --project="$PROJECT_ID"
~~~

Removing Cloud Run does not remove its supporting resources. In a project dedicated to this lab, inspect each resource in the Console and remove it only after confirming it has no other use:

| Resource | Where to inspect it | What remains |
| --- | --- | --- |
| Source bucket | Cloud Storage → bucket created in step 4 | Source archives may remain billable until deleted |
| Image repository | Artifact Registry → mcp-servers | Image versions remain until removed under your retention policy |
| Three secrets | Secret Manager | Versions remain; keep only what an authorized rollback still needs |
| OAuth database | Firestore → (default) | Deleting state loses saved authorizations; verify that no other application uses the database |
| Service accounts and IAM | IAM & Admin | Review the two accounts and their bindings after resource cleanup |
| OAuth application | Google Auth Platform | Review credentials and revoke access that is no longer needed |
| Logs | Cloud Logging | Retention can continue after the service is removed |

Do not delete a shared project or database to close this lab. Review the billing report afterwards; removing a service does not erase earlier usage charges.

See [Costs](COSTS.md) and [Security](../SECURITY.md). Sources: [Cloud Run session affinity](https://docs.cloud.google.com/run/docs/configuring/session-affinity), [minimum instances](https://docs.cloud.google.com/run/docs/configuring/min-instances), and the [pinned upstream README](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/README.md#http-interoperability-notes).

To migrate without replacing existing settings, preserve key versions, and test rollback, see [OAuth persistence](OAUTH-PERSISTENCE.md). Traffic rollback is not OAuth state restoration.
