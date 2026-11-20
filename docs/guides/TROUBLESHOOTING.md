# 05 · Troubleshooting

## `redirect_uri_mismatch`

**Causa frequente:** URL de callback divergente da lista de URIs autorizadas.

**Verifique:** esquema `https`, domínio, porta, caminho, barra final e cliente OAuth correto.

**Correção:** inclua a redirect URI exata esperada pelo servidor e pelo cliente.

## `invalid_client`

**Causa frequente:** Client ID/Secret incorreto, cliente errado ou versão antiga do segredo em execução.

**Verifique:** ID utilizado, Secret Manager, versão e revisão atual do Cloud Run.

**Correção:** atualize a versão do segredo e faça o serviço consumir a versão corrigida. Não presuma que o erro foi causado por espaço ou quebra de linha sem evidência.

## HTTP `401`

O servidor pode rejeitar chamadas anônimas à rota `/mcp`.

**Teste:** conclua OAuth com um cliente compatível e repita a solicitação autenticada. `401` sem login pode ser comportamento correto.

## Ferramentas não aparecem

- Confirme a URL terminando em `/mcp`.
- Verifique se o cliente suporta o transporte do servidor.
- Inspecione os registros de autenticação.
- Verifique a configuração de namespaces e ferramentas da revisão upstream.

## Contas não aparecem

- Verifique a conta Google autorizada.
- Verifique o acesso à conta ou MCC.
- Confirme `customer_id` e `login_customer_id` quando aplicável.
- Revise erros da Google Ads API e suas permissões.

## Ordem recomendada

`Cloud Run → transporte HTTP → OAuth → ferramentas MCP → Google Ads API`

[← Validação](VALIDATION.md) · [Custos e operação →](OPERATIONS.md)
