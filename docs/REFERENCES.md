# Referências

Esta lista prioriza documentação dos mantenedores das ferramentas e serviços usados no guia. Os links abaixo foram abertos ou consultados em **21 de novembro de 2026**. As páginas do Google Cloud e do Google for Developers são documentação viva e não têm uma versão única aplicável a todos os comandos; consulte nelas a versão indicada pela própria página.

## Servidor Google Ads MCP e versão

| Fonte | Versão ou data conferida | Uso no guia |
| --- | --- | --- |
| [Repositório oficial `googleads/google-ads-mcp`](https://github.com/googleads/google-ads-mcp) | Verificado em 2026-11-21. Fixe uma tag/commit no roteiro de implantação; não use `main` como referência reproduzível. | Código e README do servidor que será construído. Variáveis, callbacks OAuth e ferramentas dependem da versão. |
| [Release oficial `v0.0.6`](https://github.com/googleads/google-ads-mcp/releases/tag/v0.0.6) | Publicada em 2026-11-02, commit `7452a9d`; era a release marcada como mais recente em 2026-11-21. | Release publicada pelo upstream, separada do commit auditado que o roteiro usa. |
| [Commit upstream auditado pelo roteiro](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd) | `44ca7770519362c8f334875477e1ceb499f8d2dd`; revisado em 2026-11-21. O pacote declara versão `0.0.6`, mas este commit não é o commit da release tagueada `v0.0.6`. | Baseline exato usado pelos comandos em `docs/getting-started/DEPLOY.md` e registrado em `config/upstream.json`. Não o apresente como release estável. |
| [Licença do servidor upstream](https://github.com/googleads/google-ads-mcp/blob/7452a9d/LICENSE) | Apache License 2.0 no commit `7452a9d`; conferida em 2026-11-21. | Licença do código do servidor oficial; não licencia automaticamente este repositório ou conteúdo de terceiros. |

## Google Ads API e autorização

| Fonte | Estado na verificação | Uso no guia |
| --- | --- | --- |
| [Google Ads API](https://developers.google.com/google-ads/api?hl=pt-BR) | Documentação viva; consultada em 2026-11-21. | Visão geral e documentação da API. |
| [Mudanças no token de desenvolvedor e no gerenciamento de acesso](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR) | Consultada em 2026-11-21. A página informa que tokens de desenvolvedor foram desativados em 2026-09-09; novos níveis de acesso são gerenciados no projeto Google Cloud. | Fonte normativa para diferenciar ativação da API, acesso de teste e autorização para uso com contas de produção. Não use tutoriais antigos de token como procedimento atual. |
| [Como usar OAuth 2.0 em aplicativos de servidor da Web](https://developers.google.com/identity/protocols/oauth2/web-server?hl=pt-BR) | Documentação viva; consultada em 2026-11-21. | Fluxo OAuth web e exigência de correspondência exata da URI de redirecionamento. O callback do MCP deve vir da versão upstream usada. |
| [Configurar a tela de permissão OAuth e escolher escopos](https://developers.google.com/workspace/guides/configure-oauth-consent?hl=pt-br) | Documentação viva; consultada em 2026-11-21. | Conceitos de consentimento e escopos. Não substitui instruções específicas do servidor Google Ads MCP. |
| [Configurar autenticação para servidores MCP do Google e do Google Cloud](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers) | Documentação viva; consultada em 2026-11-21. | Referência para localizar Google Auth Platform e entender cadastro de uma URI; descreve servidores MCP do Google Cloud, não a configuração de OAuth do Google Ads MCP. |

## Google Cloud: projeto, build e execução

| Fonte | Versão/idioma conferidos | Uso no guia |
| --- | --- | --- |
| [Criar projetos](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=pt-BR) | Página oficial em pt-BR; consultada em 2026-11-21. | Projeto e permissões de criação. |
| [Ativar, desativar ou alterar o faturamento de um projeto](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=pt-BR) | Página oficial em pt-BR; consultada em 2026-11-21. | Vínculo de projeto a uma conta Cloud Billing ativa. |
| [Iniciar o Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell?hl=pt-BR) | Página oficial em pt-BR; consultada em 2026-11-21. | Abrir Cloud Shell no Console do Google Cloud. |
| [Primeiros passos com o Cloud Shell e o gcloud](https://codelabs.developers.google.com/codelabs/cloud-shell?hl=pt-br) | Codelab oficial em pt-BR; atualizado em 2026-03-20 e consultado em 2026-11-21. | Preparar projeto, ativar faturamento, iniciar Cloud Shell e conferir conta/projeto. É material interativo em texto. |
| [O guia definitivo do Cloud Run](https://codelabs.developers.google.com/next26/ultimate-cloud-run-guide?hl=pt-br) | Codelab oficial em pt-BR; consultado em 2026-11-21. | Exemplo separado de implantação por imagem e fonte, Cloud Shell, Artifact Registry e Secret Manager. Não reproduz a arquitetura Google Ads MCP deste repositório. |
| [Documentação do Cloud Run](https://docs.cloud.google.com/run/docs?hl=pt-BR) | Documentação viva em pt-BR; consultada em 2026-11-21. | Configuração e operação do serviço. |
| [Implantar no Cloud Run usando o Cloud Build](https://docs.cloud.google.com/build/docs/deploying-builds/deploy-cloud-run?hl=pt-BR) | Página em pt-BR; a versão aberta indicava última atualização em 2026-11-11 UTC. | Exemplo oficial de build e implantação; os comandos do guia podem usar outro caminho de build. |
| [Enviar um build pela CLI ou API](https://docs.cloud.google.com/build/docs/running-builds/submit-build-via-cli-api) | Documentação viva; consultada em 2026-11-21. | `gcloud builds submit` envia a origem para Cloud Storage; confira a identidade que envia e as permissões do bucket de staging. |
| [Executar builds com uma conta de serviço gerenciada pelo usuário](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts?hl=en) | Documentação viva; consultada em 2026-11-21. | Papéis exigidos pela identidade de build e requisito `iam.serviceAccounts.actAs` para quem submete build com uma conta indicada. |
| [Papéis IAM do Cloud Run](https://docs.cloud.google.com/run/docs/reference/iam/roles) | Documentação viva; consultada em 2026-11-21. | Permissões do implantador para publicar imagem, selecionar identidade de execução e implantar serviço. |
| [Armazenar artefatos no Artifact Registry](https://docs.cloud.google.com/build/docs/building/store-artifacts-in-artifact-registry?hl=pt-br) | Página oficial em pt-BR; consultada em 2026-11-21. | Publicação de artefatos e permissões entre Cloud Build e Artifact Registry. |
| [Guia de início rápido do Artifact Registry para imagens Docker](https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images?hl=pt-BR) | Página oficial em pt-BR; consultada em 2026-11-21. | Criar repositório e armazenar imagem de contêiner. |
| [Criar e acessar um segredo com Secret Manager](https://docs.cloud.google.com/secret-manager/docs/create-secret-quickstart?hl=pt-br) | Página oficial em pt-BR; consultada em 2026-11-21. | Criar segredos e adicionar versões. |
| [Configurar segredos para serviços do Cloud Run](https://docs.cloud.google.com/run/docs/configuring/services/secrets?hl=pt-BR) | Página oficial em pt-BR; consultada em 2026-11-21. | Vincular segredos a revisões do serviço; conferir acesso e estratégia de versão. |
| [Registros do Cloud Run](https://docs.cloud.google.com/run/docs/logging?hl=pt-br) | Página oficial em pt-BR; consultada em 2026-11-21. | Ver registros do contêiner e localizar a primeira falha de inicialização ou solicitação. |

## Protocolo MCP

- [Especificação do Model Context Protocol, revisão 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28): revisão publicada em **28 de julho de 2026**. Clientes e servidores também podem falar revisões anteriores; confira o suporte da versão upstream e do cliente usados no tutorial.
- [Registro de releases do Google Ads MCP](https://github.com/googleads/google-ads-mcp/releases): use a release fixada para descobrir o transporte, endpoint, variáveis e configuração de ferramentas realmente fornecidos pelo servidor.

## Cliente ChatGPT (quando usado para validação)

- [Conectar servidores MCP personalizados no ChatGPT](https://help.openai.com/pt-br/articles/12584461-connecting-custom-mcp-servers-in-chatgpt): Help Center oficial; consultado em 2026-11-21, indicado como atualizado 24 dias antes. A página em português é tradução automática. Descreve a interface atual Plugins → adicionar servidor MCP personalizado e disponibilidade/políticas por plano. O fluxo dessa interface é específico do ChatGPT e não substitui o README do Google Ads MCP.

## Licenças e atribuição

O código do servidor oficial está sob Apache 2.0. A licença do conteúdo original deste repositório está indicada em [LICENSE](../LICENSE). Documentação do Google Developers consultada nesta página indica CC BY 4.0 para conteúdo, salvo indicação diferente, e Apache 2.0 para exemplos de código; confira o rodapé da página-fonte antes de copiar ou adaptar trechos. Os links não transferem nem alteram licenças de upstream, documentação, vídeos, marcas ou outros materiais externos.

Para sugestões de correção ou novas fontes, veja [Como contribuir](../CONTRIBUTING.md). Vídeos em português examinados e suas limitações estão em [Vídeos em português](guides/VIDEOS-PT-BR.md).

## Clientes e implementação deste roteiro

- [MCP no VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers): formato de configuração específico do cliente.
- [MCP no Codex](https://developers.openai.com/codex/mcp): conexão HTTP e OAuth; a ajuda da CLI instalada também foi inspecionada nesta revisão.
- [GoogleProvider do FastMCP](https://gofastmcp.com/docs/integrations/google): callback padrão e fluxo OAuth web.
- [Criar banco Firestore](https://docs.cloud.google.com/sdk/gcloud/reference/firestore/databases/create): parâmetros Standard/Native usados pelo guia.
