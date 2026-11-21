# Arquitetura

![Arquitetura do Google Ads MCP](assets/architecture.svg)

Este guia descreve uma imagem construída a partir do repositório oficial [`googleads/google-ads-mcp`](https://github.com/googleads/google-ads-mcp), fixado no commit [`44ca7770519362c8f334875477e1ceb499f8d2dd`](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd) para esta revisão técnica de 21 de novembro de 2026. Esse commit declara a versão `0.0.6`; atualize o pin e reavalie configuração, autenticação e ferramentas antes de usar outro commit.

## Componentes

| Componente | Função e limite |
| --- | --- |
| Google Ads MCP | Servidor oficial. Com Client ID e Client Secret configurados, inicia Streamable HTTP e autentica usuários por OAuth do Google. |
| Cloud Run | Mantém o serviço HTTP acessível ao cliente MCP. A política IAM do Cloud Run controla quem pode invocar o serviço; ela não concede acesso a contas do Google Ads. |
| Google OAuth | Faz o usuário entrar e autorizar o escopo `https://www.googleapis.com/auth/adwords`. O proxy FastMCP usa uma credencial Web fixa do aplicativo e encaminha o retorno ao cliente MCP. |
| Google Ads API | O acesso depende do projeto Google Cloud dono das credenciais OAuth, do nível de acesso aprovado para esse projeto e das permissões da conta Google Ads do usuário. |
| Firestore | Persiste estado de OAuth entre instâncias e reinicializações. A imagem precisa ser construída com o extra `firestore` e a conta de serviço do Cloud Run precisa de acesso ao banco. |
| Secret Manager | Fornece três segredos à revisão do Cloud Run: Client Secret OAuth, chave de assinatura JWT e chave de armazenamento OAuth. Neste roteiro, a chave de armazenamento é independente da chave JWT. |
| Cloud Build e Artifact Registry | Constroem e armazenam a imagem. Não participam de cada consulta. |
| Cloud Logging | Recebe os logs de operação e os eventos de auditoria estruturados do servidor. Ainda assim, limite quem pode ler os logs. |

## Fluxo de implantação

A implantação parte do commit oficial fixado, passa pelo Cloud Build e pelo Artifact Registry e termina em uma revisão do Cloud Run.

Registre o commit de origem e o digest da imagem implantada. A tag do contêiner, sozinha, não identifica de forma imutável o código executado.

## Fluxo de autenticação e consulta

1. O cliente MCP acessa `https://SEU-SERVICO.run.app/mcp` e descobre que o recurso exige OAuth.
2. O cliente completa OAuth com o servidor FastMCP. O proxy registra dinamicamente o cliente MCP e encaminha o usuário ao Google; não se cadastra o callback local de cada cliente no console Google.
3. A credencial OAuth Web do servidor retorna para `https://SEU-SERVICO.run.app/auth/callback`. Esse é o callback do Google para o proxy FastMCP; `/mcp` é o endpoint MCP e não faz parte do callback.
4. Após autorização, o cliente envia `tools/list` e `tools/call` pelo transporte Streamable HTTP em `/mcp`.
5. A ferramenta `search_search` consulta dados autorizados usando GAQL; `customers_list_accessible_customers` e `metadata_get_resource_metadata` ajudam a descobrir contas e campos.

O `GOOGLE_ADS_MCP_BASE_URL` deve ser a origem HTTPS pública do serviço, sem o sufixo `/mcp`. Com o provedor `GoogleProvider` deste commit, o caminho de retorno padrão é `/auth/callback`.

## Limites de acesso

- **Acesso à entrada Cloud Run:** `--allow-unauthenticated` deixa o serviço alcançável pela internet para que o fluxo OAuth e clientes MCP possam iniciar a conexão. Isso não autentica o usuário nem concede acesso ao Google Ads. O endpoint público ainda pode receber tráfego anônimo e gerar custos.
- **Login do aplicativo:** o usuário precisa concluir OAuth e autorizar os escopos mostrados pelo Google. O Client Secret do servidor não deve ser colocado na configuração do cliente MCP.
- **Acesso ao Google Ads:** o usuário OAuth precisa ter acesso à conta. A função de usuário do Google Ads controla o nível efetivo; a API não possui escopo OAuth separado para somente leitura. O projeto que contém o Client ID precisa ter o Google Ads API habilitado e o nível de acesso apropriado para os dados pretendidos. Implantar no Cloud Run não aprova esse acesso.
- **Ferramentas de leitura:** o arquivo `tools_config.yaml` desta implantação deve habilitar apenas `customers`, `search` e `metadata`, e desabilitar `labels` e `assets`. A configuração de ferramentas não altera o escopo OAuth nem substitui permissões de conta.
- **Armazenamento:** Firestore mantém estado OAuth, não o estado de sessão HTTP em memória, transmissões SSE abertas nem assinaturas MCP. Após reinicialização, o cliente pode precisar reconectar e inicializar uma nova sessão.

O Google encerrou tokens de desenvolvedor em 9 de setembro de 2026. Para novos projetos, o acesso à Google Ads API é concedido ao projeto Cloud associado às credenciais OAuth; não é necessário configurar um token de desenvolvedor. Confira o nível de acesso vigente no console antes de consultar contas de produção: [política oficial de tokens de desenvolvedor](https://developers.google.com/google-ads/api/docs/api-policy/developer-token) e [modelo de acesso do Google Ads](https://developers.google.com/google-ads/api/docs/oauth/access-model).

## Estado e escala no Cloud Run

O servidor usa Streamable HTTP com estado por padrão. Não configure `stateless_http`: o upstream documenta interoperabilidade tanto com clientes que usam `Mcp-Session-Id` e GET/SSE quanto com clientes que usam POST sem sessão e `subscriptions/listen`. O armazenamento Firestore guarda estado OAuth; ele não torna sessões MCP nem transmissões contínuas duráveis.

Com `min-instances=0`, o Cloud Run pode encerrar instâncias ociosas. Isso economiza instâncias aquecidas, mas aumenta a latência de início e interrompe estado de sessão em memória quando uma instância encerra. `min-instances=1` pode reduzir inicialização fria, mas aumenta o custo e também não impede reinicializações. A afinidade de sessão do Cloud Run é de melhor esforço, não uma garantia de que todas as solicitações cheguem à mesma instância. Para esta implantação de avaliação, limite a uma instância e reconecte o cliente após reinícios; não trate essa configuração como alta disponibilidade.

## Fontes primárias

- [Google Ads MCP — commit revisado](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd), em particular [`README.md`](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/README.md), [`ads_mcp/coordinator.py`](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/ads_mcp/coordinator.py) e [`ads_mcp/auth_storage.py`](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/ads_mcp/auth_storage.py).
- [FastMCP OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy) — callback padrão e encaminhamento dinâmico dos callbacks de clientes MCP.
- [Cloud Run: afinidade de sessão](https://docs.cloud.google.com/run/docs/configuring/session-affinity) e [instâncias mínimas](https://docs.cloud.google.com/run/docs/configuring/min-instances).
- [Google Ads API: OAuth e modelo de acesso](https://developers.google.com/google-ads/api/docs/oauth/access-model) e [fim dos tokens de desenvolvedor](https://developers.google.com/google-ads/api/docs/api-policy/developer-token).

Próximo: [Implantação](getting-started/DEPLOY.md).
