# 05 · Solução de problemas

Use esta página depois de anotar **a etapa, a mensagem completa e o horário** em que algo falhou. Os erros de Cloud Run, OAuth, MCP e Google Ads vêm de camadas diferentes; o mesmo `401` ou `403` pode ter causas distintas.

## Encontre a primeira etapa que falhou

| Etapa | Sinal esperado | Se falhar, comece por |
| --- | --- | --- |
| Projeto e faturamento | O projeto escolhido é o projeto certo e está vinculado a uma conta de faturamento ativa | [Projeto, faturamento e APIs](#projeto-faturamento-ou-api) |
| Build e imagem | O Cloud Build conclui e a imagem aparece no Artifact Registry | [Build ou envio da imagem](#build-ou-envio-da-imagem) |
| Revisão do Cloud Run | A revisão fica pronta e o serviço tem uma URL HTTPS | [Revisão não fica pronta ou retorna erro](#revisão-não-fica-pronta-ou-retorna-erro) |
| OAuth | O login termina e retorna para o endereço cadastrado | [Erros OAuth](#erros-oauth) |
| Cliente MCP | O cliente conecta e descobre as ferramentas | [Cliente não encontra ferramentas MCP](#cliente-não-encontra-ferramentas-mcp) |
| Google Ads API | A conta aparece e uma consulta autorizada retorna dados | [Contas ou consultas falham](#contas-ou-consultas-falham) |

Confira primeiro se a CLI está apontando para o projeto que você pretendia usar:

```bash
gcloud config get-value project
```

O valor exibido deve ser o mesmo `PROJECT_ID` do tutorial. Se não for, selecione o projeto correto antes de repetir qualquer comando. Uma implantação no projeto errado pode criar recursos e custos em outra conta.

## Projeto, faturamento ou API

### A mensagem menciona `billing`, `SERVICE_DISABLED` ou `PERMISSION_DENIED`

1. No topo do Console do Google Cloud, confirme o projeto selecionado.
2. Em **Faturamento**, confirme que o projeto está vinculado a uma conta de faturamento ativa. Criar um projeto, por si só, não garante que o faturamento esteja ativado.
3. Em **APIs e serviços**, confira se as APIs exigidas por esta versão do guia estão habilitadas.
4. Se o acesso for negado, peça a um administrador para conferir a permissão específica que falta. Evite resolver erros de IAM concedendo o papel amplo de Proprietário.

A ativação da Google Ads API e o nível de acesso aos dados de produção são verificações distintas. Para acesso de produção, consulte a seção [Acesso à Google Ads API](#contas-ou-consultas-falham).

## Build ou envio da imagem

### O build diz que não encontrou `Dockerfile` ou arquivos do projeto

Neste roteiro, o comando envia `$UPSTREAM_DIR`, o checkout do **Google Ads MCP oficial** que foi preparado no commit fixado. Confirme que `git -C "$UPSTREAM_DIR" rev-parse HEAD` mostra o commit esperado e que `Dockerfile` existe nessa pasta; não execute o build na raiz deste repositório de documentação.

Se o comando não localizar `$UPSTREAM_DIR`, volte à seção de preparação da implantação e confira as variáveis `GUIDE_DIR` e `UPSTREAM_DIR`. A origem do build é enviada ao Cloud Storage antes de o Cloud Build começar.

### O envio da origem para Cloud Storage é negado

O comando desta implantação usa o bucket próprio indicado por `--gcs-source-staging-dir`. A pessoa ou automação que executa `gcloud builds submit` precisa poder criar o objeto de origem nesse bucket. Separadamente, a conta de serviço `google-ads-mcp-build` precisa ler essa origem; o guia concede a ela `roles/storage.objectViewer`. Se o erro mencionar `storage.objects.create`, peça ao administrador uma permissão de escrita limitada ao bucket de staging para quem executa o comando. Não dê acesso amplo ao bucket nem troque o papel de leitura da conta de build por Owner.

Para submeter o build com a conta de serviço gerenciada pelo guia, quem executa o comando também precisa de `iam.serviceAccounts.actAs` sobre `google-ads-mcp-build` e de permissão para criar builds no projeto. Se a mensagem nomear uma permissão diferente, peça ao administrador para conferir essa permissão exata e a política da organização.

### O build conclui, mas o envio ao Artifact Registry é negado

Confirme que o repositório Docker já existe na região usada pela imagem e que a identidade de execução do build pode gravar nele. O Cloud Build usa uma identidade própria; ela não é a mesma conta de serviço que executa o serviço no Cloud Run.

Abra os detalhes do build no Console do Google Cloud e veja a primeira etapa marcada como falha. Isso costuma indicar se o problema foi a criação da imagem, a permissão de envio ou a localização do repositório.

## Revisão não fica pronta ou retorna erro

No Console, abra **Cloud Run → serviço → Registros** e filtre a revisão atual. Para consultar os registros pela CLI:

```bash
gcloud run services logs read "$SERVICE" --region="$REGION" --limit=20
```

Leia o primeiro erro de inicialização; as mensagens seguintes podem ser apenas consequência. Confira:

- se a revisão aponta para a imagem que você acabou de publicar;
- se os nomes das variáveis e segredos coincidem com os da versão upstream escolhida;
- se a conta de serviço do Cloud Run tem acesso de leitura somente aos segredos necessários;
- se os valores não secretos, como a URL pública e o projeto da Google Ads API, estão definidos.

Se você acabou de corrigir um segredo, confirme qual versão foi vinculada à revisão. Segredos configurados como variáveis de ambiente são lidos quando a instância inicia; publicar uma nova versão do segredo não atualiza uma instância já iniciada por conta própria. O Cloud Run cria uma revisão quando sua configuração é atualizada. Para instruções atuais, veja [Configurar segredos para serviços do Cloud Run](https://docs.cloud.google.com/run/docs/configuring/services/secrets?hl=pt-BR).

Não copie valores de segredos para tickets, capturas de tela ou registros compartilhados.

## Erros OAuth

### `redirect_uri_mismatch`

O Google recebeu um endereço de retorno diferente do cadastrado no cliente OAuth. Compare o endereço que aparece na mensagem com:

- o domínio HTTPS da URL atual do Cloud Run;
- o caminho de callback exigido pela **versão upstream implantada**;
- a lista de URIs autorizadas no cliente OAuth usado pelo serviço.

Cada parte precisa coincidir, incluindo esquema (`https`), domínio, caminho e barra final quando presente. Não adivinhe o caminho de callback: confira a documentação ou configuração da versão fixada do Google Ads MCP.

### `invalid_client`

O Google não reconheceu o cliente OAuth apresentado. Verifique se o serviço usa o Client ID e o Client Secret do mesmo cliente OAuth, se o cliente pertence ao projeto correto e se a revisão do Cloud Run referencia a versão do segredo pretendida. Se rotacionou o segredo, publique uma revisão atualizada.

### Login termina, mas o retorno ao serviço não conclui

Confira a URL base configurada no serviço e as URIs de redirecionamento. A URL pública deve ser a URL HTTPS do serviço atual, e o callback deve corresponder à versão implantada. Se mudou o serviço ou o cliente OAuth, repita a configuração nos dois lados.

## Cliente não encontra ferramentas MCP

1. Use a URL do serviço com o caminho MCP indicado pelo README da versão fixada — no fluxo HTTP documentado, normalmente `/mcp`.
2. Confirme que o cliente de IA escolhido oferece suporte ao transporte HTTP usado pelo servidor e que a conexão completou a autenticação.
3. Peça ao cliente para atualizar ou redescobrir a lista de ferramentas depois de corrigir a conexão.
4. Confira os registros do Cloud Run no horário da tentativa. Uma falha de autenticação, transporte ou inicialização é diferente de uma consulta Google Ads negada.
5. Se a conexão autentica, mas faltam ferramentas, examine a configuração de ferramentas e namespaces da mesma versão upstream implantada.

Uma resposta HTTP isolada não prova que a sessão MCP esteja pronta. Faça a verificação de descoberta de ferramentas com um cliente MCP compatível, como na página [Validação](VALIDATION.md).

## Contas ou consultas falham

### A lista de contas está vazia ou não inclui a conta esperada

- Confirme qual Conta Google concluiu o OAuth; ela precisa ter acesso à conta Google Ads.
- Se a conta está sob uma conta de administrador (MCC), confira o contexto e o `login_customer_id` conforme a versão do servidor.
- Confira se `customer_id` está correto e sem pontuação, conforme o formato esperado pela ferramenta.
- Separe permissão do usuário na conta Ads do nível de acesso à API do projeto Google Cloud. São autorizações diferentes.

### A consulta a uma conta de teste funciona, mas à conta de produção não

A Google Ads API alterou seu processo de acesso. Desde **9 de setembro de 2026**, o token de desenvolvedor deixou de determinar o nível de acesso da API. A ativação da API no projeto concede acesso de teste; para uso com contas de produção, confira o nível de acesso e solicite o necessário na página **Visão geral da API Google Ads** do projeto Cloud que emitiu as credenciais OAuth. A Central de APIs do Google Ads não é mais o lugar para solicitar esse acesso.

Se a mensagem contiver `CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION`, a documentação associa esse erro à v25 e versões mais recentes. A v24 e anteriores podem retornar `ACTION_NOT_PERMITTED` para esse problema. Em qualquer caso, verifique primeiro o nível de acesso do projeto à API, antes de alterar IDs de conta ou refazer o OAuth.

### A API nega um campo ou consulta GAQL

Confirme a versão da Google Ads API usada pela versão fixada do servidor e verifique se o campo e a métrica estão disponíveis e são compatíveis na mesma consulta. Use o erro completo e os registros para identificar campo, recurso e versão; não altere a consulta apenas para remover métricas sem confirmar a regra de compatibilidade.

## HTTP `401` ou `403`

O código isolado não identifica a camada que recusou a solicitação:

- **`401` antes de autenticar:** pode ser o servidor MCP exigindo um fluxo OAuth válido. Se esta implantação protege `/mcp` com OAuth, essa resposta sem login pode ser esperada.
- **`403` do Cloud Run:** confira se o serviço permite chegar à entrada HTTP conforme o desenho do guia. `--allow-unauthenticated` remove a exigência de identidade IAM do Cloud Run para invocar o serviço; não dispensa o OAuth do aplicativo nem o acesso à conta Google Ads.
- **`403` após o OAuth:** leia o corpo e os registros para distinguir permissão na conta Ads, nível de acesso do projeto à API e regras de política da ferramenta.

Não remova proteções de autenticação para fazer o erro desaparecer. Identifique primeiro qual camada o emitiu.

## Ao pedir ajuda

Compartilhe a etapa, o horário aproximado, região, revisão, versão/commit upstream e a mensagem de erro sem segredos. Remova Client Secret, tokens OAuth, chaves de assinatura, cookies, dados pessoais e identificadores de conta que não sejam necessários. Para falhas do servidor-base, consulte as [issues do projeto oficial](https://github.com/googleads/google-ads-mcp/issues).

[← Validação](VALIDATION.md) · [Custos e operação →](OPERATIONS.md) · [Vídeos em português](VIDEOS-PT-BR.md)

## Reconexão OAuth frequente

Confira backend, dependência Firestore, IAM, estabilidade da chave de criptografia e status de publicação OAuth. Não confunda encerramento do transporte HTTP com perda de autorização. Veja [migração e diagnóstico de persistência](OAUTH-PERSISTENCE.md).
