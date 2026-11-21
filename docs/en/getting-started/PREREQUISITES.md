# 01 · Prepare the project and check access

Use **Cloud Shell**, the Bash terminal in the Google Cloud Console. It includes the tools used by this guide, so you can start in your browser.

## What you need

| Item | What to check |
| --- | --- |
| Google Cloud project | Project **ID**, billing enabled, and permission to create resources |
| Google Ads API | Enabled in the same project, with the access level needed for test or production accounts |
| Google Ads account | A Google identity with permission to query it; manager-account (MCC) access if your account structure requires it |
| OAuth and MCP client | Permission to create a web OAuth client, plus an MCP client that supports Streamable HTTP and OAuth |

> [!IMPORTANT]
> API access for the project and access to the ads account are separate requirements. Production API access may need approval in the Console. See the [current access levels](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=en) before proceeding.

In an organization, arrange access with the Cloud and Google Ads teams. Open the permissions checklist below with them before creating resources. They can run the resource-creation and IAM steps for you; the deployment guide identifies these steps.

<details>
<summary>Permissions checklist to share with an administrator</summary>

The table lists operations used by the guide. Request permissions scoped to the lab rather than using Owner as a shortcut.

| Human operator's task | Permissions to check | Scope |
| --- | --- | --- |
| Enable and use APIs | serviceusage.services.enable and serviceusage.services.use | Lab project |
| Inspect the project and database at the checkpoint | resourcemanager.projects.get and datastore.databases.getMetadata | Lab project/database |
| Create service accounts | iam.serviceAccounts.create | Project |
| Submit and monitor a build | cloudbuild.builds.create, cloudbuild.builds.get, and cloudbuild.builds.list | Project |
| Upload build source | storage.buckets.get and storage.objects.create | Staging bucket |
| Act as the build and runtime identities | iam.serviceAccounts.actAs | Each of the two service accounts |
| Read the image for deployment | artifactregistry.repositories.downloadArtifacts | Image repository |
| Create/update and inspect Cloud Run; configure ingress | run.services.create, run.services.update, run.services.get, run.operations.get, and run.services.setIamPolicy | Lab project/service |
| Create the repository, bucket, secrets, and database | artifactregistry.repositories.create, storage.buckets.create, secretmanager.secrets.create, secretmanager.versions.add, and datastore.databases.create | Project and new resources |
| List secret versions for the checkpoint | secretmanager.versions.list | Each of the three secrets |
| Grant the access used by the guide | The resource's setIamPolicy permission; resourcemanager.projects.setIamPolicy for project-level bindings | Lab resources/project only |

Deployment step 4 provides the operator's build, staging-bucket, image-read, and actAs bindings. Other resource-creation permissions must already be available to whoever runs those steps. The build identity receives source-read, image-write, and log-write access; the runtime identity receives access to the three secrets and Firestore.

These bindings assume a trusted operator in a lab project. The `cloudbuild.builds.create` permission also allows other builds to be submitted, including with the legacy account when available; administrators should review that account's privileges before expanding usage.

Consult [user-specified build identities](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts) and [Cloud Run deployment roles](https://docs.cloud.google.com/run/docs/deploying#required_roles). An organization policy can restrict these actions even when IAM roles have been granted.

</details>

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

## Checkpoint 3 · check Google Ads API access

Open the project's Google Ads API overview in the Console and check the access level available for your intended account. Production access may require an application and approval. [Deployment step 3](DEPLOY.md#3-enable-the-apis) contains the API-enablement command used by this guide.

**Checkpoint:** you know whether you will use a test or production account and have arranged the required API access. Enabling the API alone does not approve production access.

## What comes next

The deployment guide creates separate build and runtime identities, an image repository, a staging bucket, a Cloud Run service, three secrets, and a Firestore database for OAuth state. Cloud Build builds the image; you do not need Docker on your computer.

> [!WARNING]
> Creating and using these resources may incur charges. Review [costs](../guides/COSTS.md) and set a budget before deployment. Budget alerts notify you; they do not automatically stop spending. The [operations guide](../guides/OPERATIONS.md) covers cleanup when you finish the lab.

**Next:** [02 · Deploy to Cloud Run](DEPLOY.md). It tells you when to configure OAuth before deployment.
