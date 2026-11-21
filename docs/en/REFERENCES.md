# References

This list prioritizes documentation from the maintainers of the tools and services used in this guide. The links below were opened or checked on **November 21, 2026**. Google Cloud and Google for Developers pages are living documentation and do not have one version that applies to every command; check the version indicated on each page.

## Google Ads MCP server and version

| Source | Version or date checked | Use in this guide |
| --- | --- | --- |
| [Official `googleads/google-ads-mcp` repository](https://github.com/googleads/google-ads-mcp) | Checked on 2026-11-21. Pin a tag or commit in the deployment procedure; do not use `main` as a reproducible reference. | Server code and README used for the build. Variables, OAuth callbacks, and tools depend on the version. |
| [Official `v0.0.6` release](https://github.com/googleads/google-ads-mcp/releases/tag/v0.0.6) | Published on 2026-11-02, commit `7452a9d`; it was the latest release on 2026-11-21. | Reference for the version available when this page was reviewed. The guide should state which version it chose. |
| [Audited upstream commit](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd) | 44ca7770519362c8f334875477e1ceb499f8d2dd; reviewed on 2026-11-21. Declares package version 0.0.6, but is not the v0.0.6 release-tag commit. | Exact baseline recorded in config/upstream.json and used by this guide. |
| [Upstream server license](https://github.com/googleads/google-ads-mcp/blob/7452a9d/LICENSE) | Apache License 2.0 at commit `7452a9d`; checked on 2026-11-21. | License for the official server code; it does not automatically license this repository or third-party content. |

## Google Ads API and authorization

| Source | Status when checked | Use in this guide |
| --- | --- | --- |
| [Google Ads API](https://developers.google.com/google-ads/api) | Living documentation; checked on 2026-11-21. | API overview and documentation. |
| [Changes to developer tokens and access management](https://developers.google.com/google-ads/api/docs/api-policy/developer-token) | Checked on 2026-11-21. The page says developer tokens were retired on 2026-09-09; new access levels are managed in the Google Cloud project. | Authoritative source for distinguishing API enablement, test access, and authorization to use production accounts. Do not use older token tutorials as the current procedure. |
| [Using OAuth 2.0 for web server applications](https://developers.google.com/identity/protocols/oauth2/web-server) | Living documentation; checked on 2026-11-21. | Web OAuth flow and exact-match redirect URI requirement. The MCP callback must come from the upstream version in use. |
| [Configure the OAuth consent screen and choose scopes](https://developers.google.com/workspace/guides/configure-oauth-consent) | Living documentation; checked on 2026-11-21. | Consent and scope concepts. Does not replace server-specific instructions for Google Ads MCP. |
| [Set up authentication for Google and Google Cloud MCP servers](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers) | Living documentation; checked on 2026-11-21. | A reference for locating Google Auth Platform and understanding URI registration; it describes Google Cloud MCP servers, not the Google Ads MCP OAuth configuration. |

## Google Cloud: project, build, and runtime

| Source | Version/language checked | Use in this guide |
| --- | --- | --- |
| [Create projects](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects) | Official English page; checked on 2026-11-21. | Project creation and permissions. |
| [Enable, disable, or change billing for a project](https://docs.cloud.google.com/billing/docs/how-to/modify-project) | Official English page; checked on 2026-11-21. | Link a project to an active Cloud Billing account. |
| [Launch Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell) | Official English page; checked on 2026-11-21. | Open Cloud Shell in the Google Cloud Console. |
| [Cloud Run documentation](https://docs.cloud.google.com/run/docs) | Living English documentation; checked on 2026-11-21. | Service configuration and operations. |
| [Deploy to Cloud Run using Cloud Build](https://docs.cloud.google.com/build/docs/deploying-builds/deploy-cloud-run) | English page; the version opened showed its latest update as 2026-11-11 UTC. | Official build and deployment example; this guide's commands may use another build path. |
| [Store artifacts in Artifact Registry](https://docs.cloud.google.com/build/docs/building/store-artifacts-in-artifact-registry) | Official English page; checked on 2026-11-21. | Publish artifacts and permissions between Cloud Build and Artifact Registry. |
| [Artifact Registry Docker quickstart](https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images) | Official English page; checked on 2026-11-21. | Create a repository and store a container image. |
| [Create and access a secret with Secret Manager](https://docs.cloud.google.com/secret-manager/docs/create-secret-quickstart) | Official English page; checked on 2026-11-21. | Create secrets and add versions. |
| [Configure secrets for Cloud Run services](https://docs.cloud.google.com/run/docs/configuring/services/secrets) | Official English page; checked on 2026-11-21. | Attach secrets to service revisions; check access and version strategy. |
| [Cloud Run logs](https://docs.cloud.google.com/run/docs/logging) | Official English page; checked on 2026-11-21. | View container logs and find the first startup or request failure. |

## MCP protocol

- [Model Context Protocol specification, revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28): revision published on **July 28, 2026**. Clients and servers may also speak earlier revisions; check support in the upstream version and client used by this tutorial.
- [Google Ads MCP release history](https://github.com/googleads/google-ads-mcp/releases): use the pinned release to identify the transport, endpoint, variables, and tool configuration actually provided by the server.

## ChatGPT client (when used for validation)

- [Connect custom MCP servers in ChatGPT](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt): official Help Center; checked on 2026-11-21 and shown as updated 24 days earlier. Describes the current Plugins → add custom MCP server interface and plan/workspace availability and policies. This interface flow is ChatGPT-specific and does not replace the Google Ads MCP README.

## Licenses and attribution

The official server code is licensed under Apache 2.0. The license for this repository's original content is listed in [LICENSE](../../LICENSE). Google Developers documentation consulted on this page indicates CC BY 4.0 for content, unless otherwise stated, and Apache 2.0 for code samples; check the source page footer before copying or adapting excerpts. Links do not transfer or change the licenses of upstream code, documentation, videos, brands, or other external materials.

For corrections or new sources, see [Contributing](../../CONTRIBUTING.md). Portuguese videos reviewed and their limitations are listed in [Videos in Portuguese](guides/VIDEOS-PT-BR.md).

## Client and implementation references

- [VS Code MCP configuration](https://code.visualstudio.com/docs/agent-customization/mcp-servers): client-specific servers/type/url configuration.
- [Codex MCP documentation](https://developers.openai.com/codex/mcp): HTTP registration and OAuth. The installed CLI help was also inspected during this review.
- [FastMCP Google provider](https://gofastmcp.com/docs/integrations/google): default /auth/callback and Web OAuth flow.
- [Create Firestore databases](https://docs.cloud.google.com/sdk/gcloud/reference/firestore/databases/create): Standard/Native database creation.
- [User-specified Cloud Build accounts](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts): separate operator, build identity, and logging requirements.
- [Submit a build](https://docs.cloud.google.com/build/docs/running-builds/submit-build-via-cli-api): source staging in Cloud Storage.
- [Cloud Run IAM roles](https://docs.cloud.google.com/run/docs/reference/iam/roles): deploy and invocation permissions.
- [Cloud Shell codelab](https://codelabs.developers.google.com/codelabs/cloud-shell?hl=pt-br) and [Cloud Run codelab](https://codelabs.developers.google.com/next26/ultimate-cloud-run-guide?hl=pt-br): supplementary written exercises available in Portuguese, not videos.
