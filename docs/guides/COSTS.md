# Custos do ambiente

O faturamento depende de volume, configuração, região e recursos utilizados.

| Serviço | O que acompanhar |
| --- | --- |
| Cloud Run | CPU, memória, instâncias e requisições |
| Cloud Build | Construções executadas |
| Artifact Registry | Armazenamento de imagens |
| Secret Manager | Segredos, versões e acessos |
| Cloud Logging | Volume e retenção de registros |
| Rede e armazenamento | Tráfego e persistência OAuth |

## Controle inicial

1. Escolha uma região e configure um projeto de testes.
2. Use `min-instances=0` para evitar instâncias mínimas contínuas quando apropriado.
3. Acompanhe métricas e fatura de **todos os serviços**.
4. Configure alertas de orçamento e revise quotas.
5. Avalie o custo de manutenção além da infraestrutura.

Alertas de orçamento **não são uma trava automática** de gastos.

[Cloud Run Pricing](https://cloud.google.com/run/pricing) · [Cloud Billing](https://cloud.google.com/billing/docs).
