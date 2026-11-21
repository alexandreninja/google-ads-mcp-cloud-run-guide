# 02 · From source code to server: deployment on Cloud Run

[Português](../../getting-started/DEPLOY.md) · [Index](../README.md)

Think of this as a small workshop: Cloud Build assembles the application, Artifact Registry stores the image, and Cloud Run runs it. Firestore preserves authorization state when the container restarts. Each part has a reason; check the result before fitting in the next one.

**Before you start:** complete the [prerequisites](PREREQUISITES.md), including billing, permissions, and Google Ads API access level. Use a dedicated lab project and **the same project for OAuth, the API, and runtime** in this walkthrough. Your organization may require IT support for IAM, OAuth, and HTTP exposure.

**Basis for this revision:** commands and configuration were checked against official sources and upstream commit **44ca7770519362c8f334875477e1ceb499f8d2dd** on November 21, 2026. The package in that commit declares 0.0.6; this does not present it as a tagged stable release. This documentation review did not perform a new deployment in Google Cloud. Upstream dependencies and base images have moving ranges/tags: pinning the commit does not make every build identical. Record the resulting digest.

Run one command at a time and inspect its output. If any command fails, stop before the next one: interactive Bash does not automatically stop the rest of a pasted block. A checkpoint is valid only when all preceding commands succeeded.

## 1. Open the workbench

In the [Google Cloud Console](https://console.cloud.google.com/), open **Cloud Shell** using the terminal icon at the top of the page. Authorize the session if the Console asks. Commands use **Bash in Cloud Shell**; do not run them directly in Windows PowerShell or Command Prompt.

~~~bash
git clone https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide.git
cd google-ads-mcp-cloud-run-guide
export GUIDE_DIR="$PWD"
~~~

If the folder already exists, enter the correct clone; do not delete your work just to repeat the example. **Checkpoint:** `pwd` ends with `google-ads-mcp-cloud-run-guide` and the `config` folder contains the guide's configuration files.

## 2. Identify the project before creating resources

Replace only `SEU_PROJECT_ID`. The ID is not the display name or project number. The region is an example; choose a location and cost profile that fit your needs and your organization's rules.

~~~bash
export PROJECT_ID="SEU_PROJECT_ID"
export REGION="us-central1"
export REPOSITORY="mcp-servers"
export SERVICE="google-ads-mcp"
export RUNTIME_SA_NAME="google-ads-mcp-runtime"
export BUILD_SA_NAME="google-ads-mcp-build"
export RUNTIME_SA_EMAIL="$RUNTIME_SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
export BUILD_SA_EMAIL="$BUILD_SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
export SOURCE_BUCKET="gs://$PROJECT_ID-mcp-source"
export FIRESTORE_DATABASE="(default)"
export UPSTREAM_COMMIT="44ca7770519362c8f334875477e1ceb499f8d2dd"
export UPSTREAM_DIR="$GUIDE_DIR/.work/google-ads-mcp"
export IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE:44ca77705193"

gcloud config set project "$PROJECT_ID"
gcloud projects describe "$PROJECT_ID" --format='value(projectId,name)'
gcloud auth list --filter=status:ACTIVE --format='value(account)'
~~~

**Checkpoint:** the project and identity match the authorized lab. Check billing in the Console and set [budget alerts](../guides/COSTS.md). The next steps create resources and may incur charges. Limiting instances does not limit the bill. If Cloud Shell restarts, reset the variables in this section.

## 3. Enable the APIs

~~~bash
gcloud services enable \
  googleads.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  logging.googleapis.com \
  iam.googleapis.com \
  --project="$PROJECT_ID"
~~~

**Checkpoint:** the command finishes without errors. Enabling the Google Ads API grants test access; querying production accounts requires the appropriate access level in the OAuth project. Since September 9, 2026, onboarding uses the Cloud project; do not request a developer token by following old videos. See the [prerequisites](PREREQUISITES.md).

## 4. Separate identities and create storage

The identity that builds the image does not need to read OAuth secrets. The identity that runs the server does not need to build images. This separation limits the reach of each service account.

~~~bash
gcloud iam service-accounts create "$BUILD_SA_NAME" \
  --display-name="Build do Google Ads MCP" --project="$PROJECT_ID"
gcloud iam service-accounts create "$RUNTIME_SA_NAME" \
  --display-name="Execucao do Google Ads MCP" --project="$PROJECT_ID"

gcloud artifacts repositories create "$REPOSITORY" \
  --repository-format=docker --location="$REGION" \
  --description="Imagens do laboratorio MCP" --project="$PROJECT_ID"

gcloud storage buckets create "$SOURCE_BUCKET" \
  --location="$REGION" --uniform-bucket-level-access --project="$PROJECT_ID"

gcloud artifacts repositories add-iam-policy-binding "$REPOSITORY" \
  --location="$REGION" --member="serviceAccount:$BUILD_SA_EMAIL" \
  --role=roles/artifactregistry.writer --project="$PROJECT_ID"
gcloud storage buckets add-iam-policy-binding "$SOURCE_BUCKET" \
  --member="serviceAccount:$BUILD_SA_EMAIL" --role=roles/storage.objectViewer
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$BUILD_SA_EMAIL" --role=roles/logging.logWriter
~~~

The human Cloud Shell operator must be able to upload source to the bucket and act as both service accounts. If this access is missing, an authorized administrator can grant it on these resources only. Replace SEU_EMAIL_GOOGLE with the active user email checked in step 2. This example assumes a human user, not a service account or group.

~~~bash
export OPERATOR_EMAIL="SEU_EMAIL_GOOGLE"
gcloud storage buckets add-iam-policy-binding "$SOURCE_BUCKET" \
  --member="user:$OPERATOR_EMAIL" --role=roles/storage.objectCreator
for ACT_AS_EMAIL in "$BUILD_SA_EMAIL" "$RUNTIME_SA_EMAIL"; do
  gcloud iam service-accounts add-iam-policy-binding "$ACT_AS_EMAIL" \
    --member="user:$OPERATOR_EMAIL" --role=roles/iam.serviceAccountUser \
    --project="$PROJECT_ID"
done
~~~

**Checkpoint:** both service accounts, the image repository, and the bucket exist. If a resource already exists, check the project and region before reusing it. Do not treat `Permission denied` as `Already exists`. The person running builds/deployments needs permission to act as the corresponding accounts (`iam.serviceAccounts.actAs`); ask an administrator for the scoped access listed in the prerequisites instead of granting Owner indiscriminately.

## 5. Keep authorization outside the container

In a **dedicated project with no existing database**, create Firestore Standard in Native mode. Review the location before creating it. If a `(default)` database already exists, confirm its type and location; do not replace or change a production database to follow the example.

~~~bash
gcloud firestore databases create --database="$FIRESTORE_DATABASE" \
  --location="$REGION" --type=firestore-native --edition=standard \
  --project="$PROJECT_ID"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$RUNTIME_SA_EMAIL" --role=roles/datastore.user
gcloud firestore databases describe --database="$FIRESTORE_DATABASE" \
  --project="$PROJECT_ID"
~~~

**Checkpoint:** the database is available in Native mode. The `datastore.user` role grants access to project data, which is why this lab should be isolated. Firestore stores OAuth state, not an analytics database or every HTTP session. The upstream backend filters expired records on read but does not remove them automatically; plan [cleanup and retention](../guides/OPERATIONS.md).

## 6. Set up OAuth and three secret versions

Follow [03 · OAuth and Secret Manager, through the checkpoint before deployment](../guides/OAUTH-AND-SECRETS.md). Return with `OAUTH_CLIENT_ID` set and three secrets created, each with enabled **version 1** and access granted to the runtime account. Do not continue with empty secret containers.

## 7. Prepare and build the official server

~~~bash
mkdir -p "$GUIDE_DIR/.work"
git clone https://github.com/googleads/google-ads-mcp.git "$UPSTREAM_DIR"
git -C "$UPSTREAM_DIR" checkout --detach "$UPSTREAM_COMMIT"
python3 "$GUIDE_DIR/scripts/prepare_source.py" "$UPSTREAM_DIR"
git -C "$UPSTREAM_DIR" rev-parse HEAD
git -C "$UPSTREAM_DIR" diff -- Dockerfile
cat "$UPSTREAM_DIR/tools_config.yaml"
~~~

The helper makes local changes only: it checks the commit, enables the optional Firestore dependency in the Dockerfile, and copies the configuration that exposes only customers, search, and metadata. Labels and assets are disabled. It preserves the rest of the Dockerfile, including the upstream FastMCP compatibility adjustments. Read those changes before adopting another version.

**Checkpoint:** the SHA is correct; the install includes the `.[firestore]` extra; labels and assets are `false`. This restriction applies to the tools in this image. It does not reduce the `adwords` OAuth scope, the Google identity's permissions, or other API access.

~~~bash
gcloud builds submit "$UPSTREAM_DIR" \
  --config="$GUIDE_DIR/config/cloudbuild.yaml" \
  --substitutions="_IMAGE=$IMAGE" \
  --service-account="projects/$PROJECT_ID/serviceAccounts/$BUILD_SA_EMAIL" \
  --gcs-source-staging-dir="$SOURCE_BUCKET/source" \
  --project="$PROJECT_ID"
~~~

**Checkpoint:** the build reports `SUCCESS` and the image appears in Artifact Registry. Record its digest shown in the build. The submitted context is the prepared official checkout; do not put credentials in that folder. Downloads, quotas, or dependencies can stop the build even when the commit is pinned. Do not remove Dockerfile checks to force a success.

## 8. Deploy and find the URL

This is a pilot with at most one instance and scale-to-zero. It keeps upstream stateful HTTP and the default Cloud Run concurrency. Do not set concurrency to 1 with long-lived SSE streams: one connection can occupy the only slot. This is not a high-availability architecture. The 300-second timeout ends long-running HTTP requests after five minutes; clients that keep streams open must be able to reconnect.

~~~bash
gcloud run deploy "$SERVICE" \
  --image="$IMAGE" --region="$REGION" --platform=managed \
  --service-account="$RUNTIME_SA_EMAIL" \
  --allow-unauthenticated --min-instances=0 --max-instances=1 \
  --cpu=1 --memory=1Gi --timeout=300 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_ADS_MCP_OAUTH_CLIENT_ID=$OAUTH_CLIENT_ID,GOOGLE_ADS_MCP_STORAGE_TYPE=firestore,GOOGLE_ADS_MCP_STORAGE_FIRESTORE_PROJECT=$PROJECT_ID,GOOGLE_ADS_MCP_STORAGE_FIRESTORE_DATABASE=$FIRESTORE_DATABASE,GOOGLE_ADS_MCP_TOOLS_CONFIG=/app/tools_config.yaml" \
  --set-secrets="GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET=google-ads-mcp-oauth-client-secret:1,GOOGLE_ADS_MCP_JWT_SIGNING_KEY=google-ads-mcp-jwt-signing-key:1,GOOGLE_ADS_MCP_STORAGE_ENCRYPTION_KEY=google-ads-mcp-storage-key:1" \
  --project="$PROJECT_ID"

export SERVICE_URL="$(gcloud run services describe "$SERVICE" \
  --region="$REGION" --project="$PROJECT_ID" --format='value(status.url)')"
printf '%s\n' "$SERVICE_URL"

gcloud run services update "$SERVICE" --region="$REGION" \
  --update-env-vars="GOOGLE_ADS_MCP_BASE_URL=$SERVICE_URL" \
  --project="$PROJECT_ID"
~~~

In the first revision, the base URL is still the local default; do not start sign-in before the update. **Checkpoint:** the latest revision is ready and the base URL is the generated HTTPS URL, without `/mcp`. Now finish [registering the OAuth callback](../guides/OAUTH-AND-SECRETS.md#after-deployment-register-the-callback).

`--allow-unauthenticated` makes the endpoint reachable at the Cloud Run IAM layer for the OAuth flow. The server requires OAuth for tools, but the endpoint is exposed to the internet and may receive traffic that incurs charges. This does not create a list of authorized collaborators or certify the service. If policy forbids public exposure, pause and ask IT for a compatible architecture; do not work around the policy.

## 9. Get the first piece of evidence

Follow [04 · Validation](../guides/VALIDATION.md). A ready service, an anonymous HTTP 401, and a completed login are different pieces of evidence; access to the Google Ads API is validated only after an authorized query.

For maintenance or to close the lab, see [operations](../guides/OPERATIONS.md), [costs](../guides/COSTS.md), and [security](../SECURITY.md). Deleting Cloud Run does not delete images, secrets, the bucket, or Firestore.

[← Prerequisites](PREREQUISITES.md) · [OAuth and secrets →](../guides/OAUTH-AND-SECRETS.md)
