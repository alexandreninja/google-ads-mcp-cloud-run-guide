# 05 · Troubleshooting

Use this page after recording **the step, full error message, and approximate time** of a failure. Cloud Run, OAuth, MCP, and Google Ads errors come from different layers; the same 401 or 403 can have different causes.

## Find the first failed step

| Step | Expected signal | Start here if it fails |
| --- | --- | --- |
| Project and billing | The intended project is linked to an active billing account | [Project, billing, or API](#project-billing-or-api) |
| Build and image | Cloud Build succeeds and the image appears in Artifact Registry | [Build or image upload](#build-or-image-upload) |
| Cloud Run revision | The revision is ready and the service has an HTTPS URL | [Revision does not become ready](#revision-does-not-become-ready) |
| OAuth | Sign-in completes and returns to the configured address | [OAuth errors](#oauth-errors) |
| MCP client | The client connects and discovers tools | [Client cannot find MCP tools](#client-cannot-find-mcp-tools) |
| Google Ads API | The intended account can be queried with authorization | [Accounts or queries fail](#accounts-or-queries-fail) |

First check the CLI project:

~~~bash
gcloud config get-value project
~~~

The output should match the guide's PROJECT_ID. If it does not, select the correct project before retrying. Deploying to the wrong project can create resources and charges in another account.

## Project, billing, or API

### The error mentions billing, SERVICE_DISABLED, or PERMISSION_DENIED

1. Check the selected project at the top of the Google Cloud Console.
2. Under Billing, confirm that the project is linked to an active billing account. Creating a project does not automatically enable billing.
3. Under APIs & Services, check that the APIs required by this guide are enabled.
4. If access is denied, ask an administrator to inspect the specific missing permission. Do not fix IAM errors by granting the broad Owner role.

Enabling the Google Ads API and receiving production access are separate checks. For production, see [Accounts or queries fail](#accounts-or-queries-fail).

## Build or image upload

### The build cannot find Dockerfile or project files

The command in this guide submits UPSTREAM_DIR: the prepared checkout of the **official Google Ads MCP server** at the pinned commit. Confirm that git -C "$UPSTREAM_DIR" rev-parse HEAD reports the expected commit and that the folder contains Dockerfile. Do not build from the root of this documentation repository.

If the command cannot locate UPSTREAM_DIR, return to the deployment preparation and check GUIDE_DIR and UPSTREAM_DIR. Build source is uploaded to Cloud Storage before Cloud Build starts.

### Uploading source to Cloud Storage is denied

The guide uses its own bucket through --gcs-source-staging-dir. The person or automation running gcloud builds submit needs permission to create the source object in that bucket. Separately, the google-ads-mcp-build service account needs to read it; the guide grants that account roles/storage.objectViewer.

If the error names storage.objects.create, ask an administrator for upload permission scoped to the staging bucket for the identity running the CLI. Deployment step 4 includes Object Creator for that operator. The operator also needs storage.buckets.get for bucket metadata. Do not replace the build account's read role with Owner.

The submitter also needs cloudbuild.builds.create in the project and iam.serviceAccounts.actAs on the selected build service account. See the [permissions table](../getting-started/PREREQUISITES.md). If the message names another permission, ask the administrator to inspect that exact permission and the applicable organization policy.

### Building succeeds, but pushing to Artifact Registry is denied

Check that the Docker repository exists in the region used by the image address and that the build identity can write to it. Cloud Build uses its own identity; it is not the service account that runs Cloud Run.

Open the build details and find the first failed step. It usually distinguishes an image-build problem from an upload-permission or repository-location problem.

## Revision does not become ready

In the Console, open **Cloud Run → service → Logs** and filter for the current revision. To inspect logs from the CLI:

~~~bash
gcloud run services logs read "$SERVICE" --region="$REGION" --limit=20
~~~

Read the first startup error; later messages may only be consequences. Check:

- The revision points to the image you just published.
- Environment and secret names match the pinned server version.
- The runtime service account can read the required secrets and access Firestore.
- All three numeric secret versions exist and are enabled.
- The image includes the Firestore extra and the intended database exists.
- Non-secret settings, including the public base URL and Cloud project, are correct.

For a container that never listens on the expected port, check that both OAuth Client ID and Client Secret are present: the baseline chooses HTTP mode when both are configured.

If you corrected a secret, check the version attached to the revision. Secrets injected as environment variables are read at instance startup. Publishing a secret version alone does not update an already running instance. Updating the Cloud Run configuration creates a revision. See [Cloud Run secrets](https://docs.cloud.google.com/run/docs/configuring/services/secrets).

Do not copy secret values into tickets, screenshots, or shared logs.

## OAuth errors

### redirect_uri_mismatch

Google received a redirect address that differs from the one registered on the OAuth client. Compare:

- The HTTPS hostname of the current Cloud Run URL.
- The callback path required by the deployed upstream version.
- The authorized redirect URI list on the OAuth Web application client used by the server.

For this baseline, register SERVICE_URL/auth/callback. Scheme, hostname, path, and any trailing slash must match exactly. The local/dynamic MCP client callback is handled by the proxy and is not another Google callback to register.

### invalid_client

Google did not recognize the supplied OAuth client. Check that Client ID and Client Secret belong to the same OAuth client, that its Cloud project is correct, and that the revision references the intended secret version. If the secret was rotated, deploy a revision using the compatible version.

### Sign-in completes, but the return flow does not finish

Check the base URL and registered redirect URI. The public base URL must be the current service's HTTPS origin, without /mcp; its Google callback must match the deployed version. If the service URL or OAuth client changes, update both sides.

For external apps in Testing, check whether the account is an approved test user and whether a new authorization is needed. Do not make an app public merely to bypass a diagnostic message.

## Client cannot find MCP tools

1. Use the service URL with the MCP path documented for the pinned version: /mcp in this guide.
2. Check that the chosen client supports the server's HTTP transport and has completed OAuth.
3. Ask the client to reconnect or rediscover tools after correcting the connection.
4. Inspect Cloud Run logs at the time of the attempt. Authentication, transport, startup, and Google Ads API failures are different.
5. If sign-in succeeds but tools are missing, inspect the tool configuration and namespace prefixes in the deployed version.

An isolated HTTP response does not prove that the MCP connection is ready. Test discovery with a compatible MCP client as described in [Validation](VALIDATION.md). Restarts, scale-to-zero, and the 300-second HTTP timeout may require streaming clients to reconnect.

## Accounts or queries fail

### The account list is empty or does not include the account you expected

- Check which Google account completed OAuth. It must have access to the Google Ads account.
- The customer-list tool lists directly accessible accounts; it does not guarantee every child account of an MCC.
- For manager-account access, check the intended customer_id and conditional login_customer_id.
- Follow the schema's account-ID format, without punctuation.
- Distinguish the user's Ads permission from the Cloud project's API access level.

### A test account works, but a production account does not

Since **September 9, 2026**, developer tokens no longer determine Google Ads API access levels. Enabling the API grants test access. For production accounts, inspect the access level and request the required level on the **Google Ads API overview** page in the Cloud project that issued the OAuth credentials. New access requests no longer belong in the old Google Ads API Center.

The documentation associates CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION with API v25 and later. API v24 and earlier may return ACTION_NOT_PERMITTED for this problem. Check the project's API access level before changing account IDs or redoing OAuth.

The official migration page also lists known access-approval issues. Do not unlink billing as a generic workaround in a project running Cloud Run; it can stop paid services. Follow the documented diagnostic and ask the project administrator.

### The API rejects a field or GAQL query

Confirm the Google Ads API version used by the pinned server, then check field/metric availability and compatibility. Use metadata_get_resource_metadata. Do not remove a metric merely to hide an error without understanding the compatibility rule.

An empty query result can be valid. Check the account, finite date range, time zone, campaign activity, and limit before treating it as an authorization failure.

## HTTP 401 or 403

The status alone does not identify which layer refused the request:

- **401 before sign-in:** the MCP server may be asking for valid OAuth. This can be expected for an anonymous request to the protected /mcp endpoint.
- **403 from Cloud Run:** check whether the design allows clients to reach HTTP ingress. Allowing unauthenticated Cloud Run invocation does not remove application OAuth or Google Ads account permissions.
- **403 after OAuth:** inspect the response and logs to distinguish account permission, project API access level, and tool-policy rules.

Do not remove authentication protections to hide an error. Identify the layer that returned it.

## When asking for help

Share the step, approximate time, region, revision, upstream version/commit, and error with secrets removed. Hide Client Secrets, OAuth tokens, signing/storage keys, cookies, personal data, and unnecessary account IDs. For upstream server failures, use the [official project's issues](https://github.com/googleads/google-ads-mcp/issues).

[← Validation](VALIDATION.md) · [Costs and operations →](OPERATIONS.md) · [Videos in Portuguese](VIDEOS-PT-BR.md)
