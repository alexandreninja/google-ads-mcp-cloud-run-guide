# 01 · Pré-requisitos

## Google Cloud

- Projeto com faturamento habilitado.
- Acesso ao Cloud Run, Cloud Build, Artifact Registry, Secret Manager e IAM.
- `gcloud` CLI autenticado.
- Git e terminal com Bash (exemplos deste guia).
- Permissão para habilitar a Google Ads API.

## Google Ads

- Conta Google com acesso às contas a consultar.
- Google Ads API habilitada no projeto.
- Credenciais OAuth 2.0 adequadas ao modo HTTP.
- Credenciais e permissões exigidas pela **versão oficial** do servidor.

## Preparar projeto

```bash
gcloud auth login

export PROJECT_ID="SEU_PROJECT_ID"
export REGION="us-central1"

gcloud config set project "$PROJECT_ID"
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  googleads.googleapis.com
```

> Executar builds e criar recursos pode gerar cobrança.

## Obter código

```bash
git clone https://github.com/googleads/google-ads-mcp.git
cd google-ads-mcp
git tag --list
```

Escolha e fixe a versão que será utilizada; reveja instruções e variáveis do `README.md` do upstream correspondente.

**Próximo:** [02 · Implantação](DEPLOY.md).
