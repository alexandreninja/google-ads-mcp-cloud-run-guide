---
title: Pré-requisitos · resumo experimental
description: Confira os acessos antes de iniciar a implantação.
---

Este portal resume os passos; siga o [guia completo de pré-requisitos](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/getting-started/PREREQUISITES.md) antes de executar comandos.

- Projeto Google Cloud aprovado pela organização e com faturamento habilitado.
- Permissões para habilitar APIs e criar os recursos do tutorial, ou apoio de uma pessoa administradora.
- Google Ads API habilitada e acesso ao ambiente pretendido. A habilitação de teste e o acesso a contas de produção são gates distintos.
- Conta Google que pode acessar a conta de anúncios usada para validar.
- Cliente OAuth e cliente MCP Streamable HTTP preparados conforme o commit fixado.
- Cloud Shell Bash para o roteiro; o build é realizado no Cloud Build, não no Docker local.

O processo de acesso à Google Ads API mudou em 2026. Confira a [documentação oficial atual](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR) e o README do commit upstream antes de presumir que uma credencial antiga é necessária.

Glossário: [documento completo](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/GLOSSARY.md).
