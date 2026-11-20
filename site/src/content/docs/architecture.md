---
title: Arquitetura
description: Fluxos de build e de consulta.
---

## Deploy

`Google Ads MCP upstream → Cloud Build → Artifact Registry → Cloud Run`

## Consulta

`Cliente MCP ↔ Cloud Run /mcp ↔ Google Ads API`

OAuth e Secret Manager participam da autenticação e das credenciais.

[Arquitetura completa](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/ARCHITECTURE.md).
