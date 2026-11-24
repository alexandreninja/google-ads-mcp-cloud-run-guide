# Glossário

Use este glossário como mapa entre os termos do Cloud e do Google Ads. Uma analogia ajuda a lembrar a função; o texto entre parênteses nomeia o mecanismo real.

| Termo | Em palavras simples | O que significa neste guia |
| --- | --- | --- |
| **MCP** | Um padrão de conexão entre um cliente de IA e ferramentas. | O Model Context Protocol define como o cliente descobre e chama ferramentas oferecidas pelo servidor. O modelo escolhe se e quando chamar uma ferramenta, conforme o cliente e a política de uso. |
| **Cliente MCP** | O aplicativo que conversa com o servidor. | Um cliente compatível recebe a URL `/mcp`, conclui a autenticação e mostra as ferramentas disponíveis. |
| **Servidor Google Ads MCP** | A ponte entre o cliente e a API. | O programa oficial `googleads/google-ads-mcp`, hospedado neste tutorial no Cloud Run. Ele fornece ferramentas; não contém suas campanhas. |
| **Google Ads API** | A fonte oficial dos dados e ações de anúncios. | A API do Google que o servidor consulta. O projeto Cloud precisa estar habilitado e ter o nível de acesso adequado; a identidade autenticada também precisa ter permissão nas contas. |
| **Cloud Run** | O lugar onde o serviço HTTP fica disponível. | Plataforma gerenciada do Google Cloud que executa o contêiner e entrega uma URL HTTPS. As instâncias podem iniciar e parar; o sistema de arquivos temporário não é um lugar durável para guardar estado. |
| **Cloud Shell** | Um terminal aberto dentro do Console do Google Cloud. | O Bash usado pelo roteiro para executar `gcloud`, Git e scripts de preparação sem instalar Docker no computador. Os comandos ainda alteram o projeto remoto quando assim descrito. |
| **Cloud Build** | Uma oficina que monta o pacote em outro computador. | Serviço que constrói a imagem do servidor a partir do código e a envia ao Artifact Registry. Builds podem gerar cobrança. |
| **Imagem de contêiner** | Um pacote que reúne o programa e o que ele precisa para rodar. | Artefato criado pelo build e executado no Cloud Run. Uma tag é um rótulo; o digest identifica o conteúdo publicado com mais precisão. |
| **Artifact Registry** | Uma prateleira privada para os pacotes construídos. | Serviço que armazena a imagem do contêiner que o Cloud Run usará. |
| **Projeto Google Cloud / ID do projeto** | A pasta administrativa e seu identificador. | Projeto onde ficam serviços, permissões, faturamento e dados de configuração. O ID usado em comandos é diferente do nome exibido para pessoas no Console. |
| **Região** | A área geográfica onde o recurso será hospedado. | Região escolhida para Cloud Run, Artifact Registry e demais recursos regionais. A escolha afeta disponibilidade, latência e preço. |
| **Faturamento** | A conta que paga pelos recursos utilizados. | O projeto precisa estar associado a uma conta de faturamento para usar os serviços deste tutorial. Ativar alertas de orçamento não cria um teto automático de gasto. |
| **OAuth 2.0** | O fluxo de login e autorização do usuário. | O cliente inicia o login Google e recebe autorização para a aplicação. O servidor usa esse fluxo para acessar a Google Ads API em nome da pessoa autenticada, conforme suas permissões. |
| **Callback / URI de redirecionamento OAuth** | O endereço para onde o Google retorna depois do login. | No commit de referência deste guia, é `${SERVICE_URL}/auth/callback`. O cliente MCP faz outro salto por meio do proxy; cadastre a URI do servidor, não um callback local do cliente. |
| **OAuth Client ID** | O identificador público da aplicação de login. | Valor usado para identificar o cliente OAuth. Não é senha, embora ainda deva ser configurado apenas na aplicação correta. |
| **OAuth Client Secret** | A senha da aplicação OAuth. | Valor confidencial. Guarde-o no Secret Manager; não cole em documentação, prompt, repositório ou histórico do terminal. |
| **Identidade do usuário Google** | A pessoa que conclui o login. | É quem autentica a sessão usada pelo servidor para o acesso ao Ads. A API só pode retornar dados que essa pessoa pode acessar. |
| **Conta de serviço** | A identidade técnica do próprio serviço Cloud. | Identidade que o Cloud Run usa para ler segredos e gravar estado OAuth. Não é a pessoa que acessa Google Ads e não substitui o login OAuth do usuário. |
| **IAM** | As regras de quem pode fazer o quê no Cloud. | Identity and Access Management controla ações sobre recursos Google Cloud; por exemplo, qual conta de serviço pode ler um segredo. É distinto das permissões de uma pessoa dentro do Google Ads. |
| **Secret Manager** | Um cofre para valores confidenciais. | Serviço usado para guardar segredos e controlar qual identidade de execução pode lê-los. No deploy, referencie o segredo; não imprima o valor. |
| **Firestore** | Um banco gerenciado que mantém estado entre reinicializações. | Neste guia, guarda estado OAuth persistente para o serviço não depender do disco temporário de uma instância Cloud Run. Precisa ser preparado e ter acesso IAM apropriado. |
| **Estado OAuth** | A memória de trabalho do fluxo de login. | Informações de sessão e tokens que o servidor precisa manter entre solicitações. O backend persistente deve ser compatível com a versão fixada do servidor. |
| **Streamable HTTP** | O formato MCP transportado por HTTPS. | Mecanismo usado pelo cliente e pelo servidor remoto para trocar solicitações e respostas no caminho `/mcp`. |
| **Endpoint** | O endereço por onde se fala com o serviço. | Neste guia, é a URL do Cloud Run acrescida de `/mcp`, por exemplo `https://seu-servico.../mcp`. Use a URL exata publicada para configurar OAuth e o cliente. |
| **MCC / conta de administrador** | Uma conta de Ads que administra outras contas. | É necessária apenas se o arranjo de acesso da organização depender dela. A listagem de clientes acessíveis não garante que todas as contas filhas da MCC serão exibidas; o campo `login_customer_id` só se aplica a fluxos que passam por uma conta de administrador. |
| **Nível de acesso da Google Ads API** | A catraca que define em quais ambientes o projeto pode operar. | A ativação da API concede acesso de teste. Para contas de produção, confira o nível e os requisitos atuais na visão geral da Google Ads API no Console do Cloud; pode haver solicitação e aprovação. |
| **Developer token** | Uma credencial de API usada pelo modelo anterior de acesso. | A Google aposentou o fluxo de novos tokens em 9 de setembro de 2026 e transferiu a gestão de acesso para o projeto Cloud. Um commit antigo pode ainda mencionar a variável ou aceitar credenciais existentes; siga a documentação do commit e a orientação oficial atual. |
| **`tools_config.yaml` / allowlist** | A lista do que o servidor pode oferecer ao cliente. | Configuração da versão do servidor que inclui ou exclui ferramentas. Neste guia, `customers`, `search` e `metadata` ficam habilitadas; `labels` e `assets` ficam desabilitadas. Confira essa configuração na imagem antes de conectar uma conta. OAuth não define essa lista nem reduz as permissões do usuário. |
| **GAQL** | A linguagem de consulta da Google Ads API. | Google Ads Query Language especifica quais recursos, campos e períodos são consultados. A consulta precisa corresponder aos campos e permissões disponíveis. |
| **Quota** | O limite de uso de um serviço ou API. | Google Cloud e Google Ads API controlam quantas operações ou recursos podem ser usados. Erros de quota não são corrigidos apenas reiniciando o servidor. |
| **Homologação** | O ensaio formal antes do uso real. | Validação com ambiente, ferramentas, acessos, registros e controles aprovados pela organização. Reproduzir este tutorial não equivale a homologar nem certifica prontidão para produção. |
| **TCO** | O custo total ao longo do tempo. | Total Cost of Ownership: infraestrutura, manutenção, monitoramento, segurança, suporte e tempo da equipe, além da cobrança de cada serviço. |

### Persistência na prática

- **Fernet:** criptografia autenticada em nível de aplicação do conteúdo OAuth armazenado.
- **Revisão:** configuração imutável de implantação do Cloud Run; um novo processo não herda a memória anterior.
- **Persistência:** guardar estado fora do processo. Não garante autorização sem expiração.

**Próximo:** [Índice da documentação](README.md) · [Arquitetura](ARCHITECTURE.md) · [Tutor de IA](guides/AI-TUTOR.md)
