# Glossary

Use this glossary as a map between Google Cloud and Google Ads terms. An analogy can help you remember a function; the text in parentheses names the actual mechanism.

| Term | In plain language | What it means in this guide |
| --- | --- | --- |
| **MCP** | A standard connection between an AI client and tools. | The Model Context Protocol defines how a client discovers and calls tools offered by a server. The model decides whether and when to call a tool, depending on the client and usage policy. |
| **MCP client** | The app that talks to the server. | A compatible client receives the `/mcp` URL, completes authentication, and displays the available tools. |
| **Google Ads MCP server** | The bridge between the client and the API. | The official `googleads/google-ads-mcp` program, hosted on Cloud Run by this tutorial. It provides tools; it does not contain your campaigns. |
| **Google Ads API** | The official source for ads data and actions. | Google's API queried by the server. The Cloud project must have the API enabled and an appropriate access level; the authenticated identity also needs permission on the accounts. |
| **Cloud Run** | The place where the HTTP service is available. | A managed Google Cloud platform that runs the container and provides an HTTPS URL. Instances may start and stop; the temporary filesystem is not a durable place to keep state. |
| **Cloud Shell** | A terminal opened inside the Google Cloud Console. | The Bash environment used by this guide to run `gcloud`, Git, and setup scripts without installing Docker on your computer. Commands still change the remote project when described as doing so. |
| **Cloud Build** | A workshop that assembles the package on another computer. | A service that builds the server image from source code and sends it to Artifact Registry. Builds may incur charges. |
| **Container image** | A package containing the program and what it needs to run. | An artifact created by the build and run on Cloud Run. A tag is a label; a digest identifies the published contents more precisely. |
| **Google Cloud project / project ID** | An administrative folder and its identifier. | The project where services, permissions, billing, and configuration data live. The ID used in commands differs from the display name shown to people in the Console. |
| **Region** | The geographic area where a resource is hosted. | The region chosen for Cloud Run, Artifact Registry, and other regional resources. The choice affects availability, latency, and price. |
| **Billing** | The account that pays for resources used. | The project must be associated with a billing account to use this tutorial's services. Budget alerts do not create an automatic spending cap. |
| **OAuth 2.0** | The user's sign-in and authorization flow. | The client starts Google sign-in and receives authorization for the application. The server uses this flow to access the Google Ads API on behalf of the signed-in person, according to their permissions. |
| **OAuth Client ID** | The public identifier for the sign-in application. | A value used to identify the OAuth client. It is not a password, although it should still be configured only in the correct application. |
| **OAuth client secret** | A confidential value for the OAuth application. | Keep it in Secret Manager; do not paste it into documentation, prompts, a repository, or terminal history. |
| **Google user identity** | The person who completes sign-in. | This identity authenticates the session the server uses to access Ads. The API can return only data that person can access. |
| **Service account** | The service's own technical identity. | The identity Cloud Run uses to read secrets and write OAuth state. It is not the person who accesses Google Ads and does not replace the user's OAuth sign-in. |
| **IAM** | Rules that control who can do what in Google Cloud. | Identity and Access Management controls actions on Google Cloud resources; for example, which service account can read a secret. It is distinct from a person's permissions inside Google Ads. |
| **Secret Manager** | A vault for confidential values. | A service used to store secrets and control which runtime identity can read them. At deployment, reference the secret; do not print its value. |
| **Firestore** | A managed database that keeps state across restarts. | In this guide, it stores persistent OAuth state so the service does not depend on a temporary Cloud Run instance disk. It must be prepared and have the appropriate IAM access. |
| **OAuth state** | The working memory of the sign-in flow. | Session information and tokens the server must keep between requests. The persistent backend must be compatible with the pinned server version. |
| **Streamable HTTP** | The MCP format carried over HTTPS. | The mechanism the client and remote server use to exchange requests and responses at the `/mcp` path. |
| **Endpoint** | The address used to talk to the service. | In this guide, the Cloud Run URL with `/mcp` appended, such as `https://your-service.../mcp`. Use the exact published URL to configure OAuth and the client. |
| **MCC / manager account** | An Ads account that manages other accounts. | It is needed only if your organization's access arrangement depends on it. A list of accessible customers does not guarantee that every MCC child account will appear; `login_customer_id` applies only to flows that go through a manager account. |
| **Google Ads API access level** | The gate that defines which environments the project can use. | Enabling the API grants test access. For production accounts, check the current level and requirements in the Google Ads API overview in Cloud Console; a request and approval may be required. |
| **Developer token** | An API credential used by the previous access model. | Google retired the new-token flow on September 9, 2026 and moved access management to the Cloud project. An older commit may still mention the variable or accept existing credentials; follow that commit's documentation and current official guidance. |
| **`tools_config.yaml` / allowlist** | The list of what the server can offer to the client. | A server-version configuration that includes or excludes tools. The profile prepared by this tutorial limits the exposed list, but each name must be reviewed; OAuth alone does not prevent write calls. |
| **GAQL** | The Google Ads API query language. | Google Ads Query Language specifies which resources, fields, and time periods are queried. The query must match available fields and permissions. |
| **Quota** | A usage limit for a service or API. | Google Cloud and the Google Ads API limit how many operations or resources may be used. Quota errors are not fixed just by restarting the server. |
| **Acceptance testing** | The formal rehearsal before real use. | Validation using the environment, tools, access, logs, and controls approved by the organization. Reproducing this tutorial is not the same as acceptance testing and does not certify production readiness. |
| **TCO** | The total cost over time. | Total Cost of Ownership: infrastructure, maintenance, monitoring, security, support, and team time, in addition to each service charge. |

**Next:** [Documentation index](README.md) · [Architecture](ARCHITECTURE.md) · [AI tutor](guides/AI-TUTOR.md)
