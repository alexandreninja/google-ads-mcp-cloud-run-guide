# Vídeos em português para aprofundar

Escolha o assunto em que precisa de apoio visual e depois retome o checkpoint do guia. Os três vídeos abaixo ajudam a entender a nuvem; o passo a passo específico do Google Ads MCP está na [implantação](../getting-started/DEPLOY.md).

> [!NOTE]
> Títulos, canais, idioma, assunto e datas foram conferidos em **21 de novembro de 2026** pelos metadados públicos. Os vídeos não foram assistidos integralmente. Para comandos, permissões e telas atuais, siga este guia e as fontes oficiais.

## Para assistir

| Assunto | Vídeo em português | O que observar |
| --- | --- | --- |
| Faturamento | [Administração de faturamento no Google Cloud](https://www.youtube.com/watch?v=QKitTPX9yrU) — Google Cloud LATAM, 29/07/2024 | Funções de administração, alertas e custos. Para criar e vincular o projeto, use os exercícios abaixo. |
| Código até a nuvem | [Implantação de CI/CD no Google Cloud](https://www.youtube.com/watch?v=K4jI5ZgS95E) — Google Cloud LATAM, 25/07/2024 | Visão geral de pipelines, Cloud Build e demonstração no Console. |
| Contêiner e deploy | [Hands-on: Deploy de aplicação com Docker no Google Cloud Run](https://www.youtube.com/watch?v=QcXw0VEL_U8) — The Cloud Bootcamp - Português, 13/09/2022 | Demonstração histórica para visualizar imagem e serviço. A interface e os comandos de 2022 podem estar desatualizados. |

## Para acompanhar fazendo

Estes **exercícios oficiais em português são textos interativos**, não vídeos:

- [Cloud Shell e gcloud](https://codelabs.developers.google.com/codelabs/cloud-shell?hl=pt-br): projeto, faturamento, abertura do terminal e conferência da conta.
- [Cloud Run, do zero à demonstração](https://codelabs.developers.google.com/next26/ultimate-cloud-run-guide?hl=pt-br): imagem, implantação, Artifact Registry e Secret Manager. É um exemplo separado; ao voltar, use a configuração MCP deste repositório.

## OAuth e acesso à API: siga a documentação atual

Não foi encontrado um vídeo em português que cubra o fluxo atual completo de OAuth deste servidor ou o novo acesso à Google Ads API. Para essas etapas, use:

| Preciso entender… | Fonte e próximo passo |
| --- | --- |
| Cliente web e retorno do login | [OAuth 2.0 para servidores web](https://developers.google.com/identity/protocols/oauth2/web-server?hl=pt-BR) → [OAuth deste guia](OAUTH-AND-SECRETS.md) |
| Credenciais fora do código | [Criar um segredo](https://docs.cloud.google.com/secret-manager/docs/create-secret-quickstart?hl=pt-br) · [Usar segredos no Cloud Run](https://docs.cloud.google.com/run/docs/configuring/services/secrets?hl=pt-BR) |
| Acesso de teste ou produção à API | [Níveis de acesso atuais](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR) → [Pré-requisitos](../getting-started/PREREQUISITES.md) |

> [!IMPORTANT]
> Tutoriais antigos de developer token seguem o modelo anterior, encerrado em 09/09/2026. Tutoriais de OAuth de outros produtos também podem usar callbacks e escopos diferentes. Confira os requisitos do [servidor oficial](https://github.com/googleads/google-ads-mcp) na versão fixada pelo guia.

[← Índice](../README.md) · [Glossário](../GLOSSARY.md)
