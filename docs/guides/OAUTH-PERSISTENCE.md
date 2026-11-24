# Persistência OAuth: migrar de memória para Firestore

[English](../en/guides/OAUTH-PERSISTENCE.md) · [Índice](../README.md)

## Por que o login se perde?

Cloud Run conserva a configuração do serviço, não a memória do processo. Quando o servidor usa `GOOGLE_ADS_MCP_STORAGE_TYPE=memory`, a troca de instância pode apagar o estado necessário para usar a autorização. A autorização Google e a sessão HTTP MCP têm ciclos de vida distintos. Firestore preserva o estado OAuth; não preserva streams HTTP ou impede revogação de tokens.

## 1. Inventário e pré-requisitos

Este roteiro migra um serviço existente; para instalação nova, siga [DEPLOY](../getting-started/DEPLOY.md). Use um ambiente autorizado, revise [custos](COSTS.md) e tenha um rollback. Execute comandos individualmente, interrompendo em caso de erro. Defina PROJECT_ID, REGION, SERVICE, RUNTIME_SA_EMAIL (identidade de execução, não de build), IMAGE (nova imagem preparada), STORAGE_SECRET (nome do segredo dedicado) e PREVIOUS_REVISION (revisão anterior pronta) com seus próprios valores. Não publique IDs, tokens, logs brutos nem nomes internos.

~~~bash
gcloud run services describe "$SERVICE" --project="$PROJECT_ID" --region="$REGION" --format='value(status.latestReadyRevisionName,spec.template.spec.serviceAccountName,spec.template.spec.containers[0].image)'
gcloud firestore databases list --project="$PROJECT_ID"
~~~

Confira a configuração de armazenamento no Console sem revelar valores de segredos. Se a API Firestore estiver desabilitada, habilite-a somente com autorização.

## 2. Banco e IAM

Somente se não existir banco adequado, crie o banco abaixo. Escolha localização antes da criação. O primeiro banco elegível pode ter franquia gratuita; verifique freeTier no retorno. Não habilite backups/PITR/TTL gerenciado sem avaliar custos.

~~~bash
gcloud firestore databases create --project="$PROJECT_ID" --database='(default)' --location="$REGION" --type=firestore-native --delete-protection
~~~

Conceda acesso de dados condicionado ao banco:

~~~bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$RUNTIME_SA_EMAIL" --role=roles/datastore.user \
  --condition="expression=resource.name==\"projects/$PROJECT_ID/databases/(default)\",title=McpFirestoreAccess,description=OAuth persistent storage"
~~~

Essa condição não isola coleções no mesmo banco. Não conceda papéis administrativos amplos para corrigir erros. Confira o acesso efetivo durante a autenticação.

## 3. Preparar a imagem e a chave

O pacote 0.0.6 oferece o extra Firestore. Use o helper do guia em um clone limpo do commit fixado ou revise o Dockerfile da implantação existente; substitua apenas a instalação por `RUN uv pip install --system ".[firestore]"`. Preserve o perfil read-only, as demais adaptações e a imagem anterior. Construa com uma tag nova conforme [DEPLOY](../getting-started/DEPLOY.md). Confira o sucesso e registre o digest. Não envie credenciais no contexto de build.

Se ainda não houver uma chave dedicada, gere-a diretamente no Secret Manager (não execute novamente se o segredo já existir; confira a versão e preserve a chave existente).

~~~bash
python3 -c 'import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(),end="")' | \
  gcloud secrets create "$STORAGE_SECRET" --project="$PROJECT_ID" --replication-policy=automatic --data-file=-
gcloud secrets add-iam-policy-binding "$STORAGE_SECRET" --project="$PROJECT_ID" \
  --member="serviceAccount:$RUNTIME_SA_EMAIL" --role=roles/secretmanager.secretAccessor
~~~

A chave Fernet protege o conteúdo OAuth em nível de aplicação; preserve-a entre revisões, separada da chave JWT. Use a versão correta do segredo no deploy. A rotação ou perda da chave pode invalidar o estado persistido.

## 4. Migrar sem substituir outras configurações

Confira IMAGE e STORAGE_SECRET; o exemplo pressupõe versão 1 habilitada. Preserve URL base, OAuth Client ID, Client Secret, chave JWT, conta de serviço, perfil de ferramentas e limites de execução.

~~~bash
gcloud run services update "$SERVICE" --project="$PROJECT_ID" --region="$REGION" \
  --image="$IMAGE" \
  --update-env-vars="GOOGLE_ADS_MCP_STORAGE_TYPE=firestore,GOOGLE_ADS_MCP_STORAGE_FIRESTORE_PROJECT=$PROJECT_ID,GOOGLE_ADS_MCP_STORAGE_FIRESTORE_DATABASE=(default)" \
  --update-secrets="GOOGLE_ADS_MCP_STORAGE_ENCRYPTION_KEY=$STORAGE_SECRET:1"
~~~

Aguarde revisão pronta e confira tráfego. Reconecte o cliente uma vez: o estado anterior em memória não é migrado automaticamente.

## 5. Testar a persistência

Liste as contas autorizadas pela ferramenta customers_list_accessible_customers. No Firestore Studio, confira a presença das coleções mcp-jti-mappings, mcp-refresh-tokens e mcp-upstream-tokens. O formato __encrypted_data__ foi observado em um registro de mapeamento JTI; não abra ou copie conteúdo secreto. A expiração de um registro não garante validade da autorização Google.

Em janela de manutenção, crie outra revisão mantendo a mesma imagem e chaves. A variável abaixo é apenas um marcador de teste.

~~~bash
gcloud run services update "$SERVICE" --project="$PROJECT_ID" --region="$REGION" \
  --update-env-vars="OAUTH_PERSISTENCE_TEST=$(date -u +%Y%m%dT%H%M%SZ)"
~~~

Confirme que a nova revisão recebe 100% do tráfego. Sem reconectar OAuth manualmente, repita a consulta. O cliente pode precisar restabelecer o transporte MCP automaticamente. Registre sucesso ou erro e teste separadamente a renovação após expiração do access token. Verifique se o aplicativo OAuth está em modo de teste, que pode limitar a duração de refresh tokens.

## 6. Rollback

Se necessário, direcione tráfego à revisão anterior após verificar que ela continua disponível e segura.

~~~bash
gcloud run services update-traffic "$SERVICE" --project="$PROJECT_ID" --region="$REGION" \
  --to-revisions="$PREVIOUS_REVISION=100"
~~~

Se a revisão anterior usava memória, será possível precisar de nova autorização. Não apague banco ou chaves como parte do rollback.

## Evidência e limites

Em 24/11/2026, uma implantação existente do pacote 0.0.6, commit upstream 7452a9d49e3d350403f2610cd7125c60f6d05264, foi migrada de memory para Firestore; build e deploy concluídos, três ferramentas de leitura preservadas, registros observados no banco, e duas contas retornadas antes e depois de uma nova revisão sem reconexão manual reportada. Isso demonstra continuidade de acesso entre revisões naquele experimento, não comprova renovação após expiração, persistência de todos os tipos de registro, compatibilidade de todos os clientes ou custo zero. O commit fixado no guia original é distinto; não afirmamos que o roteiro integral daquele commit foi executado.

Fontes: [implementação de storage testada](https://github.com/googleads/google-ads-mcp/blob/7452a9d49e3d350403f2610cd7125c60f6d05264/ads_mcp/auth_storage.py), [Firestore pricing](https://cloud.google.com/firestore/pricing), [Cloud Run](https://cloud.google.com/run/docs).

[Validação](VALIDATION.md) · [Operação](OPERATIONS.md)
