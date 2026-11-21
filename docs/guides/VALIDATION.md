# 04 · Acendeu a luz? Validação do servidor e da consulta

[English](../en/guides/VALIDATION.md) · [Índice](../README.md)

Serviço pronto mostra que o contêiner iniciou. HTTP 401 mostra que uma requisição anônima foi recusada. Login mostra que a autorização avançou. **Só a consulta bem-sucedida comprova acesso à Google Ads API.** Vamos testar separadamente.

## 1. Conferir revisão e endpoint

No Cloud Shell, com as variáveis da [implantação](../getting-started/DEPLOY.md):

~~~bash
gcloud run services describe "$SERVICE" --region="$REGION" \
  --project="$PROJECT_ID" --format='yaml(status.conditions,status.url)'

curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' \
  -X POST -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"anonymous-check","version":"1.0"}}}' \
  "$SERVICE_URL/mcp"
~~~

**Esperado:** revisão pronta e autenticação exigida, normalmente com HTTP 401. Isso ainda não valida Client Secret, callback ou acesso Ads. O exemplo envia uma requisição anônima de um protocolo 2025 que o baseline mantém compatível; não é um cliente completo nem um teste universal para todo protocolo MCP. HTTP 404 pede conferir URL; 5xx pede logs de inicialização; 403 pode vir de IAM/rede antes do OAuth. Não remova autenticação para fazer o teste ficar verde.

## 2. Escolher um cliente

Use cliente instalado com MCP HTTP e OAuth. Acesso a modelos/assistentes pode depender de conta, plano e políticas corporativas. Consulte as [referências oficiais](../REFERENCES.md). Usar ChatGPT como tutor para ler o guia é diferente de conectar um cliente MCP ao servidor.

### VS Code com agentes/Copilot habilitados

No seu computador, abra uma pasta no VS Code. Na paleta de comandos, procure **MCP: Add Server**, escolha HTTP, informe a URL com /mcp e dê um nome à conexão. Para configurar pela pasta, crie .vscode/mcp.json com o exemplo abaixo, substituindo apenas a URL. Não coloque segredos nem tokens nele. Este formato é **do VS Code**, não universal.

~~~json
{
  "servers": {
    "google-ads-mcp": {
      "type": "http",
      "url": "https://SEU-SERVICO.a.run.app/mcp"
    }
  }
}
~~~

Inicie a conexão pelo editor/comando MCP da sua versão. Revise a confiança no servidor e conclua o login Google com o usuário de teste autorizado. No chat de agentes, confira as ferramentas habilitadas e suas aprovações; não habilite execução irrestrita para pular um erro.

### Codex CLI já instalado e autenticado

Execute **no terminal do computador onde o Codex está instalado**, não no Cloud Shell por engano. As variáveis do Cloud Shell não são transferidas para ele.

~~~bash
export SERVICE_URL="https://SEU-SERVICO.a.run.app"
codex mcp add google-ads-mcp --url "$SERVICE_URL/mcp"
codex mcp login google-ads-mcp
codex mcp list
~~~

Se codex não for reconhecido, instale/configure-o pelo guia oficial antes de continuar. Esses comandos cadastram/autenticam a conexão; não consultam ferramentas. Abra uma sessão Codex na sua pasta para os próximos testes.

## 3. Conferir as ferramentas

Peça ao assistente:

> Liste as ferramentas deste servidor. Confirme customers_list_accessible_customers, metadata_get_resource_metadata e search_search. Não consulte dados ainda. Se encontrar ferramentas de criar ativos, enviar vídeos ou alterar rótulos, pare e informe: a configuração de leitura deste guia não está aplicada.

O baseline usa namespaces; versões antigas podem ter nomes diferentes. Ausência de ferramentas de mutação confirma a configuração deste servidor, não uma redução do escopo OAuth nem de todas as permissões da identidade Google.

## 4. Escolher uma conta autorizada

> Execute customers_list_accessible_customers. Mostre os IDs necessários para eu escolher uma conta autorizada. Não tente consultar contas que eu não indicar.

A ferramenta lista contas **diretamente acessíveis** ao usuário Google autenticado, não necessariamente todas as contas-filhas de uma gerenciadora (MCC). Para consultar uma conta-filho, use seu customer_id. Quando necessário, login_customer_id é o ID da gerenciadora pela qual você tem acesso; ambos seguem o schema, sem hífens. Ter um ID não concede permissão.

## 5. Fazer uma consulta pequena

Primeiro consulte metadados de customer, depois customer.id, customer.descriptive_name, customer.currency_code e customer.time_zone. Conheça moeda e fuso antes de interpretar desempenho. A ferramenta metadata_get_resource_metadata informa campos disponíveis; não peça ao modelo que os invente.

Escolha uma conta autorizada, duas datas completas e até dez linhas. Abaixo estão **argumentos para search_search**, não um comando Bash nem uma requisição HTTP completa. Substitua ID e datas. Acrescente login_customer_id somente se seu acesso pela gerenciadora exigir.

~~~json
{
  "customer_id": "1234567890",
  "resource": "campaign",
  "fields": [
    "campaign.id",
    "campaign.name",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros"
  ],
  "conditions": [
    "segments.date BETWEEN '2026-11-01' AND '2026-11-07'"
  ],
  "limit": 10
}
~~~

Prompt para acompanhar:

> Consulte metadados de campaign e confira a compatibilidade dos campos do exemplo. Use conta e datas que eu confirmar. Execute a consulta de leitura com dez linhas no máximo, sem filtro de status atual para este período histórico. Informe moeda e fuso da conta. Mostre cost_micros original e calcule o custo por código dividindo-o por 1.000.000. Não invente números, não misture moedas e não trate dez linhas como o total da conta. Se não houver linhas, explique que resultado vazio pode ser válido e proponha como verificar conta, período e atividade.

**Checkpoint:** confira uma campanha no Google Ads com a mesma conta, período e fuso. Métricas atribuídas pela plataforma não equivalem a cadastros únicos em outro banco; consulta descritiva não demonstra causalidade. Dez linhas servem para validar, não para produzir um relatório completo.

## 6. Registrar o que realmente aconteceu

| Etapa | Evidência sem segredos |
| --- | --- |
| Build | Commit upstream, ID do build e digest da imagem |
| Serviço | Revisão pronta e URL base |
| Anônimo | Código HTTP e data; sem tokens/cabeçalhos de autorização |
| OAuth | Login concluído; sem copiar credenciais |
| Ferramentas | Três ferramentas de leitura presentes; mutações ausentes |
| Contas | Identidade/permissões conferidas; IDs ocultados ao compartilhar |
| Consulta | Campos, período, linhas, moeda e fuso conferidos |
| Resultado | Sucesso, vazio coerente ou erro diagnosticado; nunca “passou” sem executar |

Escala a zero, reinícios e novas revisões podem encerrar sessões MCP/streams HTTP mesmo com OAuth persistente no Firestore. Reconecte o cliente; não apague segredos ou banco para recuperar uma sessão. Se falhar, use [solução de problemas](TROUBLESHOOTING.md).

[← OAuth](OAUTH-AND-SECRETS.md) · [Erros e diagnóstico →](TROUBLESHOOTING.md)

