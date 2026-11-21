# Segurança

O exemplo é um laboratório de baixo volume, não uma configuração de produção nem uma garantia de acesso autorizado. Revise estas camadas separadamente antes de conectar uma conta Google Ads.

## Entrada no Cloud Run e OAuth

O roteiro usa `--allow-unauthenticated` para que clientes MCP possam alcançar as rotas de descoberta e iniciar OAuth. Isso desativa a verificação de invocador do Cloud Run; o serviço pode receber tráfego anônimo e gerar custo. Não confunda essa política de IAM com o login Google no aplicativo: ferramentas MCP protegidas ainda exigem token OAuth válido.

O provedor Google do FastMCP mantém as credenciais do servidor e encaminha o retorno OAuth. O callback Google deste baseline é `https://SEU-SERVICO.run.app/auth/callback`; os callbacks dinâmicos locais do cliente MCP são encaminhados pelo proxy e não devem ser cadastrados no cliente OAuth Web do Google. Guarde o Client Secret fora do cliente MCP.

Se uma política de organização proibir acesso público, interrompa a implantação e peça à equipe responsável uma arquitetura compatível com o cliente. Um endpoint protegido por IAM do Cloud Run também exige que o cliente apresente uma identidade de invocador Google; isso é uma etapa distinta do OAuth do Google Ads.

## Quem pode consultar dados

Há três permissões independentes:

1. **Projeto Google Cloud:** o projeto dono do Client ID OAuth precisa ter a Google Ads API habilitada e o nível de acesso apropriado. Desde 9 de setembro de 2026, tokens de desenvolvedor foram encerrados; não copie guias antigos que solicitem um. Habilitar a API ou implantar o servidor não garante autorização para produção.
2. **Usuário Google Ads:** a pessoa que conclui OAuth precisa ter acesso à conta escolhida. Use uma conta de teste ou um usuário com o papel menos privilegiado que atenda à consulta, como acesso somente leitura quando disponível.
3. **Ferramentas expostas:** o arquivo `tools_config.yaml` do roteiro mantém `customers`, `search` e `metadata` e desativa `labels` e `assets`, que incluem mutações no upstream. Verifique `tools/list` depois do build e de cada atualização.

O Google Ads API usa o mesmo escopo OAuth `https://www.googleapis.com/auth/adwords` para operações de leitura e escrita; não existe um escopo separado que torne o token somente de leitura. Desativar ferramentas de mutação reduz as operações expostas por esta imagem, mas não restringe o escopo OAuth, o papel do usuário, nem alterações futuras no contêiner. Veja o [modelo oficial de acesso do Google Ads](https://developers.google.com/google-ads/api/docs/oauth/access-model) e a [política de níveis de acesso](https://developers.google.com/google-ads/api/docs/api-policy/developer-token).

## Segredos, identidade e estado

- Armazene `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET`, `GOOGLE_ADS_MCP_JWT_SIGNING_KEY` e `GOOGLE_ADS_MCP_STORAGE_ENCRYPTION_KEY` no Secret Manager. O Client ID é um identificador público; nunca coloque os segredos no `.env`, no código, no histórico de shell ou na configuração do cliente.
- Use a conta de serviço de execução separada da conta de build. Restrinja o acesso a cada segredo à identidade de execução e conceda ao runtime apenas o papel Firestore necessário para o estado OAuth.
- O backend OAuth Firestore desta imagem cifra os registros persistidos com a chave de armazenamento. A chave JWT precisa permanecer estável para assinar tokens entre instâncias. Planeje rotação coordenada: mudar chaves pode invalidar estado já salvo e exigir nova autenticação. O Google Cloud também criptografa dados armazenados; isso não substitui a proteção das chaves da aplicação.
- Fixe versões numéricas dos segredos referenciadas por variáveis de ambiente. O Cloud Run resolve valores de ambiente ao iniciar instâncias; a documentação do Google recomenda fixar uma versão em vez de `latest` para esse uso.
- O Firestore preserva estado OAuth, não sessões MCP em memória, transmissões SSE abertas ou assinaturas. Escala a zero e reinicializações podem exigir que o cliente reconecte.

## Registros e dados de contas

O upstream registra chamadas de ferramenta em formato estruturado e oculta vários campos sensíveis, mas esses eventos ainda podem indicar ferramenta, identificador de cliente Ads, horários, resultado e duração. Limite leitores do Cloud Logging, defina retenção adequada e evite anexar respostas, IDs de contas e capturas com dados a issues públicas.

As respostas de consulta podem conter dados de desempenho e informações de negócio. Conecte apenas clientes MCP aprovados, confirme a conta e o período antes de solicitar uma consulta e siga as regras da organização para compartilhar esses resultados.

## Repositório e atualizações

Antes de publicar o guia ou reconstruir a imagem:

- [ ] Examine o conteúdo e o histórico para remover credenciais, tokens, arquivos OAuth, dados reais de contas, URLs internas, logs e capturas de tela sensíveis.
- [ ] Confirme que `.env` e arquivos de credenciais locais estão ignorados pelo Git e pelo contexto do Cloud Build.
- [ ] Revise o commit upstream fixado, o Dockerfile e a configuração de ferramentas.
- [ ] Revise alterações de OAuth, callback, permissões, dependências, ferramentas e armazenamento antes de atualizar o pin.
- [ ] Registre o commit de origem, o digest da imagem e as versões de segredos usadas por cada revisão.

A compilação desta revisão é derivada do código oficial, mas não é uma distribuição oficial do Google. Preserve a licença e os avisos do servidor upstream ao redistribuir fontes ou imagem. Consulte [OAuth e segredos](docs/guides/OAUTH-AND-SECRETS.md), [operação](docs/guides/OPERATIONS.md) e [referências oficiais](docs/REFERENCES.md).

[English security guide](docs/en/SECURITY.md)
