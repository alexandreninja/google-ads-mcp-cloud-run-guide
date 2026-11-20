---
title: "Arquitetura"
description: "Transporte e hospedagem são decisões diferentes."
---

## Duas decisões

**Streamable HTTP:** para testar um servidor remoto reutilizável por clientes autorizados.

**Cloud Run:** caminho documentado, viável com Google Cloud já disponível; **não é uma imposição do MCP**.

## Dois fluxos

- **Deploy:** upstream → Cloud Build → Artifact Registry → Cloud Run.
- **Consulta:** cliente autorizado ↔ servidor MCP ↔ Google Ads API.

[Arquitetura técnica](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/ARCHITECTURE.md) · [ADRs](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/tree/main/docs/decisions).
