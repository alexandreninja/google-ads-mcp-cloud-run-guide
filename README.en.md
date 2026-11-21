# Google Ads MCP on Google Cloud Run

[Português](README.md) · [Documentation](docs/en/README.md) · [MIT license](LICENSE)

<p align="center">
  <img src="docs/assets/github-header.svg" alt="MCP client connected to the Google Ads MCP server on Cloud Run and to the Google Ads API" width="100%">
</p>

This guide grew out of a challenge at Sebrae Rio: modernizing marketing dashboards and exploring how AI could help interpret validated data. After considering managed integration and self-hosting, the experiment used the official [Google Ads MCP](https://github.com/googleads/google-ads-mcp) server on Cloud Run.

The repository can be used independently. To explain the motivation behind it, I published the LinkedIn article **Construir ou integrar? O que aprendi implementando um Google Ads MCP com Cloud Run e OAuth 2.0**. It covers the decisions, authentication errors, and lessons that led to this guide. That background helps explain the context; **here, the experience becomes a step-by-step path**, including for people coming from marketing who are beginning to work with cloud services and AI.

## 🧭 Start here

| I want to… | Where to go |
| --- | --- |
| Understand the choice and components | [Architecture](docs/en/ARCHITECTURE.md) · [STDIO or HTTP?](docs/en/concepts/MCP-TRANSPORTS.md) |
| Implement one step at a time | [01 · Prerequisites](docs/en/getting-started/PREREQUISITES.md) → [02 · Deployment](docs/en/getting-started/DEPLOY.md) |
| Learn with an AI assistant | [Tutoring prompt for your AI assistant](docs/en/guides/AI-TUTOR.md) |
| Resolve an error | [Troubleshooting by symptom](docs/en/guides/TROUBLESHOOTING.md) |
| Maintain or close the lab | [Costs](docs/en/guides/COSTS.md) · [Operations and cleanup](docs/en/guides/OPERATIONS.md) |

## 🔎 What you will build

An HTTPS service that lets an AI client query the Google Ads API through MCP. The guide uses **Cloud Shell**, a terminal available in your browser, and breaks deployment into steps with checkpoints:

1. Prepare the project, access, and separate build and runtime identities.
2. Set up Google sign-in with OAuth and store credentials in Secret Manager.
3. Build the image, deploy to Cloud Run, and connect an MCP client.
4. Check the available tools and validate a query against an authorized account.

This integration provides **access to data**. In this architecture, calculations and business rules remain in code and SQL; the language model helps interpret the results. Dashboards, pipelines, and integration into corporate workflows are further steps.

> [!IMPORTANT]
> Before starting, check the [prerequisites](docs/en/getting-started/PREREQUISITES.md): a project with billing enabled, deployment permissions, and access to the API and Google Ads account. Resources may incur charges. In an institutional environment, arrange these permissions with the team responsible.

## 🧪 Learn by doing

Each checkpoint tells you what to verify before moving on. New acronym? Look it up in the [glossary](docs/en/GLOSSARY.md). Need to see the interface? The [Portuguese videos](docs/en/guides/VIDEOS-PT-BR.md) supplement the written steps.

You can also share this repository with **your preferred AI assistant**, such as ChatGPT, Codex, Claude, or Gemini, and request guidance with the [tutoring prompt](docs/en/guides/AI-TUTOR.md). It asks the tutor to explain commands and check results with you. Redact values when sharing errors or configuration, and keep credentials out of the conversation.

<details>
<summary>Reference version and guide checks</summary>

The guide pins commit `44ca7770519362c8f334875477e1ceb499f8d2dd` of the official server. The [deployment guide](docs/en/getting-started/DEPLOY.md) explains how to prepare that source; the [review record](docs/en/REVIEW.md) lists local checks and what still requires testing in your environment.

</details>

## 📚 Reference

[Full index](docs/en/README.md) · [Security](docs/en/SECURITY.md) · [Official sources](docs/en/REFERENCES.md) · [Contributing](CONTRIBUTING.md)

The guide and its original files use the [MIT license](LICENSE): you may use, study, adapt, and redistribute them, including commercially, while retaining the license notice. The server is maintained by Google's official project and has its own license, described in the [third-party notices](THIRD_PARTY_NOTICES.md).
