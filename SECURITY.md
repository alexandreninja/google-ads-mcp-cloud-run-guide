# Política de segurança e fronteiras de confiança

> [!WARNING]
> Guia educacional. A arquitetura de exemplo não equivale a homologação. Não compartilhe tokens, contas, URLs internas, logs privados ou imagens com dados reais em issues.

## Fronteiras

1. **Cliente MCP:** recebe respostas e pode repassá-las ao ambiente do modelo. Avalie fornecedor, retenção, identidades e políticas institucionais.
2. **Endpoint HTTP:** acesso à rede não implica acesso livre às ferramentas. Configure TLS, OAuth, proteção contra abuso e monitoramento.
3. **Cloud Run:** utilize conta de serviço com o menor privilégio viável; revise IAM, logs e região.
4. **Google Ads API:** a permissão real depende do OAuth e da conta do usuário. Desabilitar ferramentas de mutação **não torna o escopo `adwords` somente leitura**.
5. **Secret Manager:** controle acessos, rotação e auditoria; nunca imprima o valor de segredos.

## Antes de colocar em produção

- [ ] Aprovação de quem responde pelos dados e revisão da segurança da informação.
- [ ] Avaliação do cliente MCP, do modelo e das fronteiras de processamento externo.
- [ ] Revisão de escopos OAuth, permissões das contas e ferramentas habilitadas.
- [ ] Estratégia de estado OAuth persistente, revogação e renovação.
- [ ] Testes negativos de acesso, limites, controles de rede e monitoramento.
- [ ] Política de logs minimizados, retenção e alertas.
- [ ] Avaliação de TCO, limites de uso e resposta a incidentes.

## Comunicação responsável

Não abra issues públicas com vulnerabilidades exploráveis ou dados reais. Use canais privados de divulgação responsável ou o projeto upstream, conforme o problema.
