# Índice da documentação

Este é um roteiro sequencial para quem trabalha com marketing e ainda está conhecendo a nuvem. Cada etapa tem um checkpoint: confirme-o antes de seguir. Os comandos são exemplos para revisar e adaptar; alguns habilitam serviços, criam ou alteram recursos e podem gerar custos.

| Etapa | O que conferir | Guia |
| --- | --- | --- |
| 1. Preparar | Projeto, faturamento, permissões, APIs e acesso à Google Ads API | [Pré-requisitos](getting-started/PREREQUISITES.md) |
| 2. Entender o ambiente | O que será publicado, qual commit de referência será usado e que recursos podem ser criados | [Implantação no Cloud Run](getting-started/DEPLOY.md) |
| 3. Preparar o login | Cliente OAuth, URLs de retorno e armazenamento dos valores secretos | [OAuth e Secret Manager](guides/OAUTH-AND-SECRETS.md) |
| 4. Publicar e conferir | Serviço HTTPS, autenticação, ferramentas MCP e consulta à conta autorizada | [Implantação](getting-started/DEPLOY.md) · [Validação](guides/VALIDATION.md) |
| 5. Operar | Erros, custos, registros, atualizações e manutenção | [Troubleshooting](guides/TROUBLESHOOTING.md) · [Custos](guides/COSTS.md) · [Operação](guides/OPERATIONS.md) |

O guia de implantação leva você até os pontos em que precisa pausar para preparar OAuth e conferir as ferramentas do commit fixado. Não pule esses pontos: se atualizar o servidor ou se a configuração organizacional for diferente, os requisitos podem mudar.

## Referência e apoio

- [Leia o mapa do projeto](../README.md)
- [Arquitetura e componentes](ARCHITECTURE.md)
- [MCP: STDIO e Streamable HTTP](concepts/MCP-TRANSPORTS.md)
- [Glossário](GLOSSARY.md)
- [Tutoria com seu assistente de IA: prompt pronto para copiar](guides/AI-TUTOR.md)
- [Vídeos complementares em português](guides/VIDEOS-PT-BR.md) — contexto visual, não procedimentos operacionais.
- [Segurança](../SECURITY.md)
- [Referências oficiais](REFERENCES.md)
- [Licença do guia](../LICENSE) · [Avisos de terceiros](../THIRD_PARTY_NOTICES.md)

## English

See the [English documentation index](en/README.md) and the [English project README](../README.en.md).

[← Voltar ao README](../README.md)

[Revisão documental, verificações e limites](REVIEW.md)
