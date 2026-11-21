# 01 · Prepare the project and check access

This deployment is designed to run in **Cloud Shell**, the Bash terminal opened from the Google Cloud Console. That way, you do not need to install tools on your computer. Cloud Shell is still just your workbench: commands publish resources to the selected project, and some may incur charges.

## Before opening the terminal

Have these ready:

- **A Google Cloud project** approved by your organization, with billing enabled. Write down the **project ID** (a short identifier), not the display name shown in the Console.
- **Permission to make the required changes**, or an administrator who can make them. The guide enables APIs, creates a source-staging bucket, builds and stores an image, and creates a Cloud Run service, two service accounts, three secrets, and a Firestore database. The build identity reads source, writes images, and writes logs; the runtime identity reads secrets and accesses Firestore. The staging bucket persists until you clean it up. Ask for specific permissions rather than using Owner as a shortcut.
- **Google Ads API access in the same project.** Enabling the API opens the test environment; querying production accounts requires the appropriate access level, which may depend on a request in the Google Cloud Console. This process changed in 2026. See the [official access-level page](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=en). This guide pins commit 44ca7770519362c8f334875477e1ceb499f8d2dd. If you update it, review requirements and configuration instead of assuming the procedure is unchanged.
- **A Google account with access to the ads account** you plan to query. API access for the project and a user's permission on the account are two separate checks. If your organization accesses clients through a manager account (MCC), use the arrangement approved by the team responsible.
- **An OAuth client** that can be configured for the HTTP server, with permission to register the exact server redirect URL required by the chosen commit. The MCP client uses another step in the flow; do not register its URL as the server callback. You will configure the OAuth client in the [OAuth and Secret Manager](../guides/OAUTH-AND-SECRETS.md) guide.
- **An MCP client that supports Streamable HTTP and OAuth** for final validation. Sign-in confirms identity; it does not by itself determine which ads tools the server offers.

If another team needs to handle any item, pause here and send them this list. You do not need to share a password, secret, or credential file to request access.

## Permissions to request from an administrator

In a personal project you created, your identity may already have the required access. In a corporate environment, send this table to the responsible team. It lists the operations used by the guide rather than recommending one broad role. An administrator can run just the resource-creation and IAM steps, leaving deployment to you.

| Human operator's task | Permissions to check | Scope |
| --- | --- | --- |
| Enable and use APIs | serviceusage.services.enable and serviceusage.services.use | Lab project |
| Create service accounts | iam.serviceAccounts.create | Project |
| Submit a build | cloudbuild.builds.create | Project |
| Upload build source | storage.buckets.get and storage.objects.create | Staging bucket |
| Act as the build and runtime identities | iam.serviceAccounts.actAs | Each of the two service accounts |
| Read the image for deployment | artifactregistry.repositories.downloadArtifacts | Image repository |
| Create/update Cloud Run and allow ingress | run.services.create, run.services.update, and run.services.setIamPolicy | Lab project/service |
| Create the repository, bucket, secrets, and database | artifactregistry.repositories.create, storage.buckets.create, secretmanager.secrets.create, secretmanager.versions.add, and datastore.databases.create | Project and new resources |
| Grant the access used by the guide | The resource's setIamPolicy permission; resourcemanager.projects.setIamPolicy for project-level bindings | Lab resources/project only |

Deployment step 4 includes Object Creator on the bucket for the operator and Service Account User on both identities where needed. Object Creator does not replace permission to read bucket metadata. The build account receives source-read, image-write, and log-write access. The runtime account receives access to the three secrets and Firestore state. Effective access also depends on organizational policies; do not remove those policies to work around a denial.

See [user-specified build service accounts](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts) and [required roles for Cloud Run deployment](https://docs.cloud.google.com/run/docs/deploying#required_roles).


## Checkpoint 1 · check the account and project

In the Google Cloud Console, select the approved test project and confirm that billing is linked. Then open Cloud Shell. Its name and icon may change, but it is in the Console header.

These two commands only report which tools are available in the terminal; they do not create or change resources:

```bash
# Check whether the terminal recognizes the Google Cloud tool.
gcloud --version

# Check whether Git is available to download the official source code.
git --version
```

If a command is not found in Cloud Shell, pause and check that you opened the right terminal or whether your organization has disabled a tool.

## Checkpoint 2 · explicitly select the project

```bash
# Replace the text in quotes with the project ID copied from the project picker.
export PROJECT_ID="SEU_ID_DE_PROJETO"

# Set the project in your active gcloud configuration.
gcloud config set project "$PROJECT_ID"

# Show the selected project; compare it with the Console.
gcloud config get-value project

# Show which Google account is authenticated in gcloud.
gcloud auth list --filter=status:ACTIVE --format='value(account)'
```

`PROJECT_ID` is a placeholder: replace it with the actual identifier. Carefully check the project and account before continuing. `gcloud config set project` changes your profile's active gcloud configuration and persists after this terminal closes; it does not create a project or change a Google Ads account.

**Checkpoint:** the terminal shows the correct project ID and the Google account with the permissions agreed with your organization. If not, correct the selection before enabling APIs.

## Checkpoint 3 · enable APIs used by this guide

The command below changes project configuration by enabling services used by this tutorial to run the server, build and store its image, read secrets, and query the ads API. Enabling an API is not the same as receiving production access to the Google Ads API. Creating and using the other resources may incur charges.

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  iam.googleapis.com \
  logging.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  googleads.googleapis.com
```

**Checkpoint:** in the Console, confirm that the APIs used in this guide are enabled. Also check the Google Ads API overview page to confirm that the project has the access level you want. For production, do not assume that enabling the API is enough: you may need to request access and wait for approval.

## What this tutorial will create

The next guide clones a specific commit of the official server, prepares a restricted tool configuration, builds an image in Cloud Build, and publishes the service to Cloud Run. The service uses a runtime identity with restricted access to secrets and to OAuth state storage in Firestore. You do not need to install Docker on your computer; the build runs in Google Cloud and may be billed.

Before authorizing any account, review the tools included in the commit and the configuration prepared by the guide. A reduced profile limits what is available to the client, but OAuth and the sign-in screen are not, by themselves, barriers that make write tools impossible.

## Costs and control

Cloud Build, Artifact Registry, Cloud Run, Secret Manager, Firestore, Cloud Logging, and data transfer may incur charges. The total depends on the region, builds, query volume, storage, and log retention. Set a budget and monitor billing from the start; budget alerts notify you, but do not automatically stop usage.

See the [cost guidance](../guides/COSTS.md) before publishing. To pause, remove resources, or clear state, follow your project's documentation and operating instructions; do not run copied deletion commands until you have identified each resource.

**Next:** [02 · Deploy to Cloud Run](DEPLOY.md). The deployment guide marks when to pause and configure OAuth before publishing.
