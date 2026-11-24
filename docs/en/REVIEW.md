# Guide checks · November 21, 2026

This record describes the scope and evidence of the documentation review. The server reference is commit `44ca7770519362c8f334875477e1ceb499f8d2dd`, recorded in [upstream.json](../../config/upstream.json).

## Changes in this round

- An opening connected to *Construir ou integrar?*, navigation by goal, and technical detail introduced as needed.
- Cost, credential, and configuration alerts placed at the relevant steps, with equivalent examples in Portuguese and English.
- Operator permissions for monitoring builds, uploading source, and reading images made explicit in deployment.
- Source preparation requires the official repository, pinned commit, and a clean checkout before writing any files.
- Validation covers data granularity, currency, time zone, and conversion from micros using code.

## Local checks

| Check | Coverage |
| --- | --- |
| `check_docs.py` | Local links and anchors, JSON, and Bash/Python syntax; no Cloud commands executed |
| `check_translations.py` | Equivalent executable examples across PT/EN documents |
| Helper tests | Temporary Git repositories: origin, commit, local changes, and image preparation |
| Upstream parser | Acceptance of the `customers`, `search`, and `metadata` profile, with `labels` and `assets` disabled |
| Build inspection | Firestore extra, parameterized image, and Cloud Logging output |
| `git diff --check` | Whitespace errors in the diff |

The checks above passed in this round. The helper tests ran **11 cases using real temporary Git repositories**. A heuristic scan of text content found no credential patterns; this does not replace a security review of the target environment.

To repeat the automated checks from the repository root:

~~~bash
python3 scripts/check_docs.py
python3 scripts/check_translations.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
git diff --check
~~~

## Evidence limits

> [!NOTE]
> This review did not run a new container build, Google Cloud deployment, live OAuth flow, or query against Google Ads accounts. Local checks assess the material and source preparation; deployment checkpoints must be run in the target environment.

The [validation matrix](guides/VALIDATION.md) explains how to record the build, revision, sign-in, tools, and query. Supplementary videos had their metadata checked, without a full content review. The `site/` scaffold remains experimental.

[Português](../REVIEW.md) · [Index](README.md)

## Additional evidence · November 24, 2026

The [migration experiment](guides/OAUTH-PERSISTENCE.md) used a different upstream commit of package 0.0.6. The review above remains a historical record of November 21. Access continuity across revisions was observed; post-expiry renewal and actual cost remain unverified. Automated checks for the documentation update must run before publication.
