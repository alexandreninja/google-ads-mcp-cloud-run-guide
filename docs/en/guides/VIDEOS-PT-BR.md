# Portuguese-language videos for further context

Choose the topic where you need visual help, then return to your checkpoint. The three videos below introduce cloud concepts; the Google Ads MCP-specific steps are in the [deployment guide](../getting-started/DEPLOY.md).

> [!NOTE]
> Titles, channels, language, topics, and dates were checked on **November 21, 2026** using public metadata. The videos were not watched in full. For current commands, permissions, and interfaces, follow this guide and official sources.

## Watch

| Topic | Video in Portuguese | What to look for |
| --- | --- | --- |
| Billing | [Administração de faturamento no Google Cloud](https://www.youtube.com/watch?v=QKitTPX9yrU) — Google Cloud LATAM, July 29, 2024 | Administration roles, alerts, and costs. For creating and linking a project, use the exercises below. |
| Code to cloud | [Implantação de CI/CD no Google Cloud](https://www.youtube.com/watch?v=K4jI5ZgS95E) — Google Cloud LATAM, July 25, 2024 | An overview of pipelines, Cloud Build, and a Console demonstration. |
| Containers and deployment | [Hands-on: Deploy de aplicação com Docker no Google Cloud Run](https://www.youtube.com/watch?v=QcXw0VEL_U8) — The Cloud Bootcamp - Português, September 13, 2022 | A historical demonstration to visualize images and services. Its 2022 interface and commands may be outdated. |

## Follow along

These **official exercises localized into Portuguese are interactive text**, not videos:

- [Cloud Shell and gcloud](https://codelabs.developers.google.com/codelabs/cloud-shell?hl=pt-br): projects, billing, opening the terminal, and checking the account.
- [Cloud Run, from basics to a demonstration](https://codelabs.developers.google.com/next26/ultimate-cloud-run-guide?hl=pt-br): images, deployment, Artifact Registry, and Secret Manager. It is a separate example; when you return, use this repository's MCP configuration.

## OAuth and API access: use current documentation

No Portuguese video was found that covers this server's complete current OAuth flow or the new Google Ads API access process. For those steps, use:

| I need to understand… | Source and next step |
| --- | --- |
| Web client and sign-in callback | [OAuth 2.0 for web servers](https://developers.google.com/identity/protocols/oauth2/web-server) → [OAuth in this guide](OAUTH-AND-SECRETS.md) |
| Credentials outside source code | [Create a secret](https://docs.cloud.google.com/secret-manager/docs/create-secret-quickstart) · [Use secrets in Cloud Run](https://docs.cloud.google.com/run/docs/configuring/services/secrets) |
| Test or production API access | [Current access levels](https://developers.google.com/google-ads/api/docs/api-policy/developer-token) → [Prerequisites](../getting-started/PREREQUISITES.md) |

> [!IMPORTANT]
> Older developer-token tutorials follow the previous model, retired on September 9, 2026. OAuth tutorials for other products may also use different callbacks and scopes. Check the [official server](https://github.com/googleads/google-ads-mcp) requirements at the version pinned by this guide.

[← Index](../README.md) · [Glossary](../GLOSSARY.md)
