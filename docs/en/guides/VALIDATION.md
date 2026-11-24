# 04 · Is the light on? Validate the server and query

[Português](../../guides/VALIDATION.md) · [Index](../README.md)

A ready service shows that the container started. HTTP 401 shows that an anonymous request was rejected. Signing in shows that the authorization flow progressed. **Only a successful query proves access to the Google Ads API.** We will test these separately.

## 1. Check the revision and endpoint

In Cloud Shell, with the variables from the [deployment guide](../getting-started/DEPLOY.md):

~~~bash
gcloud run services describe "$SERVICE" --region="$REGION" \
  --project="$PROJECT_ID" --format='yaml(status.conditions,status.url)'

curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' \
  -X POST -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"anonymous-check","version":"1.0"}}}' \
  "$SERVICE_URL/mcp"
~~~

**Expected:** the revision is ready and authentication is required, normally with HTTP 401. This does not yet validate the Client Secret, callback, or Ads access. The example sends an anonymous request using a 2025 protocol version that this baseline keeps compatible; it is not a full client or a universal test for every MCP protocol version. HTTP 404 means check the URL; 5xx means check startup logs; 403 may come from IAM/network before OAuth. Do not remove authentication to make the test turn green.

## 2. Choose a client

Use an installed client that supports MCP over HTTP and OAuth. Access to models/assistants may depend on account, plan, and corporate policies. See the [official references](../REFERENCES.md). Using an AI assistant as a tutor to read this guide is different from connecting an MCP client to the server.

### VS Code with agents/Copilot enabled

On your computer, open a folder in VS Code. In the Command Palette, search for **MCP: Add Server**, choose HTTP, enter the URL ending in `/mcp`, and name the connection. To configure it for the folder, create `.vscode/mcp.json` with the example below, replacing only the sample URL. Do not put secrets or tokens in it. This format is **specific to VS Code**, not universal.

~~~json
{
  "servers": {
    "google-ads-mcp": {
      "type": "http",
      "url": "https://SEU-SERVICO.a.run.app/mcp"
    }
  }
}
~~~

Start the connection using the editor/MCP command for your version. Review server trust and complete Google sign-in with the authorized test user. In the agent chat, check the enabled tools and their approvals; do not enable unrestricted execution to bypass an error.

### Codex CLI already installed and signed in

Run this **in the terminal on the computer where Codex is installed**, not accidentally in Cloud Shell. Cloud Shell variables are not transferred to it.

~~~bash
export SERVICE_URL="https://SEU-SERVICO.a.run.app"
codex mcp add google-ads-mcp --url "$SERVICE_URL/mcp"
codex mcp login google-ads-mcp
codex mcp list
~~~

If `codex` is not recognized, install/configure it using the official guide before continuing. These commands register/authenticate the connection; they do not call tools. Open a Codex session in your folder for the next tests.

## 3. Check the tools

Ask the assistant:

> List this server's tools. Confirm `customers_list_accessible_customers`, `metadata_get_resource_metadata`, and `search_search`. Do not query data yet. If you find tools to create assets, upload videos, or change labels, stop and report: this guide's read-only configuration is not applied.

The baseline uses namespaces; older versions may have different names. The absence of mutation tools confirms this server's configuration, not a reduced OAuth scope or all permissions of the Google identity.

## 4. Choose an authorized account

> Run `customers_list_accessible_customers`. Show the IDs I need to choose an authorized account. Do not try to query accounts I have not identified.

Choose an account you are authorized to query. `customer_id` identifies the target account; `login_customer_id` identifies the manager account when the call depends on that access.

> [!NOTE]
> This list does not traverse the MCC hierarchy: a child account accessible through a manager may not appear here. Confirm the child ID with the responsible team and use it as `customer_id`; include the MCC's `login_customer_id` in the query when access depends on it.

## 5. Run a small query

First check `customer` metadata to confirm the fields are available. Metadata shows what can be queried; use `search_search` to retrieve the account's values.

Choose an authorized account. The following are **arguments for `search_search`**, not a Bash command or a complete HTTP request. Replace the ID and add `login_customer_id` only if your manager-account access requires it.

~~~json
{
  "customer_id": "1234567890",
  "resource": "customer",
  "fields": [
    "customer.id",
    "customer.descriptive_name",
    "customer.currency_code",
    "customer.time_zone"
  ],
  "limit": 1
}
~~~

Use the returned `currency_code` and `time_zone` when interpreting metrics and dates. Then choose two complete dates in the account's time zone and up to ten rows for the campaign query:

~~~json
{
  "customer_id": "1234567890",
  "resource": "campaign",
  "fields": [
    "campaign.id",
    "campaign.name",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros"
  ],
  "conditions": [
    "segments.date BETWEEN '2026-11-01' AND '2026-11-07'"
  ],
  "limit": 10
}
~~~

Prompt to include:

> Check metadata for `campaign` and verify that the example fields are compatible. Use the account and dates I confirm. Run the read-only query with no more than ten rows and no current-status filter for this historical period. Report the account's currency and time zone, and show the original `cost_micros`. Do not invent numbers, mix currencies, or treat ten rows as the account total. If there are no rows, explain that an empty result can be valid and suggest how to check the account, period, and activity.

Because `segments.date` is in the filter but not in the selected fields, each row aggregates a campaign across the full date range. If you add `segments.date` to `fields`, the result has one row per campaign and day. `limit: 10` caps returned rows; it is not the total for the period. If you add `campaign.status`, interpret it as the campaign's current status, not its status on each past date.

Convert micros with decimal arithmetic in code. This example is fictional; check the `currency_code` value by reading `customer` after confirming the field is available in metadata. The value below is not a real account response:

~~~python
from decimal import Decimal

currency_code = "BRL"  # fictional; replace with the value read from the account
cost_micros = 1_234_567  # fictional metrics.cost_micros example
cost = Decimal(cost_micros) / Decimal(1_000_000)

print(f"{currency_code} {cost}")  # BRL 1.234567
~~~

**Checkpoint:** compare a campaign in Google Ads using the same account, period, and time zone. Platform-attributed metrics are not the same as validated records in another database. Use SQL, Python, and business rules for reproducible calculations and reconciliation; ask the LLM to interpret checked results and suggest hypotheses.

> [!IMPORTANT]
> MCP makes this query on demand. This guide does not configure recurring extraction, analytical storage, or a dashboard feed.

## 6. Record what actually happened

| Step | Evidence without secrets |
| --- | --- |
| Build | Upstream commit, build ID, and image digest |
| Service | Ready revision and base URL |
| Anonymous | HTTP status code and date; no tokens/authorization headers |
| OAuth | Sign-in completed; do not copy credentials |
| Tools | Three read tools present; mutation tools absent |
| Accounts | Identity/permissions checked; hide IDs when sharing |
| Query | Fields, period, rows, currency, and time zone checked |
| Result | Success, coherent empty result, or diagnosed error; never mark “passed” without running it |

Scale-to-zero, restarts, and new revisions can end MCP sessions/HTTP streams even with OAuth persisted in Firestore. Reconnect the client; do not delete secrets or the database to recover a session. If something fails, use [troubleshooting](TROUBLESHOOTING.md).

[← OAuth](OAUTH-AND-SECRETS.md) · [Errors and diagnosis →](TROUBLESHOOTING.md)

## OAuth continuity across revisions

Follow the [persistence experiment](OAUTH-PERSISTENCE.md): compare queries before and after a revision change without manual OAuth reconnection. Test renewal after expiry separately.
