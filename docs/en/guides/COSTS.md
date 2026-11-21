# Environment costs

There is no guaranteed zero-cost configuration. The amount depends on region, request duration and volume, container configuration, persisted data, traffic, log retention, and current prices. Review current pricing before deployment.

| Service | What can incur charges |
| --- | --- |
| Cloud Run | CPU, memory, requests, minimum instances, and execution time. Long HTTP requests and streams can keep requests active. |
| Cloud Build | Builds and image updates. |
| Artifact Registry | Storage for image versions. Retain enough for rollback and remove obsolete versions under your policy. |
| Firestore | Reads, writes, storage, backups, and OAuth-state cleanup. Usage depends on users and token renewals. |
| Secret Manager | Stored secret versions and access, including reads when instances start. |
| Cloud Logging | Ingestion, queries, exports, and retention beyond applicable allowances. |
| Network | Outbound traffic, including query responses and integrations. |

## Reduce surprises

1. Start with a dedicated evaluation project, enabling billing and APIs only as required.
2. A minimum of zero instances avoids keeping a minimum instance warm, but does not eliminate charges for requests, builds, storage, databases, or logs.
3. This guide caps the pilot at one instance. That limits capacity, not the cost of the other services.
4. Configure budget alerts and monitor billing. Alerts notify you; they do not stop services or impose a spending cap.
5. Review retention for images, Firestore data, logs, and secret versions. Removing OAuth state may require users to sign in again.
6. Choose concurrency compatible with clients that keep HTTP streams open; an excessively low value can queue or reject requests.
7. Include support, updates, access reviews, and maintenance in your cost estimate.

The Google Ads API's access level and operation quotas control access and capacity separately from Cloud infrastructure billing. Developer tokens were retired on September 9, 2026. New projects must check the access level of the project that owns the OAuth credentials. This does not promise unlimited access or free infrastructure.

Prices and allowances can change. See [Cloud Run pricing](https://cloud.google.com/run/pricing), [Firestore pricing](https://cloud.google.com/firestore/pricing), [Cloud Build pricing](https://cloud.google.com/build/pricing), [Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing), [Secret Manager pricing](https://cloud.google.com/secret-manager/pricing), [Cloud Billing](https://cloud.google.com/billing/docs), and the [Google Ads API access policy](https://developers.google.com/google-ads/api/docs/api-policy/developer-token).

[Operations and cleanup](OPERATIONS.md)
