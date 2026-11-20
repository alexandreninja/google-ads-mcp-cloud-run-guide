# 02 · Implantação no Google Cloud Run

Guia de comandos parametrizados para o [Google Ads MCP oficial](https://github.com/googleads/google-ads-mcp). Execute a partir do diretório do código upstream, não deste repositório de documentação.

## 1. Definir variáveis

```bash
export PROJECT_ID="SEU_PROJECT_ID"
export REGION="us-central1"
export REPOSITORY="mcp-servers"
export SERVICE="google-ads-mcp"
export RUNTIME_SA="google-ads-mcp-runtime"

gcloud config set project "$PROJECT_ID"
```

## 2. Criar o Artifact Registry

```bash
gcloud artifacts repositories create "$REPOSITORY" \
  --repository-format=docker \
  --location="$REGION" \
  --description="Container images for MCP services"
```

Se o repositório já existir, ignore esta criação.

## 3. Construir e publicar a imagem

```bash
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${SERVICE}:guide-v1"

gcloud builds submit --tag "$IMAGE" .
```

Para ambientes controlados, registre o digest da imagem e a tag/commit exato do upstream.

## 4. Criar identidade de execução

```bash
gcloud iam service-accounts create "$RUNTIME_SA" \
  --display-name="Google Ads MCP Runtime"

export RUNTIME_SA_EMAIL="${RUNTIME_SA}@${PROJECT_ID}.iam.gserviceaccount.com"
```

A conta poderá precisar de permissões adicionais conforme o armazenamento do estado OAuth e a versão utilizada. Conceda apenas as necessárias.

## 5. Configurar OAuth e segredos

Antes do deploy, siga [03 · OAuth e Secret Manager](../guides/OAUTH-AND-SECRETS.md). O servidor HTTP necessita de Client ID, Client Secret e configuração de URL pública. Use o Secret Manager para valores secretos.

## 6. Deploy inicial

O exemplo usa acesso HTTP público **à entrada do servidor OAuth**; isso não libera dados do Google Ads sem autenticação.

```bash
export OAUTH_CLIENT_ID="SEU_CLIENT_ID_PUBLICO"

gcloud run deploy "$SERVICE" \
  --image="$IMAGE" \
  --region="$REGION" \
  --platform=managed \
  --service-account="$RUNTIME_SA_EMAIL" \
  --allow-unauthenticated \
  --min-instances=0 \
  --max-instances=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_ADS_MCP_OAUTH_CLIENT_ID=${OAUTH_CLIENT_ID}" \
  --set-secrets="GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET=google-ads-mcp-oauth-client-secret:latest,GOOGLE_ADS_MCP_JWT_SIGNING_KEY=google-ads-mcp-jwt-signing-key:latest"
```

**Antes de executar:** crie os segredos e conceda à conta de serviço do Cloud Run acesso estritamente aos segredos requeridos. O comando pressupõe esses recursos já configurados.

## 7. Configurar a URL pública

```bash
export SERVICE_URL="$(gcloud run services describe "$SERVICE" \
  --region="$REGION" --format='value(status.url)')"

printf '%s\n' "$SERVICE_URL"

gcloud run services update "$SERVICE" \
  --region="$REGION" \
  --update-env-vars="GOOGLE_ADS_MCP_BASE_URL=${SERVICE_URL}"
```

Registre as URLs de redirecionamento OAuth exatas exigidas pelo servidor e pelo cliente na configuração do Google Cloud. Confira o callback na versão upstream utilizada antes de autorizar URIs.

## 8. Validar o servidor

```bash
gcloud run services describe "$SERVICE" --region="$REGION"

curl --silent --show-error --output /dev/null \
  --write-out '%{http_code}\n' "${SERVICE_URL}/mcp"
```

Uma resposta `401` sem login **pode ser esperada**. Conclua o fluxo OAuth com um cliente compatível antes de testar consultas.

Para uso continuado, configure **persistência de estado OAuth** adequada à sua versão upstream (por exemplo, Firestore/Redis quando suportado). Em Cloud Run, filesystem temporário não é armazenamento durável.

**Próximo:** [04 · Validação](../guides/VALIDATION.md).
