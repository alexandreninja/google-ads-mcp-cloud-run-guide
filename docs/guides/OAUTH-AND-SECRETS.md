# 03 · OAuth 2.0 e Secret Manager

## 1. Criar o cliente OAuth

No Google Cloud Console, prepare um cliente OAuth compatível com o fluxo web utilizado pelo servidor.

- Registre o Client ID.
- Guarde o Client Secret fora do repositório.
- Cadastre as **redirect URIs exatas** exigidas pelo servidor e pelos clientes que serão conectados.
- Confirme a URL de callback na versão do [Google Ads MCP](https://github.com/googleads/google-ads-mcp) que você fixou.

## 2. Criar os segredos

Exemplo de nomes (não são credenciais):

- `google-ads-mcp-oauth-client-secret`
- `google-ads-mcp-jwt-signing-key`

```bash
gcloud secrets create google-ads-mcp-oauth-client-secret \
  --replication-policy="automatic"

gcloud secrets create google-ads-mcp-jwt-signing-key \
  --replication-policy="automatic"
```

Adicione as versões com o mecanismo seguro de sua preferência. Evite valores em comandos copiados, variáveis de shell compartilhadas, arquivos versionados e histórico.

## 3. Conceder acesso à conta de serviço

```bash
export PROJECT_ID="SEU_PROJECT_ID"
export RUNTIME_SA_EMAIL="google-ads-mcp-runtime@${PROJECT_ID}.iam.gserviceaccount.com"

for SECRET in google-ads-mcp-oauth-client-secret google-ads-mcp-jwt-signing-key; do
  gcloud secrets add-iam-policy-binding "$SECRET" \
    --member="serviceAccount:${RUNTIME_SA_EMAIL}" \
    --role="roles/secretmanager.secretAccessor"
done
```

## 4. Variáveis da aplicação

| Variável | Origem |
| --- | --- |
| `GOOGLE_ADS_MCP_OAUTH_CLIENT_ID` | ID do cliente OAuth |
| `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET` | Secret Manager |
| `GOOGLE_ADS_MCP_BASE_URL` | URL HTTPS pública do serviço |
| `GOOGLE_ADS_MCP_JWT_SIGNING_KEY` | Secret Manager |
| `GOOGLE_ADS_MCP_STORAGE_TYPE` | Backend compatível com sua versão |

O escopo Google Ads pode autorizar operações mais amplas que as ferramentas expostas. Ajuste a disponibilidade das ferramentas no servidor conforme a versão e revise IAM/OAuth separadamente.

## 5. Checklist

- [ ] Redirect URIs autorizadas corretamente.
- [ ] Serviço utiliza a versão correta dos segredos.
- [ ] Conta de serviço tem somente os acessos necessários.
- [ ] URL base confere com o endpoint publicado.
- [ ] Persistência de OAuth preparada se houver uso contínuo ou múltiplas instâncias.

[← Deploy](../getting-started/DEPLOY.md) · [Próximo: validação →](VALIDATION.md)
