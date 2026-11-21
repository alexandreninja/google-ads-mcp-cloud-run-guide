# 01 · Preparar o projeto e conferir os acessos

Esta implantação foi organizada para ser executada no **Cloud Shell**, o terminal Bash aberto pelo Console do Google Cloud. Assim você evita instalar ferramentas no computador. O Cloud Shell ainda é só o local de trabalho: os comandos publicam recursos no projeto escolhido e alguns podem gerar cobrança.

## Antes de abrir o terminal

Tenha em mãos:

- **Um projeto Google Cloud** escolhido pela sua organização, com faturamento habilitado. Anote o **ID do projeto** (um identificador curto), não o nome que aparece no Console.
- **Acesso para fazer as alterações necessárias** ou uma pessoa administradora que possa fazê-las. A implantação habilita APIs, cria um bucket para a origem dos builds, que permanece até a limpeza, constrói e armazena uma imagem, cria um serviço Cloud Run, duas contas de serviço, segredos e um banco Firestore. A conta de build precisa ler o código de origem, publicar a imagem e gravar logs; a conta de execução precisa ler segredos e acessar o Firestore. As permissões IAM exatas dependem das políticas da organização; peça permissões específicas, sem usar Owner como atalho.
- **Acesso à Google Ads API no mesmo projeto.** Habilitar a API libera o ambiente de teste; consultar contas de produção exige o nível de acesso apropriado, que pode depender de uma solicitação no Console do Google Cloud. Esse processo mudou em 2026. Consulte a [página oficial de níveis de acesso](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR). O tutorial fixa o commit `44ca7770519362c8f334875477e1ceb499f8d2dd`; se você decidir atualizar, reavalie os requisitos e a configuração em vez de presumir que o procedimento permanece igual.
- **Uma conta Google com acesso à conta de anúncios** que será consultada. O acesso de API ao projeto e a permissão de usuário na conta são duas verificações distintas. Se sua organização acessa clientes por uma conta de administrador (MCC), use o arranjo aprovado pela equipe responsável.
- **Um cliente OAuth** que possa ser configurado para o servidor HTTP, com permissão para cadastrar a URL de retorno exata do servidor conforme o commit de referência. O cliente MCP usa outra etapa do fluxo; não cadastre a URL dele como callback do servidor. Você configurará esse cliente no guia de [OAuth e Secret Manager](../guides/OAUTH-AND-SECRETS.md).
- **Um cliente MCP compatível com Streamable HTTP e OAuth** para a validação final. O login confirma a identidade; não define, por si só, quais ferramentas de anúncios o servidor oferece.

Se algum item depender de outra equipe, pare aqui e encaminhe a lista. Não é necessário compartilhar senha, segredo ou arquivo de credenciais para pedir essas liberações.

## Permissões para pedir à administração

Em um projeto pessoal que você criou, sua identidade pode já ter os acessos necessários. Em ambiente corporativo, envie esta tabela à equipe responsável. Ela lista as operações do roteiro, não recomenda conceder um único papel amplo. Um administrador pode executar só os blocos de criação e IAM, deixando a implantação com você.

| Operação do operador humano | Permissões a conferir | Escopo |
| --- | --- | --- |
| Habilitar e usar APIs | serviceusage.services.enable e serviceusage.services.use | Projeto do laboratório |
| Criar contas de serviço | iam.serviceAccounts.create | Projeto |
| Submeter um build | cloudbuild.builds.create | Projeto |
| Enviar a origem do build | storage.buckets.get e storage.objects.create | Bucket de staging |
| Atuar como as identidades de build e execução | iam.serviceAccounts.actAs | Cada uma das duas contas de serviço |
| Ler a imagem para implantar | artifactregistry.repositories.downloadArtifacts | Repositório de imagens |
| Criar/atualizar o Cloud Run e liberar sua entrada | run.services.create, run.services.update e run.services.setIamPolicy | Projeto/serviço do laboratório |
| Criar repositório, bucket, segredos e banco | artifactregistry.repositories.create, storage.buckets.create, secretmanager.secrets.create, secretmanager.versions.add e datastore.databases.create | Projeto e recursos criados |
| Conceder os acessos do roteiro | setIamPolicy do recurso correspondente; resourcemanager.projects.setIamPolicy para os vínculos no projeto | Apenas recursos/projeto do laboratório |

A etapa 4 da implantação inclui Object Creator no bucket para o operador e Service Account User nas duas identidades, quando necessários. Object Creator não substitui a permissão de consultar metadados do bucket. A conta de build recebe leitura da origem, escrita no repositório de imagens e escrita de logs. A conta de execução recebe leitura dos três segredos e acesso ao estado Firestore. Permissões efetivas também dependem de políticas da organização; uma mensagem de bloqueio não deve ser resolvida com a remoção dessas políticas.

Para conferir detalhes, consulte [contas de build definidas pelo usuário](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts) e [papéis para implantar no Cloud Run](https://docs.cloud.google.com/run/docs/deploying#required_roles).


## Checkpoint 1 · confira a conta e o projeto

No Console do Google Cloud, selecione o projeto de teste aprovado e confirme que o faturamento está vinculado. Depois abra o Cloud Shell. O nome e o ícone podem mudar, mas ele fica no cabeçalho do Console.

Estes dois comandos apenas informam quais ferramentas estão disponíveis no terminal; não criam nem alteram recursos:

```bash
# Confere se o terminal reconhece a ferramenta do Google Cloud.
gcloud --version

# Confere se Git está disponível para baixar o código oficial.
git --version
```

Se um comando não for encontrado no Cloud Shell, pare e verifique se abriu o terminal correto ou se a organização desativou alguma ferramenta.

## Checkpoint 2 · selecione explicitamente o projeto

```bash
# Troque o texto entre aspas pelo ID copiado do seletor de projetos.
export PROJECT_ID="SEU_ID_DE_PROJETO"

# Define o projeto padrão somente para os próximos comandos deste terminal.
gcloud config set project "$PROJECT_ID"

# Mostra o projeto que ficou selecionado; compare o resultado com o Console.
gcloud config get-value project

# Mostra qual conta Google está autenticada no gcloud.
gcloud auth list --filter=status:ACTIVE --format='value(account)'
```

`PROJECT_ID` é um marcador: substitua pelo identificador real. Confira com calma projeto e conta antes de continuar. `gcloud config set project` altera a configuração ativa do gcloud no seu perfil e ela continua valendo depois que este terminal fecha; não cria um projeto nem muda uma conta Google Ads.

**Checkpoint:** o terminal mostra o ID de projeto correto e a conta Google com as permissões combinadas com a organização. Caso não, corrija a seleção antes de habilitar APIs.

## Checkpoint 3 · habilite APIs usadas pelo roteiro

O comando abaixo altera a configuração do projeto ao habilitar os serviços que o tutorial usa para executar, construir, armazenar a imagem, ler segredos e consultar a API de anúncios. Habilitar uma API não equivale a aprovar acesso de produção à Google Ads API. A criação e o uso dos demais recursos podem gerar cobrança.

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  iam.googleapis.com \
  logging.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  googleads.googleapis.com
```

**Checkpoint:** no Console, confirme que as APIs do roteiro estão habilitadas. Na página de visão geral da Google Ads API, confira também se o projeto tem o nível de acesso desejado. Para produção, não presuma que habilitar a API basta: pode ser preciso solicitar acesso e aguardar aprovação.

## O que este tutorial vai criar

O próximo guia fixa um commit do servidor oficial, prepara uma configuração limitada de ferramentas, constrói uma imagem no Cloud Build e publica o serviço no Cloud Run. Cria identidades separadas: `google-ads-mcp-build` para construir a imagem e `google-ads-mcp-runtime` para executar o serviço com acesso a segredos e armazenamento de estado OAuth em Firestore. Não é preciso instalar Docker no seu computador; o build é feito no Google Cloud e pode ser cobrado.

Antes de autorizar qualquer conta, confira a configuração de ferramentas preparada pelo guia: `customers`, `search` e `metadata` habilitadas; `labels` e `assets` desabilitadas. Se a lista não corresponder, pare antes de conectar uma conta. OAuth e a tela de login não limitam por si só o escopo de acesso à Google Ads API.

## Custos e controle

Cloud Build, Artifact Registry, Cloud Run, Secret Manager, Firestore, Cloud Logging e transferência de dados podem gerar custos. O total depende da região, dos builds, do volume de consultas, do armazenamento e da retenção de registros. Defina um orçamento e acompanhe o faturamento desde o começo; alertas de orçamento avisam, mas não interrompem automaticamente o uso.

Veja as [orientações de custo](../guides/COSTS.md) antes de publicar. Para pausar, remover recursos ou limpar estado, siga a documentação do seu projeto e as instruções de operação; não execute comandos de exclusão copiados sem identificar primeiro cada recurso.

**Próximo:** [02 · Implantação no Cloud Run](DEPLOY.md). O guia de implantação sinaliza quando parar para configurar OAuth antes de publicar.
