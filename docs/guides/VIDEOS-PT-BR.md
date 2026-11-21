# Vídeos em português para aprofundar

Esta lista oferece contexto visual para quem está começando. Os vídeos são **complementos conceituais**: não reproduzem todos os comandos deste guia, não implantam o Google Ads MCP e não substituem as instruções da versão upstream fixada. Telas, nomes de menus, preços e requisitos mudam; use a documentação oficial atual para os passos operacionais.

Os metadados de título, idioma, assunto, canal e data de publicação abaixo foram conferidos em **21 de novembro de 2026**. Os vídeos **não foram assistidos integralmente**; a verificação não confirma que cada demonstração ou passo mostrado ainda funcione. Quando não encontrei um vídeo em português que pudesse recomendar com segurança, registro a lacuna e indico documentação oficial. Uma busca complementar leva a resultados ainda não revisados; não deve ser tratada como uma recomendação de vídeo.

## Projeto, faturamento e Cloud Shell

### Vídeo de apoio (metadados conferidos): faturamento

[Administração de faturamento no Google Cloud](https://www.youtube.com/watch?v=QKitTPX9yrU) · Google Cloud LATAM · publicado em **29 de julho de 2024** · em português.

A descrição cobre conceitos e funções de administração de faturamento, alertas e opções de otimização de custos. O canal Google Cloud LATAM está verificado no YouTube. O vídeo **não** é um passo a passo para criar um projeto, vinculá-lo a uma conta de faturamento ou abrir o Cloud Shell.

Para essas etapas, use os guias oficiais atuais:

- [Criar projetos do Google Cloud](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=pt-BR)
- [Ativar, desativar ou alterar o faturamento de um projeto](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=pt-BR)
- [Iniciar o Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell?hl=pt-BR)
- [Primeiros passos com o Cloud Shell e o gcloud](https://codelabs.developers.google.com/codelabs/cloud-shell?hl=pt-br) — codelab oficial em português; cobre projeto, faturamento, abrir o Shell e confirmar conta/projeto. É texto interativo, não vídeo.

Não encontrei um vídeo em português que trate, em conjunto e com instruções atuais, da criação do projeto, do vínculo de faturamento e do Cloud Shell. Para uma sequência prática oficial em texto, use o codelab acima e confirme as permissões com os [pré-requisitos deste guia](../getting-started/PREREQUISITES.md).

## Cloud Run, Cloud Build e Artifact Registry

### Vídeo de apoio (metadados conferidos): visão geral de CI/CD

[Implantação de CI/CD no Google Cloud](https://www.youtube.com/watch?v=K4jI5ZgS95E) · Google Cloud LATAM · publicado em **25 de julho de 2024** · em português.

A descrição apresenta CI/CD, pipelines a partir do código-fonte, Cloud Build e uma demonstração no Console do Google Cloud; também aponta para Cloud Run. O canal está verificado no YouTube. É uma introdução ao fluxo, **não** uma gravação dos comandos deste repositório nem um tutorial específico de Artifact Registry ou do Google Ads MCP.

Para seguir o procedimento deste guia e conferir permissões, comandos e formatos atuais, consulte:

- [O guia definitivo do Cloud Run, do zero ao tutorial de demonstração de produção](https://codelabs.developers.google.com/next26/ultimate-cloud-run-guide?hl=pt-br) — codelab oficial em pt-BR com projeto/faturamento, Cloud Shell, implantação por imagem e por código-fonte, Artifact Registry e Secret Manager. É um exemplo separado, não reproduz as contas de serviço, banco, configuração de ferramentas e fluxo OAuth do Google Ads MCP deste repositório.
- [Como criar e enviar imagens com o Cloud Build](https://docs.cloud.google.com/build/docs/deploying-builds/deploy-cloud-run?hl=pt-BR)
- [Armazenar artefatos no Artifact Registry](https://docs.cloud.google.com/build/docs/building/store-artifacts-in-artifact-registry?hl=pt-br)
- [Guia de início rápido do Artifact Registry para imagens Docker](https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images?hl=pt-BR)
- [Documentação do Cloud Run](https://docs.cloud.google.com/run/docs?hl=pt-BR)

### Vídeo de apoio (metadados conferidos): deploy com Docker

[Hands-on: Deploy de aplicação com Docker no Google Cloud Run](https://www.youtube.com/watch?v=QcXw0VEL_U8) · The Cloud Bootcamp - Português · publicado em **13 de setembro de 2022** · em português.

A descrição apresenta um hands-on de modernização de uma aplicação para contêiner Docker e implantação no Cloud Run. É o material mais próximo de uma demonstração de deploy em português que encontrei, mas é antigo: use-o para visualizar a ideia de contêiner e serviço, não para copiar telas, comandos, permissões ou fluxo de publicação atual. O canal tem foco em formação de nuvem/DevOps; os metadados públicos foram conferidos, mas o vídeo não foi assistido integralmente.

## Google Auth Platform, OAuth e Secret Manager

Não encontrei um vídeo em português que cubra a interface atual da Google Auth Platform, a criação de um cliente OAuth web, o callback específico do servidor MCP e o acesso a segredos pelo Cloud Run. Tutoriais de OAuth para outros produtos (por exemplo, YouTube Data API, n8n ou Apps Script) usam fluxos, escopos e callbacks diferentes e não devem ser copiados para esta implantação.

Use estas fontes oficiais atuais e confira o callback exigido pela versão upstream escolhida:

- [Como usar OAuth 2.0 em aplicativos de servidor da Web](https://developers.google.com/identity/protocols/oauth2/web-server?hl=pt-BR) — explica o fluxo web e que a URI de redirecionamento precisa corresponder exatamente à URI autorizada.
- [Configurar autenticação para servidores MCP do Google e do Google Cloud](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers) — mostra onde fica **Google Auth Platform → Clients** no Console e como cadastrar uma URI de redirecionamento. Esse tutorial configura os MCPs do Google Cloud descritos naquela página; use-o só como referência de navegação, não copie seu cliente, escopos ou callback para o Google Ads MCP.
- [Configurar a tela de permissão OAuth e escolher escopos](https://developers.google.com/workspace/guides/configure-oauth-consent?hl=pt-br) — conceitos de consentimento e escopos; não documenta a configuração específica do Google Ads MCP.
- [Criar e acessar um segredo usando o Secret Manager](https://docs.cloud.google.com/secret-manager/docs/create-secret-quickstart?hl=pt-br)
- [Configurar segredos para serviços do Cloud Run](https://docs.cloud.google.com/run/docs/configuring/services/secrets?hl=pt-BR) — configuração atual de segredos e criação de revisões no Cloud Run.

## Google Ads API e acesso ao projeto

Não encontrei um vídeo em português que explique a experiência atual de acesso à Google Ads API. Vídeos antigos sobre solicitar ou usar um token de desenvolvedor não representam o processo atual: esses tokens foram desativados em **9 de setembro de 2026**. Hoje, o acesso é associado ao projeto Google Cloud que emitiu as credenciais OAuth; acesso de teste e acesso a contas de produção são níveis distintos.

Leia a página oficial atual antes de solicitar acesso ou interpretar um erro:

- [Token de desenvolvedor e mudanças no acesso à Google Ads API](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR) — a documentação explica a migração, o acesso pelo projeto Cloud e por que a Central de APIs não deve ser usada para novas solicitações.
- [Repositório oficial do Google Ads MCP](https://github.com/googleads/google-ads-mcp) — confira o README da tag/commit que o guia fixar; configuração e ferramentas variam por versão.

## Buscas complementares não revisadas

Os links abaixo são **páginas de resultados de busca, não vídeos validados**. Use-os somente se quiser pesquisar outros materiais; verifique autor, data, idioma e se a interface ainda existe antes de seguir qualquer passo.

- [Buscar vídeos sobre projeto, faturamento e Cloud Shell](https://www.youtube.com/results?search_query=Google+Cloud+criar+projeto+faturamento+Cloud+Shell+portugu%C3%AAs)
- [Buscar vídeos sobre Cloud Run, Cloud Build e Artifact Registry](https://www.youtube.com/results?search_query=Google+Cloud+Run+Cloud+Build+Artifact+Registry+portugu%C3%AAs)
- [Buscar vídeos sobre OAuth e Secret Manager](https://www.youtube.com/results?search_query=Google+Auth+Platform+OAuth+Secret+Manager+Cloud+Run+portugu%C3%AAs)
- [Buscar vídeos sobre acesso atual à Google Ads API](https://www.youtube.com/results?search_query=Google+Ads+API+acesso+projeto+Google+Cloud+2026+portugu%C3%AAs)

---

**Verificação de fontes:** 21 de novembro de 2026. As páginas de documentação do Google são conteúdo vivo, sem versão fixa; esta data registra quando os links e as orientações foram conferidos. Os dados dos vídeos vêm dos metadados/listagens do YouTube; o conteúdo integral dos vídeos não foi verificado.
