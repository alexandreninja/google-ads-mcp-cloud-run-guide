# 04 · Conexão e testes

## 1. Status do Cloud Run

```bash
gcloud run services describe google-ads-mcp \
  --region=us-central1 \
  --format='value(status.url)'
```

Substitua serviço e região pelos valores definidos na implantação.

## 2. Teste anônimo de HTTP

```bash
curl --silent --show-error --output /dev/null \
  --write-out '%{http_code}\n' \
  "https://SEU-SERVICO.a.run.app/mcp"
```

Se o servidor exigir login, `401 Unauthorized` é um resultado esperado.

## 3. Conectar cliente MCP

Em um cliente compatível com Streamable HTTP, configure:

```json
{
  "mcpServers": {
    "google-ads-mcp": {
      "serverUrl": "https://SEU-SERVICO.a.run.app/mcp"
    }
  }
}
```

**A estrutura exata varia por cliente.** Consulte a documentação do produto utilizado (VS Code, Codex CLI, outros).

Conclua o fluxo OAuth interativo.

## 4. Verificar ferramentas e contas

Após a autenticação:

1. Liste as ferramentas disponibilizadas pelo servidor.
2. Execute `customers_list_accessible_customers`.
3. Confirme que apenas contas acessíveis à identidade autenticada aparecem.
4. Faça uma consulta GAQL em conta de teste ou autorizada.
5. Verifique períodos, métricas e formato da resposta.

Algumas ferramentas são disponibilizadas apenas quando a configuração e a versão correspondente as habilitam.

## 5. Registro de testes

| Teste | Resultado esperado |
| --- | --- |
| `/mcp` anônimo | Acesso negado, quando a autenticação é exigida |
| OAuth | Autorização concluída |
| Descoberta MCP | Ferramentas visíveis |
| Listagem de contas | Contas da identidade autorizada |
| GAQL | Dados da conta e período solicitados |
| Conta sem permissão | Acesso recusado |

[Próximo: troubleshooting →](TROUBLESHOOTING.md)
