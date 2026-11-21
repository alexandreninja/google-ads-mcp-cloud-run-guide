# Portuguese-language videos for further context

This list offers visual context for people who are getting started. These videos are **conceptual supplements**: they do not reproduce every command in this guide, deploy Google Ads MCP, or replace the instructions for the pinned upstream version. Screens, menu names, prices, and requirements change; use current official documentation for operational steps.

The titles, language, topic, channel, and publication date below were checked on **November 21, 2026**. The videos were not watched in full; metadata checks do not verify that every demonstrated step still works. When I could not find a Portuguese video that I could recommend with confidence, I note the gap and point to official documentation. Additional searches lead to results that have not been reviewed; they should not be treated as video recommendations.

## Project, billing, and Cloud Shell

### Supporting video: billing (metadata checked)

[Administração de faturamento no Google Cloud](https://www.youtube.com/watch?v=QKitTPX9yrU) · Google Cloud LATAM · published **July 29, 2024** · in Portuguese.

The description covers billing administration concepts and roles, alerts, and cost optimization options. The Google Cloud LATAM channel is verified on YouTube. The video is **not** a walkthrough for creating a project, linking it to a billing account, or opening Cloud Shell.

For those steps, use the current official guides:

- [Create Google Cloud projects](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=en)
- [Enable, disable, or change billing for a project](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=en)
- [Launch Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell?hl=en)

I could not find a Portuguese video that provides current instructions for creating a project, linking billing, and opening Cloud Shell together.

## Cloud Run, Cloud Build, and Artifact Registry

### Supporting video: CI/CD overview (metadata checked)

[Implantação de CI/CD no Google Cloud](https://www.youtube.com/watch?v=K4jI5ZgS95E) · Google Cloud LATAM · published **July 25, 2024** · in Portuguese.

The description introduces CI/CD, pipelines from source code, Cloud Build, and a demonstration in the Google Cloud Console; it also points to Cloud Run. The channel is verified on YouTube. This is an introduction to the flow, **not** a recording of the commands in this repository or a tutorial specific to Artifact Registry or Google Ads MCP.

To follow this guide and check current permissions, commands, and formats, see:

- [Build and push images with Cloud Build](https://docs.cloud.google.com/build/docs/deploying-builds/deploy-cloud-run?hl=en)
- [Store artifacts in Artifact Registry](https://docs.cloud.google.com/build/docs/building/store-artifacts-in-artifact-registry?hl=en)
- [Artifact Registry Docker quickstart](https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images?hl=en)
- [Cloud Run documentation](https://docs.cloud.google.com/run/docs?hl=en)

### Historical hands-on: Docker and Cloud Run

[Docker and Google Cloud Run hands-on](https://www.youtube.com/watch?v=QcXw0VEL_U8) · The Cloud Bootcamp · published in 2022 · in Portuguese. The listing describes containers and deployment to Cloud Run. It is useful for visual context, but its menus and commands may be outdated. It is not a tutorial for Google Ads MCP or its current OAuth flow.

Official written exercises, with Portuguese localization, are also available: [Cloud Shell](https://codelabs.developers.google.com/codelabs/cloud-shell?hl=pt-br) and [Cloud Run](https://codelabs.developers.google.com/next26/ultimate-cloud-run-guide?hl=pt-br). These are codelabs, not videos.

## Google Auth Platform, OAuth, and Secret Manager

I could not find a Portuguese video that covers the current Google Auth Platform interface, creating a web OAuth client, the callback specific to the MCP server, and Cloud Run access to secrets. OAuth tutorials for other products (for example, YouTube Data API, n8n, or Apps Script) use different flows, scopes, and callbacks and should not be copied for this deployment.

Use these current official sources and check the callback required by your chosen upstream version:

- [Using OAuth 2.0 for web server applications](https://developers.google.com/identity/protocols/oauth2/web-server) — explains the web flow and that the redirect URI must exactly match an authorized URI.
- [Set up authentication for Google and Google Cloud MCP servers](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers) — shows where **Google Auth Platform → Clients** is in the Console and how to register a redirect URI. This tutorial configures the Google Cloud MCP servers described on that page; use it only as a navigation reference, and do not copy its client, scopes, or callback for Google Ads MCP.
- [Configure the OAuth consent screen and choose scopes](https://developers.google.com/workspace/guides/configure-oauth-consent) — consent and scope concepts; does not document Google Ads MCP-specific setup.
- [Create and access a secret using Secret Manager](https://docs.cloud.google.com/secret-manager/docs/create-secret-quickstart)
- [Configure secrets for Cloud Run services](https://docs.cloud.google.com/run/docs/configuring/services/secrets) — current secret configuration and creation of Cloud Run revisions.

## Google Ads API and project access

I could not find a Portuguese video explaining the current Google Ads API access process. Older videos about requesting or using a developer token do not represent the current process: these tokens were retired on **September 9, 2026**. Access is now associated with the Google Cloud project that issued the OAuth credentials; test access and access to production accounts are separate levels.

Read the current official page before requesting access or interpreting an error:

- [Developer tokens and changes to Google Ads API access](https://developers.google.com/google-ads/api/docs/api-policy/developer-token) — explains the migration, project-based Cloud access, and why the API Center should not be used for new requests.
- [Official Google Ads MCP repository](https://github.com/googleads/google-ads-mcp) — check the README for the tag/commit pinned by the guide; configuration and tools vary by version.

## Additional searches not reviewed

The links below are **search results pages, not validated videos**. Use them only if you want to look for other materials; check the author, date, language, and whether the interface still exists before following any steps.

- [Search for videos about projects, billing, and Cloud Shell](https://www.youtube.com/results?search_query=Google+Cloud+criar+projeto+faturamento+Cloud+Shell+portugu%C3%AAs)
- [Search for videos about Cloud Run, Cloud Build, and Artifact Registry](https://www.youtube.com/results?search_query=Google+Cloud+Run+Cloud+Build+Artifact+Registry+portugu%C3%AAs)
- [Search for videos about OAuth and Secret Manager](https://www.youtube.com/results?search_query=Google+Auth+Platform+OAuth+Secret+Manager+Cloud+Run+portugu%C3%AAs)
- [Search for videos about current Google Ads API access](https://www.youtube.com/results?search_query=Google+Ads+API+acesso+projeto+Google+Cloud+2026+portugu%C3%AAs)

---

**Source check:** November 21, 2026. Google documentation pages are living content without a fixed version; this date records when the links and guidance were checked. Video details come from YouTube metadata/listings; the full video content was not verified.
