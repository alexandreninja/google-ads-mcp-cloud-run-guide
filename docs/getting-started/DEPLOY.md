# Guia de implantação — ambiente de teste

> [!IMPORTANT]
> Roteiro de estudo parametrizado, não um instalador pronto e homologado. Confirme a versão upstream, quotas, políticas, custos e permissões antes de executar.

## 1. Obter e fixar a versão oficial

```bash
git clone https://github.com/googleads/google-ads-mcp.git
cd google-ads-mcp
git tag --list
# Escolha uma tag ou commit e registre-o antes do build.
```

Não use automaticamente `main` em produção. Confirme a compatibilidade das instruções com a revisão escolhida.

## 2. Preparar o Google Cloud

```bash
export GOOGLE_CLOUD_PROJECT='SEU_PROJECT_ID'
export REGION='us-central1'
export REPOSITORY='mcp-servers'
export SERVICE='google-ads-mcp'

gcloud config set project "$GOOGLE_CLOUD_PROJECT"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com \
  googleads.googleapis.com
```

Habilitar APIs e criar recursos pode gerar custos.

## 3. Construir a imagem

```bash
# Rode somente se o repositório ainda não existir.
gcloud artifacts repositories create "$REPOSITORY" \
  --repository-format=docker --location="$REGION"

export IMAGE="${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${REPOSITORY}/${SERVICE}:experiment"
gcloud builds submit --tag "$IMAGE" .
```

A tag `experiment` pode ser sobrescrita. Prefira digest imutável em ambientes controlados.

## 4. Configurar OAuth e segredos

Consulte [OAuth e Secret Manager](../guides/OAUTH-AND-SECRETS.md). Evite `--set-env-vars` para conteúdo confidencial. Use referências ao Secret Manager e verifique IAM.

## 5. Implantar e validar

Configure OAuth, segredos, chave JWT persistente quando aplicável, conta de serviço, URL de callback e estratégia de estado OAuth. Algumas variáveis dependem da URL final do Cloud Run e exigem atualização após o primeiro deploy.

Use a sintaxe de deploy do [upstream](https://github.com/googleads/google-ads-mcp#google-cloud-run-deployment) como referência para sua versão; **não copie valores de credenciais em texto claro** para comandos ou históricos compartilhados.

Depois, siga [validação](../guides/VALIDATION.md) e [troubleshooting](../guides/TROUBLESHOOTING.md).

> [!WARNING]
> Este roteiro intencionalmente não é um deploy one-click: autenticação, estado OAuth e controles institucionais exigem decisões específicas de cada ambiente.
