# Custos do ambiente

Não há custo garantido como zero. O valor depende de região, duração e volume das solicitações, configuração do contêiner, quantidade de dados persistidos, tráfego, retenção de logs e preços vigentes. Consulte os preços atuais antes da implantação.

| Serviço | O que pode gerar custo |
| --- | --- |
| Cloud Run | CPU, memória, solicitações, instâncias mínimas e tempo de execução. Chamadas HTTP longas e transmissões também mantêm uma solicitação ativa. |
| Cloud Build | Execuções para construir ou atualizar a imagem. |
| Artifact Registry | Armazenamento das versões de imagem. Remova imagens antigas segundo uma política de retenção compatível com seu rollback. |
| Firestore | Leituras, gravações, armazenamento, backup e operações de limpeza de estado OAuth. O uso depende da quantidade de usuários e renovações de token. |
| Secret Manager | Versões armazenadas e acessos aos segredos, incluindo leituras quando instâncias são iniciadas. |
| Cloud Logging | Ingestão, consultas, exportação e retenção além dos limites aplicáveis. |
| Rede | Tráfego de saída, especialmente respostas de consultas e integrações externas. |

## Limitar surpresas

1. Faça a primeira implantação em um projeto de avaliação com faturamento e APIs habilitados apenas conforme necessário.
2. `min-instances=0` evita manter uma instância mínima aquecida, mas aumenta a latência de início e não elimina cobranças por solicitações, builds, armazenamento, banco ou logs.
3. A configuração do tutorial limita a uma instância; isso restringe capacidade e não limita os gastos dos demais serviços.
4. Configure alertas de orçamento e acompanhe a fatura. Alertas de orçamento notificam; não interrompem o serviço nem funcionam como teto automático.
5. Revise retenção de imagens, dados Firestore, logs e versões de segredos. A exclusão de estado OAuth pode exigir que os usuários entrem novamente.
6. Defina limites de concorrência compatíveis com clientes que mantenham fluxos HTTP abertos; uma concorrência muito baixa pode formar fila ou rejeitar solicitações.
7. Avalie os custos de suporte, atualização, revisão de acesso e manutenção, além dos recursos cobrados pelo Google Cloud.

O nível de acesso da Google Ads API e suas quotas de operação são controles de acesso e capacidade separados da fatura de infraestrutura do Cloud. O Google encerrou tokens de desenvolvedor em 9 de setembro de 2026; novos projetos precisam verificar o nível de acesso associado ao projeto que contém as credenciais OAuth. Isso não é uma promessa de acesso ilimitado nem de custo zero.

Preços e limites podem mudar. Consulte [preços do Cloud Run](https://cloud.google.com/run/pricing), [preços do Firestore](https://cloud.google.com/firestore/pricing), [preços do Cloud Build](https://cloud.google.com/build/pricing), [preços do Artifact Registry](https://cloud.google.com/artifact-registry/pricing), [preços do Secret Manager](https://cloud.google.com/secret-manager/pricing), [Cloud Billing](https://cloud.google.com/billing/docs) e a [política de acesso da Google Ads API](https://developers.google.com/google-ads/api/docs/api-policy/developer-token).

## Persistência e franquia gratuita

Confira freeTier no banco escolhido e acompanhe consumo de todas as franquias, inclusive Secret Manager e imagens adicionais. Elegibilidade não equivale a custo zero medido. O experimento descrito em [persistência OAuth](OAUTH-PERSISTENCE.md) ainda não possui avaliação de faturamento de longo prazo.
