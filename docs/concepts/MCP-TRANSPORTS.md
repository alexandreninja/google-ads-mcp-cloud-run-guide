# STDIO e Streamable HTTP

| | STDIO | Streamable HTTP |
| --- | --- | --- |
| Execução | Processo local iniciado pelo cliente | Serviço HTTP acessado por HTTPS |
| Transporte MCP | Entrada e saída do processo | `POST` no endpoint `/mcp`, com respostas HTTP e, quando usadas, transmissões SSE |
| Identidade no exemplo oficial | Application Default Credentials (ADC) locais | OAuth do Google encaminhado pelo proxy FastMCP |
| Estado | Estado do processo local | Pode incluir sessão MCP em memória e estado OAuth persistido separadamente |
| Uso típico | Desenvolvimento local e uso individual | Cliente remoto ou contêiner separado |

## Streamable HTTP neste guia

No commit oficial [`44ca7770519362c8f334875477e1ceb499f8d2dd`](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd), definir `GOOGLE_ADS_MCP_OAUTH_CLIENT_ID` e `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET` ativa o provedor `GoogleProvider` do FastMCP e troca o servidor para Streamable HTTP. O contêiner escuta na porta `8080`; o endpoint MCP é:

```text
https://SEU-SERVICO.run.app/mcp
```

`GOOGLE_ADS_MCP_BASE_URL` recebe a URL HTTPS raiz do serviço, sem `/mcp`. O Google redireciona para `https://SEU-SERVICO.run.app/auth/callback`. O proxy encaminha depois o retorno ao callback dinâmico do cliente MCP. Por isso, a URI fixa no cliente OAuth Web do Google é a callback do servidor, não os callbacks locais do Codex, Claude ou outro cliente.

## Descoberta e ferramentas

O cliente MCP faz o handshake do protocolo e descobre a autorização automaticamente. Nesta configuração, os principais endereços são:

| Endereço | Função |
| --- | --- |
| `/.well-known/oauth-protected-resource/mcp` | Metadados do recurso protegido no endpoint `/mcp` |
| `/.well-known/oauth-authorization-server` | Metadados do servidor de autorização FastMCP |
| `/register`, `/authorize`, `/token` | Registro dinâmico e etapas OAuth para clientes MCP |
| `/auth/callback` | Retorno do Google ao provedor OAuth do FastMCP |
| `/mcp` | Transporte MCP para inicialização, `tools/list` e `tools/call` |

Com a configuração somente de leitura, `tools/list` deve apresentar somente:

- `customers_list_accessible_customers` — lista as contas acessíveis ao usuário autenticado;
- `metadata_get_resource_metadata` — consulta metadados dos campos disponíveis;
- `search_search` — consulta dados com GAQL. Seus argumentos incluem `customer_id`, `resource`, `fields` e filtros opcionais.

Envie chamadas MCP pelo cliente que concluiu OAuth. Um `curl` anônimo ao endpoint `/mcp` não executa a inicialização, autorização, descoberta de ferramentas nem consulta; uma resposta `401` só indica que aquela solicitação precisa de autenticação.

## Sessões, estado e reinícios

O commit revisado mantém Streamable HTTP com estado por padrão. Ele documenta compatibilidade com clientes que usam `Mcp-Session-Id` e GET/SSE e com clientes que usam POST sem sessão e `subscriptions/listen`. Não habilite `stateless_http` para contornar problemas de roteamento: isso remove o canal GET/SSE usado por clientes compatíveis com o fluxo anterior.

Há dois tipos de estado que não devem ser confundidos:

- **OAuth:** estado e tokens do proxy podem ser armazenados no Firestore com `GOOGLE_ADS_MCP_STORAGE_TYPE=firestore`. A imagem precisa incluir o extra `firestore` e a conta de serviço precisa acessar o banco.
- **Sessão MCP e transmissão aberta:** não são persistidas pelo backend OAuth do Firestore. Uma reinicialização pode encerrar a sessão ou uma transmissão; o cliente deve reconectar e inicializar outra sessão. `min-instances=0` permite encerrar instâncias ociosas, mas o Cloud Run também pode reiniciar instâncias com mínimo maior que zero.

O Cloud Run pode encaminhar solicitações de um mesmo cliente a instâncias diferentes. A afinidade de sessão, se habilitada, é de melhor esforço e não substitui estado durável. Limitar o serviço a uma instância simplifica um piloto, mas reduz capacidade e não evita perda de sessão quando essa instância reinicia. Consulte [afinidade de sessão no Cloud Run](https://docs.cloud.google.com/run/docs/configuring/session-affinity) e o [contrato de HTTP do upstream](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/README.md#http-interoperability-notes).

## Camadas de autorização

O transporte HTTP não torna uma conta Google Ads pública. A política IAM do Cloud Run controla invocadores do serviço; o proxy FastMCP faz OAuth para o aplicativo; o Google Ads API valida o projeto autorizado e o papel do usuário na conta. A configuração de ferramentas reduz as operações expostas pelo servidor, mas a API não oferece escopo OAuth separado para leitura. Veja [Segurança](../../SECURITY.md).

Fontes: [código e README do Google Ads MCP fixados nesta revisão](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd), [FastMCP OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy), [descoberta OAuth no MCP](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/authorization-server-discovery.mdx) e [rotas do SDK Python MCP](https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/server/auth/routes.py).
