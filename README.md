# Google Ads MCP · Cloud Run Guide

[![Documentation](https://img.shields.io/badge/docs-GitHub%20%2B%20Starlight-5a67d8)](docs/README.md) [![Upstream](https://img.shields.io/badge/upstream-googleads%2Fgoogle--ads--mcp-4285F4)](https://github.com/googleads/google-ads-mcp) [![Security](https://img.shields.io/badge/security-review%20required-orange)](SECURITY.md)

<p align="center"><img src="docs/assets/github-header.svg" alt="Cliente MCP via Streamable HTTP, servidor Google Cloud Run e Google Ads API" width="100%"></p>

> **Um guia de implantação remota, do primeiro deploy aos erros de OAuth.**

Guia independente de estudo da implantação do **servidor oficial [Google Ads MCP](https://github.com/googleads/google-ads-mcp)** com Streamable HTTP, Google Cloud Run, OAuth 2.0, Secret Manager, Cloud Build e Artifact Registry.

**Autoria do guia:** Alexandre Carvalho Ribeiro Costa · [@alexandreninja](https://github.com/alexandreninja). **Código do servidor:** equipe do Google; não é reivindicado como implementação própria.

> [!IMPORTANT]
> Este repositório documenta uma experiência técnica, não uma distribuição modificada do servidor nem uma implantação institucional homologada. Consultas autorizadas foram validadas em clientes MCP de teste; integração corporativa no VS Code + Copilot e acesso multiusuário permanecem pendentes.

## 🧭 Comece por aqui

| Seu objetivo | Documento |
| --- | --- |
| Entender o case e seus limites | [Visão geral](docs/OVERVIEW.md) · [Escopo](docs/SCOPE.md) |
| Compreender a arquitetura | [Arquitetura](docs/ARCHITECTURE.md) · [Decisões](docs/decisions/README.md) |
| Preparar um ambiente próprio | [Pré-requisitos](docs/getting-started/PREREQUISITES.md) |
| Seguir a implantação | [Guia de deploy](docs/getting-started/DEPLOY.md) |
| Configurar autenticação | [OAuth e Secret Manager](docs/guides/OAUTH-AND-SECRETS.md) |
| Verificar o funcionamento | [Testes](docs/guides/VALIDATION.md) · [Evidências](docs/EVIDENCE.md) |
| Diagnosticar problemas | [Troubleshooting](docs/guides/TROUBLESHOOTING.md) |
| Avaliar segurança e custos | [Segurança](SECURITY.md) · [Custos](docs/guides/COSTS.md) |
| Navegar no portal de documentação | [Site Astro/Starlight](site/README.md) |

## 🎯 O que é — e o que não é

Documentação original de decisões, comandos parametrizados, validação, limitações e erros observados. **Não** é o servidor Google Ads MCP, um SaaS, um script de instalação automático ou um produto homologado. Não contém IDs de contas, projetos internos, URL privada, segredos ou dados institucionais.

## 🏗️ Arquitetura

![Diagrama dos fluxos de deploy e consulta](docs/assets/architecture.svg)

**Implantação:** código oficial → Cloud Build → Artifact Registry → Cloud Run. **Consulta:** cliente MCP autorizado ↔ servidor remoto em Cloud Run ↔ Google Ads API. **Controles de apoio:** OAuth 2.0, Secret Manager, IAM e logs.

A escolha por **Streamable HTTP** decorreu do potencial de reutilização remota; a escolha por **Cloud Run** refletiu a disponibilidade de Google Cloud institucional e o caminho documentado pelo projeto oficial. **Cloud Run não é obrigatório para hospedar MCP remoto.**

## 🚀 Caminho seguro

1. [Preparar pré-requisitos](docs/getting-started/PREREQUISITES.md) em ambiente próprio ou autorizado.
2. [Fixar e revisar a versão upstream](docs/getting-started/DEPLOY.md).
3. [Construir e publicar a imagem](docs/getting-started/DEPLOY.md).
4. [Configurar OAuth, segredos e IAM](docs/guides/OAUTH-AND-SECRETS.md).
5. [Executar validação progressiva](docs/guides/VALIDATION.md).

> [!CAUTION]
> Endpoint HTTP publicamente alcançável não significa acesso irrestrito aos dados; o fluxo deve exigir autenticação e autorização adequadas. Nunca publique credenciais, tokens, IDs institucionais ou logs de produção. Uma implantação corporativa exige revisão de segurança.

## 🔬 Evidências e limites

| Item | Situação |
| --- | --- |
| Servidor MCP remoto | Implantado e testado |
| Consulta a contas Google Ads | Validada em clientes MCP de teste |
| `redirect_uri_mismatch` | Corrigido com URLs de callback autorizadas |
| `invalid_client` | Resolvido após revisão/atualização do segredo |
| HTTP `401` sem autenticação | Comportamento esperado no teste negativo |
| VS Code + Copilot institucional | Ainda não validado de ponta a ponta |
| Acesso por múltiplos colaboradores | Possibilidade futura, não homologada |
| Economia frente a plataformas gerenciadas | Não comprovada; TCO não calculado |

## 📚 Aprenda, implemente e opere

**Aprender:** [Visão geral](docs/OVERVIEW.md) · [Transportes MCP](docs/concepts/MCP-TRANSPORTS.md) · [ADRs](docs/decisions/README.md).

**Implementar:** [Pré-requisitos](docs/getting-started/PREREQUISITES.md) · [Deploy](docs/getting-started/DEPLOY.md) · [OAuth](docs/guides/OAUTH-AND-SECRETS.md) · [Validação](docs/guides/VALIDATION.md).

**Operar:** [Segurança](SECURITY.md) · [Troubleshooting](docs/guides/TROUBLESHOOTING.md) · [Custos](docs/guides/COSTS.md) · [Checklist](docs/guides/OPERATIONS.md).

## 🔗 Artigo e código oficial

- **Artigo técnico no LinkedIn:** link a inserir após publicação — motivações, arquitetura e aprendizados.
- **Este guia:** como estudar, configurar, validar e diagnosticar a implantação.
- **Servidor oficial:** https://github.com/googleads/google-ads-mcp.

## 📄 Licença e atribuição

Documentação e diagramas originais deste guia: [CC BY 4.0](LICENSE). A licença do software do Google permanece no repositório upstream.
