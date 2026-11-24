# 03 · OAuth e segredos: identificar, autorizar e guardar

[English](../en/guides/OAUTH-AND-SECRETS.md) · [Índice](../README.md)

Pense em três objetos: o Client ID identifica a aplicação; o Client Secret é uma credencial confidencial dela; o consentimento autoriza o acesso de uma pessoa às suas contas Google Ads. A conta de serviço do Cloud Run acessa Firestore e Secret Manager, mas não ganha acesso às contas de anúncios por existir no Google Cloud.

Esta página entra na etapa 6 da [implantação](../getting-started/DEPLOY.md). PROJECT_ID e RUNTIME_SA_EMAIL já precisam estar definidos. Use **o mesmo projeto para OAuth e execução** neste laboratório: o nível de acesso à Google Ads API é vinculado ao projeto que emite as credenciais OAuth.

## Antes do deploy: preparar o aplicativo Google

1. No Console do projeto, abra **Google Auth Platform**. Em interfaces anteriores: **APIs e serviços → Tela de consentimento OAuth**.
2. Em **Branding/Marca**, defina nome reconhecível, e-mail de suporte e contato. Não use uma marca institucional sem autorização.
3. Em **Audience/Público-alvo**, selecione o tipo permitido. Para laboratório pessoal externo, mantenha **Testing/Teste** e adicione seu e-mail como usuário de teste. **Internal/Interno** só se aplica às organizações Google Workspace que permitam esse uso.
4. Em **Data Access/Acesso a dados**, confira os escopos requeridos pelo upstream: openid, https://www.googleapis.com/auth/userinfo.email, https://www.googleapis.com/auth/userinfo.profile e https://www.googleapis.com/auth/adwords. O último **não é um escopo exclusivamente de leitura**. Verificações podem ser exigidas conforme público, uso e política da organização.
5. Em **Clients/Clientes**, crie um cliente **Web application/Aplicativo da Web**. Guarde Client ID e Client Secret de modo seguro. A URL final ainda não existe: crie o cliente e complete a URI de redirecionamento depois do deploy. Não escolha aplicativo para computador para este fluxo web.

~~~bash
# O Client ID não é o segredo; substitua pelo identificador da sua aplicação.
export OAUTH_CLIENT_ID="SEU_CLIENT_ID.apps.googleusercontent.com"
~~~

**Checkpoint:** cliente web no projeto certo, público delimitado e identidade com acesso à conta Google Ads escolhida. Consentimento não concede um nível de acesso à API que o projeto ainda não tenha.

## Criar segredos com valores, sem gravá-los no histórico

> [!WARNING]
> Execute no **Bash do Cloud Shell**, sem gravação ou compartilhamento de tela e sem `set -x`. O `read -s` recebe o segredo sem exibi-lo. Mantenha credenciais fora de chats, issues, arquivos versionados e argumentos de comandos.

~~~bash
read -r -s -p "OAuth Client Secret: " TASK_OAUTH_SECRET
printf '\n'
printf '%s' "$TASK_OAUTH_SECRET" | gcloud secrets create \
  google-ads-mcp-oauth-client-secret --data-file=- \
  --replication-policy=automatic --project="$PROJECT_ID"
unset TASK_OAUTH_SECRET

# Gera chaves aleatórias e as envia ao Secret Manager sem exibi-las.
python3 -c 'import secrets; print(secrets.token_urlsafe(48), end="")' | \
  gcloud secrets create google-ads-mcp-jwt-signing-key --data-file=- \
  --replication-policy=automatic --project="$PROJECT_ID"
python3 -c 'import secrets; print(secrets.token_urlsafe(48), end="")' | \
  gcloud secrets create google-ads-mcp-storage-key --data-file=- \
  --replication-policy=automatic --project="$PROJECT_ID"

for SECRET_NAME in google-ads-mcp-oauth-client-secret google-ads-mcp-jwt-signing-key google-ads-mcp-storage-key; do
  gcloud secrets add-iam-policy-binding "$SECRET_NAME" \
    --member="serviceAccount:$RUNTIME_SA_EMAIL" \
    --role=roles/secretmanager.secretAccessor --project="$PROJECT_ID"
  gcloud secrets versions list "$SECRET_NAME" \
    --filter='state:ENABLED' --format='value(name)' --project="$PROJECT_ID"
done
~~~

**Checkpoint antes do deploy:** os três nomes existem e têm a versão **1** habilitada; a identidade de execução pode acessá-los. A listagem mostra metadados, não conteúdo. Se algum segredo já existia, pare e confira sua versão: não sobrescreva automaticamente. O deploy fixa :1; use outro número apenas depois de revisar a configuração.

A chave JWT mantém assinaturas consistentes entre reinícios. A chave de armazenamento protege registros OAuth no backend. Trocar essas chaves afeta autorizações/sessões guardadas; veja [rotação em operação](OPERATIONS.md).

**Volte agora à etapa 7 da implantação.** A próxima seção depende da SERVICE_URL atribuída pelo Cloud Run.

## Depois do deploy: cadastrar o callback

~~~bash
# Exibe somente a URI de redirecionamento; não contém credenciais.
printf '%s/auth/callback\n' "$SERVICE_URL"
~~~

> [!IMPORTANT]
> No cliente OAuth web, adicione a saída exata em **Authorized redirect URIs/URIs de redirecionamento autorizadas** e salve. O callback do servidor é `/auth/callback`; o endpoint do cliente MCP é `/mcp`. Use cada endereço no campo correspondente abaixo.

| Endereço | Uso |
| --- | --- |
| SERVICE_URL | URL base HTTPS, sem /mcp |
| SERVICE_URL/auth/callback | Callback do servidor cadastrado no OAuth Google |
| SERVICE_URL/mcp | Endpoint informado ao cliente MCP |
| Callback local do VS Code/Codex | Gerenciado pelo cliente e pelo proxy; não cadastre portas aleatórias no OAuth Google deste roteiro |

Se a interface exigir origem JavaScript, use a URL base HTTPS, sem caminho. Origem não substitui URI de redirecionamento. Esquema, hostname, caminho e barra final precisam coincidir; divergências causam redirect_uri_mismatch.

> [!NOTE]
> Aplicativos externos em Testing podem emitir refresh tokens com expiração de sete dias quando pedem escopos além de identidade básica; este servidor pede adwords. Nova autorização pode ser necessária. Sair de Testing exige revisar público, verificação e governança, não apenas mudar um seletor. Consulte as [referências oficiais](../REFERENCES.md) se interface ou política mudar.

**Checkpoint final:** a URL base configurada no Cloud Run e o callback cadastrado apontam para o mesmo serviço. Faça a [validação com um cliente](VALIDATION.md).

[← Implantação](../getting-started/DEPLOY.md) · [Validação →](VALIDATION.md)


A chave de criptografia do armazenamento é distinta da chave de assinatura JWT. Mantenha sua versão estável entre revisões. Não a imprima para conferir persistência. Veja [persistência OAuth](OAUTH-PERSISTENCE.md).
