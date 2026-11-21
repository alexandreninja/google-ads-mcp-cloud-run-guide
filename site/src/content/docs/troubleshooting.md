---
title: Validação e erros · resumo experimental
description: Alguns sinais para investigar com os guias completos.
---

Este portal não certifica a implantação. Siga a [matriz de validação canônica](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/guides/VALIDATION.md) e o [guia de troubleshooting](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/guides/TROUBLESHOOTING.md).

| Sinal | Próxima verificação |
| --- | --- |
| `redirect_uri_mismatch` | Compare o callback registrado com a URL exigida pelo servidor do commit fixado. |
| `invalid_client` | Confira o OAuth Client ID, a versão do segredo lida pelo serviço e a configuração implantada; não imprima nem cole o segredo. |
| `401` sem login | Pode ser esperado para uma solicitação anônima; não prova sucesso do OAuth. |
| `401` depois do login | Investigue a sessão OAuth, callback e logs redigidos conforme o guia completo. |
| Sem ferramentas ou contas | Confira endereço `/mcp`, versão do cliente, allowlist de ferramentas, identidade Google e permissão Ads. Uma listagem vazia não prova que não existam contas acessíveis. |
| Consulta rejeitada | Verifique nível de acesso da Google Ads API, conta, permissões, campos GAQL e quotas. |

Nunca compartilhe valores de segredos, tokens OAuth ou dados de clientes ao pedir ajuda.
