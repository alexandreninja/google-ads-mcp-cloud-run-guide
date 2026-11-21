---
title: OAuth e segurança · resumo experimental
description: Conceitos de autenticação e controle de acesso.
---

Este resumo não contém os passos completos. Use o [guia canônico de OAuth e Secret Manager](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/guides/OAUTH-AND-SECRETS.md) junto com o commit upstream fixado.

- O OAuth Client ID identifica a aplicação; o Client Secret é confidencial e deve ser lido do Secret Manager.
- Cadastre a URL de callback exigida pelo servidor fixado. O cliente MCP e o servidor participam de etapas diferentes do fluxo OAuth; não cadastre uma URL do cliente como callback do servidor sem instrução explícita do guia.
- `--allow-unauthenticated` controla se a camada de entrada do Cloud Run aceita solicitações HTTP. Não substitui o login e a autorização OAuth da aplicação.
- IAM do Google Cloud, identidade OAuth do usuário, acesso à Google Ads API e permissões do usuário nas contas de anúncios são controles distintos.
- O perfil deste baseline permite somente `customers`, `search` e `metadata`; `labels` e `assets` ficam desabilitadas. OAuth não define a lista de ferramentas nem reduz o escopo do consentimento Google.

Nunca cole segredos em prompts, documentação, capturas de tela ou logs. Consulte também as [orientações completas de segurança](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/SECURITY.md).
