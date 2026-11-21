---
title: Arquitetura · resumo experimental
description: Componentes no fluxo de publicação e consulta.
---

Este é apenas um mapa breve. Consulte a [arquitetura canônica](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/ARCHITECTURE.md) para detalhes.

**Publicação:** commit fixado do servidor oficial → Cloud Build → Artifact Registry → Cloud Run.

**Consulta:** cliente MCP → HTTPS `/mcp` no Cloud Run → servidor Google Ads MCP → Google Ads API.

O login OAuth identifica a pessoa que autorizou o acesso. A conta de serviço do Cloud Run é outra identidade: ela acessa os recursos Cloud necessários, como Secret Manager e Firestore. O nível de acesso da API no projeto e as permissões da pessoa nas contas Ads também são gates separados.
