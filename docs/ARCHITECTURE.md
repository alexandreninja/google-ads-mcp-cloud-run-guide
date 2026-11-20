# Arquitetura e fronteiras

![Fluxos de implantação e consulta](assets/architecture.svg)

## Capô fechado

Existem dois fluxos distintos:

1. **Implantação:** versão do código oficial → Cloud Build → Artifact Registry → Cloud Run.
2. **Consulta:** cliente MCP autorizado ↔ endpoint Streamable HTTP no Cloud Run ↔ ferramentas do servidor ↔ Google Ads API.

OAuth, Secret Manager, IAM e logs sustentam o funcionamento. **Eles não são necessariamente nós sequenciais do caminho de cada requisição**; Cloud Build não participa das consultas.

## Capô aberto

| Camada | Responsabilidade | Verificação necessária |
| --- | --- | --- |
| Cliente | Requisições, interface e processamento das respostas | Política de dados, suporte MCP |
| Transporte | Streamable HTTP e negociação de sessão | Versão e interoperabilidade |
| Servidor | Ferramentas e intermediação com Google Ads API | Ferramentas habilitadas, auditoria |
| Identidade | OAuth e tokens | Callback, scopes, revogação |
| Infraestrutura | Execução, IAM, logs, limites, custos | Persistência e segurança |
| Dados | Informações autorizadas das contas | Minimização e governança |

## Decisões registradas

- [ADR-0001](decisions/0001-streamable-http.md): transporte remoto para reduzir dependência de execução local.
- [ADR-0002](decisions/0002-cloud-run.md): hospedagem no Google Cloud por viabilidade institucional e caminho oficial documentado — **não é exigência do MCP**.

## Representação textual

```text
Deploy:
upstream fixado -> Cloud Build -> Artifact Registry -> Cloud Run

Uso:
Cliente autorizado <-> Cloud Run /mcp <-> Google Ads MCP <-> Google Ads API

Controles de apoio:
OAuth | Secret Manager | IAM | logs | governança de dados
```

Antes de utilizar com outras pessoas, consulte a [política de segurança](../SECURITY.md) e o [checklist operacional](guides/OPERATIONS.md).
