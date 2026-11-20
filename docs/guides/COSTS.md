# Custos e avaliação de viabilidade

No experimento, foi observado consumo de CPU no Cloud Run **na ordem de centavos** em testes iniciais. Isso **não é o custo total da arquitetura**.

Custos possíveis: Cloud Run, Cloud Build, Artifact Registry, Secret Manager, logs, rede e armazenamento do estado OAuth. Também há esforço de implantação, atualização e suporte.

| Critério | Integração gerenciada | Hospedagem própria |
| --- | --- | --- |
| Configuração | Pode ser mais simples | Exige IAM, OAuth e deploy |
| Credenciais | Conforme oferta e custódia do fornecedor | Conforme implementação e controles internos |
| Operação | Parte delegada ao fornecedor | Responsabilidade de quem hospeda |
| Cobrança | Planos, limites e consumo | Infraestrutura, logs e manutenção |

**Não há economia comprovada** contra Composio ou qualquer integração gerenciada. Uma comparação válida precisa de cenários equivalentes, volume, SLA, manutenção e requisitos de segurança.

Alertas de orçamento não são necessariamente limites rígidos de gastos.
