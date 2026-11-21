---
title: Implantação · resumo experimental
description: Roteiro resumido para publicar o servidor no Cloud Run.
---

Este resumo não substitui o [guia canônico de implantação](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/getting-started/DEPLOY.md). Use os comandos e checkpoints daquele documento.

O roteiro canônico usa Cloud Shell, fixa um commit do servidor oficial, limita as ferramentas configuradas, constrói a imagem com Cloud Build e publica uma revisão no Cloud Run. O perfil do baseline habilita `customers`, `search` e `metadata`, e desabilita `labels` e `assets`. Antes da publicação, o guia pausa para OAuth, segredos no Secret Manager e persistência do estado OAuth. Cloud Build, Firestore, Artifact Registry, Cloud Run, logs e tráfego podem gerar custos.

Antes de conectar uma conta de anúncios, confirme que a configuração de ferramentas foi aplicada à imagem da versão fixada. OAuth autentica a pessoa; não altera o escopo de autorização nem substitui as permissões Google Ads.

Referências completas: [OAuth e Secret Manager](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/guides/OAUTH-AND-SECRETS.md) · [custos](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/guides/COSTS.md) · [operação](https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide/blob/main/docs/guides/OPERATIONS.md).
