# 06 · Operação e manutenção

Este serviço combina Cloud Run, OAuth, Google Ads API e armazenamento de estado. Revise as quatro camadas após cada atualização de código ou configuração.

## Rotina

- [ ] Registrar o commit de origem do Google Ads MCP, a versão de dependências e o digest da imagem implantada.
- [ ] Revisar o diff do upstream antes de reconstruir; não atualizar o pin automaticamente para `main` ou para uma tag móvel.
- [ ] Confirmar que `tools_config.yaml` permite apenas `customers`, `search` e `metadata`; conferir `tools/list` depois de cada nova revisão.
- [ ] Acompanhar status, latência, reinicializações, erros HTTP e saturação de concorrência no Cloud Run.
- [ ] Acompanhar erros de autorização, nível de acesso do projeto e uso de operações na Google Ads API.
- [ ] Conferir acesso e versões dos três segredos: Client Secret OAuth, chave JWT e chave de armazenamento OAuth. A rotação da chave JWT invalida assinaturas anteriores; a troca da chave de armazenamento afeta a leitura do estado cifrado.
- [ ] Confirmar que a conta de serviço tem apenas `roles/datastore.user` no Firestore e acesso aos segredos usados pelo serviço.
- [ ] Revisar custo e retenção de Cloud Run, Firestore, Artifact Registry, Cloud Build, Secret Manager e Cloud Logging.
- [ ] Manter o digest da imagem e as versões anteriores dos segredos necessários para rollback.

## Estado e disponibilidade

O Firestore preserva estado OAuth entre instâncias e reinicializações. Ele não preserva sessões MCP em memória, conexões SSE abertas ou assinaturas de `subscriptions/listen`. Se uma instância reiniciar, oriente o cliente a reconectar e inicializar uma nova sessão.

Este tutorial configura uma implantação de avaliação com no máximo uma instância. Isso limita a capacidade e não fornece alta disponibilidade. `min-instances=0` permite encerrar instâncias ociosas e pode aumentar a latência de início. `min-instances=1` mantém uma instância aquecida como alvo, com custo adicional, mas não impede reinicializações. A afinidade de sessão do Cloud Run é de melhor esforço; não dependa dela como mecanismo de persistência.

O upstream mantém HTTP com estado para compatibilidade com clientes Streamable HTTP atuais e anteriores. Não habilite `stateless_http` sem testar os clientes previstos: isso remove o fluxo GET/SSE usado por alguns clientes. O Firestore para tokens OAuth e as sessões do transporte MCP são camadas de estado diferentes.

## Inspecionar o serviço

```bash
# Inspeciona a revisão ativa e a configuração implantada.
gcloud run services describe "$SERVICE" --region="$REGION"

# Lista as revisões disponíveis para investigar e planejar rollback.
gcloud run revisions list \
  --service="$SERVICE" \
  --region="$REGION"

# Consulta os builds recentes.
gcloud builds list --limit=10
```

Para logs, use Cloud Logging com filtro pelo nome do serviço e janela de tempo necessária. Os eventos de auditoria do servidor incluem nome da ferramenta, identificadores de conta e estado da execução; vários argumentos sensíveis são ocultados, mas logs continuam sendo dados operacionais a proteger. Evite copiar respostas de consulta ou logs para issues públicas.

## Atualização e rollback

1. Leia o diff e as notas do upstream; confirme transporte, configuração de ferramentas, OAuth e armazenamento para o commit novo.
2. Construa a partir do commit fixado e registre a proveniência do build e o digest publicado.
3. Implante como nova revisão sem substituir imediatamente o digest anterior.
4. Faça login em um cliente MCP de teste, confira `tools/list` e execute uma consulta não destrutiva em conta autorizada.
5. Verifique logs, erros e reconexão após reinicialização antes de direcionar usuários ao novo serviço.
6. Em caso de regressão, direcione o serviço à revisão anterior e aos números de versão Secret Manager compatíveis com ela.

Este roteiro injeta uma chave de armazenamento própria. Por isso, a rotação do Client Secret ou da chave JWT não troca automaticamente a chave de criptografia do Firestore. Trate cada segredo separadamente: atualizar o Client Secret requer uma revisão compatível com o cliente OAuth; rotacionar JWT pode exigir novo login; rotacionar a chave de armazenamento exige um plano para migrar o estado ou obter novas autorizações. O backend não migra dados automaticamente entre chaves.

## Encerrar o laboratório

Confirme primeiro projeto, serviço e região. Para remover apenas o serviço Cloud Run, execute o comando e revise a confirmação da CLI:

~~~bash
gcloud run services delete "$SERVICE" --region="$REGION" --project="$PROJECT_ID"
~~~

Excluir o Cloud Run não remove os recursos de apoio. Em um projeto dedicado ao laboratório, confira cada recurso no Console e remova-o somente depois de confirmar que não tem outro uso:

| Recurso | Onde conferir | O que permanece |
| --- | --- | --- |
| Bucket de origem | Cloud Storage → bucket criado na etapa 4 | Arquivos de origem podem continuar gerando cobrança até serem removidos |
| Repositório de imagens | Artifact Registry → mcp-servers | Versões de imagem permanecem até a limpeza definida pela sua política |
| Três segredos | Secret Manager | Versões permanecem; preserve apenas o que um rollback autorizado ainda exigir |
| Banco OAuth | Firestore → (default) | Remover o estado perde autorizações; confira se nenhuma outra aplicação usa o banco |
| Contas de serviço e IAM | IAM e administração | Revise as duas contas e seus vínculos após remover os recursos |
| Aplicativo OAuth | Google Auth Platform | Revise credenciais e revogue acessos que não sejam mais necessários |
| Logs | Cloud Logging | A retenção pode continuar após a remoção do serviço |

Não apague um projeto ou banco compartilhado para encerrar este laboratório. Confira o relatório de faturamento depois: remover um serviço não apaga cobranças pelo uso anterior.


Para custos, consulte [Custos](COSTS.md). Para limites de acesso e credenciais, consulte [Segurança](../../SECURITY.md). Fontes: [Cloud Run — afinidade de sessão](https://docs.cloud.google.com/run/docs/configuring/session-affinity), [Cloud Run — instâncias mínimas](https://docs.cloud.google.com/run/docs/configuring/min-instances) e [README do upstream fixado](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/README.md#http-interoperability-notes).

Para migrar sem substituir as configurações existentes, preservar versões de chaves e testar rollback, consulte [persistência OAuth](OAUTH-PERSISTENCE.md). Não confunda rollback de tráfego com restauração de estado OAuth.
