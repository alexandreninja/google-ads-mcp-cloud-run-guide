# Google Ads MCP · Cloud Run Deployment Guide

<p align="center">
  <img src="docs/assets/github-header.svg" alt="Google Ads MCP: cliente HTTP, servidor Cloud Run e Google Ads API" width="100%">
</p>

**Implante o servidor oficial [Google Ads MCP](https://github.com/googleads/google-ads-mcp) no Google Cloud Run**, com Streamable HTTP, OAuth 2.0, Secret Manager e integração à Google Ads API.

## 🧭 Documentação

| O que você precisa? | Acesse |
| --- | --- |
| Preparar o Google Cloud e o Google Ads | [Pré-requisitos](docs/getting-started/PREREQUISITES.md) |
| Construir a imagem e publicar no Cloud Run | [Implantação passo a passo](docs/getting-started/DEPLOY.md) |
| Configurar OAuth e credenciais | [Autenticação e segredos](docs/guides/OAUTH-AND-SECRETS.md) |
| Conectar um cliente e testar | [Validação](docs/guides/VALIDATION.md) |
| Resolver erros de OAuth e HTTP | [Troubleshooting](docs/guides/TROUBLESHOOTING.md) |
| Entender o desenho técnico | [Arquitetura](docs/ARCHITECTURE.md) |
| Acompanhar custos e manutenção | [Custos](docs/guides/COSTS.md) · [Operação](docs/guides/OPERATIONS.md) |
| Navegar por todos os documentos | [Índice completo](docs/README.md) |

## 🚀 Roteiro rápido

**1. Obtenha o servidor oficial e fixe uma versão.**

```bash
git clone https://github.com/googleads/google-ads-mcp.git
cd google-ads-mcp
git tag --list
# Selecione uma tag estável compatível com o guia do upstream:
# git checkout <TAG_REVISADA>
```

**2. Configure o projeto e prepare os serviços.**

```bash
export PROJECT_ID="SEU_PROJECT_ID"
export REGION="us-central1"
export SERVICE="google-ads-mcp"

gcloud config set project "$PROJECT_ID"
gcloud services enable \
  googleads.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com
```

**3. Siga a implantação.** O guia separa build, Cloud Run, OAuth, armazenamento de segredos e testes, com comandos parametrizados.

[**Abrir implantação passo a passo →**](docs/getting-started/DEPLOY.md)

## 🏗️ Arquitetura

![Fluxos de implantação e consulta do Google Ads MCP](docs/assets/architecture.svg)

```text
DEPLOY
Google Ads MCP (upstream)
    → Cloud Build
    → Artifact Registry
    → Cloud Run

CONSULTA
Cliente MCP
    ↔ Streamable HTTP + OAuth
    ↔ Google Ads MCP / Cloud Run
    ↔ Google Ads API
```

## 🧪 Verificação

O roteiro de validação cobre:

- Status do serviço e resposta HTTP;
- Autenticação OAuth;
- Descoberta de ferramentas MCP;
- Listagem de contas autorizadas;
- Consulta GAQL;
- Teste negativo sem autenticação.

[**Abrir matriz de testes →**](docs/guides/VALIDATION.md)

## 🛠️ Problemas comuns

| Erro | Onde investigar |
| --- | --- |
| `redirect_uri_mismatch` | URLs autorizadas e callback OAuth |
| `invalid_client` | Client ID, versão do segredo e configuração do serviço |
| HTTP `401` | Autenticação ausente ou recusada — pode ser esperado |
| Ferramentas não aparecem | Endpoint, versão MCP, OAuth e configuração do cliente |
| Contas não aparecem | Identidade Google e permissões Google Ads |

[**Abrir troubleshooting →**](docs/guides/TROUBLESHOOTING.md)

## 📚 Referências

- [Código oficial — googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp)
- [Documentação Google Ads API](https://developers.google.com/google-ads/api)
- [Documentação Google Cloud Run](https://cloud.google.com/run/docs)
- [Índice da documentação deste guia](docs/README.md)
