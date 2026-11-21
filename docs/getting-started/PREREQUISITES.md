# 01 · Preparar o projeto e conferir os acessos

Use o **Cloud Shell**, terminal Bash do Console do Google Cloud. Ele já inclui as ferramentas usadas pelo roteiro, para você começar pelo navegador.

## O que você precisa

| Item | O que conferir |
| --- | --- |
| Projeto Google Cloud | **ID do projeto**, faturamento habilitado e permissão para criar recursos |
| Google Ads API | Habilitada no mesmo projeto, com nível de acesso adequado a contas de teste ou produção |
| Conta Google Ads | Identidade Google com permissão para consultá-la; acesso via conta de administrador (MCC), se a estrutura de contas exigir |
| OAuth e cliente MCP | Permissão para criar um cliente OAuth web e um cliente MCP compatível com Streamable HTTP e OAuth |

> [!IMPORTANT]
> O acesso de API do projeto e a permissão na conta de anúncios são requisitos distintos. O acesso de produção à API pode precisar de aprovação no Console. Confira os [níveis de acesso atuais](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR) antes de seguir.

Em uma organização, combine as liberações com as equipes de Cloud e Google Ads. Abra o checklist de permissões abaixo com essas equipes antes de criar recursos. Elas podem executar os blocos de criação e IAM por você; a implantação identifica esses momentos.

<details>
<summary>Checklist de permissões para compartilhar com a administração</summary>

A tabela lista as operações usadas pelo roteiro. Peça permissões delimitadas ao laboratório, sem usar Owner como atalho.

| Operação do operador humano | Permissões a conferir | Escopo |
| --- | --- | --- |
| Habilitar e usar APIs | serviceusage.services.enable e serviceusage.services.use | Projeto do laboratório |
| Consultar projeto e banco no checkpoint | resourcemanager.projects.get e datastore.databases.getMetadata | Projeto/banco do laboratório |
| Criar contas de serviço | iam.serviceAccounts.create | Projeto |
| Submeter e acompanhar um build | cloudbuild.builds.create, cloudbuild.builds.get e cloudbuild.builds.list | Projeto |
| Enviar a origem do build | storage.buckets.get e storage.objects.create | Bucket de staging |
| Atuar como as identidades de build e execução | iam.serviceAccounts.actAs | Cada uma das duas contas de serviço |
| Ler a imagem para implantar | artifactregistry.repositories.downloadArtifacts | Repositório de imagens |
| Criar/atualizar e consultar o Cloud Run; configurar sua entrada | run.services.create, run.services.update, run.services.get, run.operations.get e run.services.setIamPolicy | Projeto/serviço do laboratório |
| Criar repositório, bucket, segredos e banco | artifactregistry.repositories.create, storage.buckets.create, secretmanager.secrets.create, secretmanager.versions.add e datastore.databases.create | Projeto e recursos criados |
| Listar versões de segredos no checkpoint | secretmanager.versions.list | Cada um dos três segredos |
| Conceder os acessos do roteiro | getIamPolicy e setIamPolicy do recurso correspondente; resourcemanager.projects.getIamPolicy e resourcemanager.projects.setIamPolicy no projeto | Apenas recursos/projeto do laboratório |
| Aplicar vínculos IAM ao bucket com gcloud | storage.buckets.get, storage.buckets.getIamPolicy, storage.buckets.setIamPolicy e storage.buckets.update | Bucket de origem |

As permissões específicas de comandos do Cloud Storage constam na [tabela oficial do gcloud storage](https://docs.cloud.google.com/storage/docs/access-control/iam-gcloud).

A etapa 4 da implantação inclui os vínculos do operador para build, bucket de origem, leitura da imagem e actAs. As demais permissões de criação precisam estar disponíveis para quem executar os respectivos blocos. A identidade de build recebe leitura da origem, escrita da imagem e dos logs; a de execução recebe acesso aos três segredos e ao Firestore.

Esses vínculos pressupõem um operador confiável em um projeto de laboratório. A permissão `cloudbuild.builds.create` também permite submeter outros builds, inclusive com a conta legada quando disponível; a administração deve revisar os privilégios dessa conta antes de ampliar o uso.

Consulte [identidades de build definidas pelo usuário](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts) e [papéis de implantação no Cloud Run](https://docs.cloud.google.com/run/docs/deploying#required_roles). Políticas da organização podem restringir essas ações mesmo com os papéis IAM concedidos.

</details>

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

# Define o projeto na configuração ativa do gcloud.
gcloud config set project "$PROJECT_ID"

# Mostra o projeto que ficou selecionado; compare o resultado com o Console.
gcloud config get-value project

# Mostra qual conta Google está autenticada no gcloud.
gcloud auth list --filter=status:ACTIVE --format='value(account)'
```

`PROJECT_ID` é um marcador: substitua pelo identificador real. Confira com calma projeto e conta antes de continuar. `gcloud config set project` altera a configuração ativa do gcloud no seu perfil e ela continua valendo depois que este terminal fecha; não cria um projeto nem muda uma conta Google Ads.

**Checkpoint:** o terminal mostra o ID de projeto correto e a conta Google com as permissões combinadas com a organização. Caso não, corrija a seleção antes de habilitar APIs.

## Checkpoint 3 · conferir o acesso à Google Ads API

Abra a visão geral da Google Ads API no Console do projeto e confira o nível de acesso disponível para a conta pretendida. O acesso de produção pode exigir solicitação e aprovação. A [etapa 3 da implantação](DEPLOY.md#3-habilitar-as-apis) reúne o comando de ativação das APIs usadas pelo roteiro.

**Checkpoint:** você definiu se usará uma conta de teste ou produção e encaminhou a liberação de API necessária. Habilitar a API, por si só, não aprova acesso de produção.

## O que vem a seguir

A implantação cria identidades separadas de build e execução, repositório de imagens, bucket de origem, serviço Cloud Run, três segredos e banco Firestore para estado OAuth. O Cloud Build constrói a imagem; você não precisa de Docker no computador.

> [!WARNING]
> Criar e usar esses recursos pode gerar cobrança. Confira os [custos](../guides/COSTS.md) e defina um orçamento antes da implantação. Alertas avisam, mas não interrompem os gastos automaticamente. O [guia de operação](../guides/OPERATIONS.md) orienta a limpeza ao encerrar o laboratório.

**Próximo:** [02 · Implantação no Cloud Run](DEPLOY.md). O guia sinaliza quando configurar OAuth antes de publicar.
