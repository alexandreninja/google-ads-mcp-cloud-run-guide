# OAuth 2.0, Secret Manager e acesso

## 1. Identidades e autorização

Defina quem pode acessar o cliente MCP, o endpoint Cloud Run e as contas Google Ads. As permissões da API dependem do usuário autenticado e do escopo OAuth. **A ferramenta de leitura não torna o escopo `adwords` exclusivamente de leitura.**

## 2. OAuth remoto

No modo HTTP do servidor oficial, revise as variáveis e os fluxos OAuth do upstream:

- `GOOGLE_ADS_MCP_OAUTH_CLIENT_ID`: identificador do cliente OAuth.
- `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET`: segredo — **armazenar no Secret Manager**.
- `GOOGLE_ADS_MCP_BASE_URL`: URL pública correta do serviço.
- `GOOGLE_ADS_MCP_JWT_SIGNING_KEY`: chave de assinatura persistente quando aplicável.
- Estratégia de persistência do estado OAuth e sua criptografia.

Registre as **redirect URIs exatas** esperadas. Evite publicar URLs reais do serviço ou de callbacks particulares.

## 3. Secret Manager

Crie os segredos em projeto autorizado com IAM mínimo. Prefira uma versão explícita e registre revisões. Não digite valores em shell history, issues ou arquivos versionados.

Valide que a identidade do Cloud Run possui permissão de acesso somente aos segredos necessários. Substituir uma versão exige atualizar a referência efetivamente usada pelo serviço e verificar o novo deploy.

## 4. Estado OAuth

Em serviços de escala a zero, processos e filesystem efêmero não são armazenamento durável. Para uso contínuo/multi-instância, planeje backend persistente adequado; consulte os backends documentados pelo upstream, incluindo Firestore ou Redis, e respectivas permissões e custos.

## 5. Verificação

Faça testes anônimos negativos, fluxo de login autorizado, descoberta de ferramentas e consulta a uma conta própria/de teste. Confira logs **sem imprimir tokens**.

Próximo: [Validação](VALIDATION.md).
