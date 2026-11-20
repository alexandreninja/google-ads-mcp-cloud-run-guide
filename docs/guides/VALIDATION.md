# Matriz de validação e evidências

O experimento validou consultas reais a contas gerenciadoras autorizadas em clientes MCP de teste. **Não há afirmação de integração concluída com Copilot corporativo ou múltiplos colaboradores.**

| Teste | Esperado | Observação |
| --- | --- | --- |
| `/mcp` sem credenciais | `401` no modelo que exige autenticação | Teste negativo esperado, não falha de deploy |
| Descoberta e OAuth | Autorização válida e ferramentas disponíveis | Verificar callback, metadados e cliente |
| `customers_list_accessible_customers` | IDs das contas acessíveis ao usuário | Não publicar IDs reais |
| Consulta GAQL autorizada | Resposta consistente com permissões | Registrar período, métrica e fonte |
| Conta não autorizada | Recusa de acesso | Não contornar permissões |

## Smoke-test negativo

```bash
curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' \
  'https://SEU-SERVICO.a.run.app/mcp'
```

O `401` é válido somente quando há uma configuração que exige login. Não prova que toda a aplicação é segura.

## Registro de teste (sem dados sensíveis)

```text
Data/hora UTC:
Tag/commit upstream:
Cliente e transporte:
Teste e resultado esperado:
Resultado observado:
Diagnóstico:
Próxima ação:
```
