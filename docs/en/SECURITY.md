# Security

This guide describes a low-volume lab, not a production configuration or a guarantee of authorized access. Review each layer before connecting a Google Ads account.

## Cloud Run ingress and OAuth

The guide allows unauthenticated invocation at the Cloud Run IAM layer so MCP clients can reach discovery and start OAuth. The endpoint can receive anonymous traffic and incur costs. This is separate from application-level Google sign-in: protected MCP tools still require a valid OAuth token.

The FastMCP Google provider keeps the server credentials and forwards the OAuth return flow. This baseline's Google callback is the service's HTTPS base URL followed by /auth/callback. The MCP client's dynamic/local callback is handled by the proxy; do not register it as another Google Web application callback. Keep the server Client Secret out of MCP client configuration.

If organizational policy forbids public exposure, stop and ask the responsible team for a compatible architecture. A Cloud Run endpoint protected by IAM also needs a Google invoker identity from the client; that is separate from Google Ads OAuth.

## Who can query data

Three independent checks apply:

1. **Cloud project:** the project that owns the OAuth Client ID must have the Google Ads API enabled and the appropriate access level. Developer tokens were retired on September 9, 2026; do not follow old token-application instructions. Enabling the API or deploying the server does not approve production access.
2. **Google Ads user:** the person completing OAuth must have access to the chosen account. Use a test account or the least-privileged user role that supports the task, such as read-only access where available.
3. **Exposed tools:** the guide's tools_config.yaml keeps customers, search, and metadata enabled and disables labels and assets, which include upstream mutations. Inspect tools/list after building and after every update.

The Google Ads API uses the adwords OAuth scope for both reading and writing; there is no separate read-only OAuth scope. Disabling mutation tools restricts this image's surface, not the OAuth scope, the user's account role, or future container changes. See the [Google Ads access model](https://developers.google.com/google-ads/api/docs/oauth/access-model) and [API access policy](https://developers.google.com/google-ads/api/docs/api-policy/developer-token).

## Secrets, identity, and state

- Keep the OAuth Client Secret, JWT signing key, and OAuth storage key in Secret Manager. The Client ID is a public identifier. Do not put secrets in source code, shell history, environment files, or client configuration.
- Separate build and runtime service accounts. Scope runtime secret access to the three required secrets and grant the Firestore access required for OAuth state.
- This image encrypts persisted OAuth records with its independent storage key. Keep JWT signatures consistent across instances and plan rotation: changing keys can invalidate stored authorizations or sessions. Google Cloud encryption at rest does not replace application-key protection.
- Pin numeric secret versions for values injected as environment variables. Cloud Run resolves them at instance startup; a new secret version does not automatically refresh a running instance.
- Firestore preserves OAuth state, not in-memory MCP sessions, open SSE streams, or subscriptions. Scale-to-zero and restarts may require client reconnection.

## Logs and account data

Upstream produces structured tool-call audit events and redacts several sensitive fields. Events can still include tool names, Ads account identifiers, times, outcomes, and duration. Restrict log readers, configure retention, and avoid attaching live query responses or account-data screenshots to public issues.

Query results can contain performance and business information. Connect only approved clients, confirm the account and period before each query, and follow organizational rules for sharing results.

## Repository and updates

Before publishing source or rebuilding an image:

- Inspect current files and history for credentials, OAuth files, real account data, internal URLs, sensitive logs, and screenshots.
- Confirm that local credential files are excluded from both Git and the build context.
- Review the pinned upstream commit, Dockerfile, and tool configuration.
- Revisit OAuth, callback, permissions, dependencies, tools, and storage before changing the pin.
- Record the source commit, image digest, and secret versions for each revision.

This build is derived from official code, but it is not an official Google distribution. Preserve upstream license notices when redistributing source or images. See [OAuth and secrets](guides/OAUTH-AND-SECRETS.md), [operations](guides/OPERATIONS.md), and [official references](REFERENCES.md).

[Português](../../SECURITY.md)
