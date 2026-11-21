# Google Ads MCP no Google Cloud Run

<p align="center">
  <img src="docs/assets/github-header.svg" alt="Cliente MCP conectado ao servidor Google Ads MCP no Cloud Run e à Google Ads API" width="100%">
</p>

Você quer responder “quais campanhas consumiram mais orçamento nos últimos 30 dias — e como confirmar os dados?”. Este tutorial mostra como hospedar no Google Cloud Run o servidor oficial [Google Ads MCP](https://github.com/googleads/google-ads-mcp). O cliente de IA envia pedidos por HTTPS; o Cloud Run executa o servidor MCP, que consulta a Google Ads API com o acesso autorizado. Cada etapa tem um checkpoint para você saber o que já funciona.

O código do servidor pertence ao projeto oficial do Google. Este repositório explica uma implantação; não é um produto oficial do Google nem uma promessa de que qualquer conta estará pronta para produção. Nomes de configuração e requisitos podem mudar entre versões.

Para esta revisão, o roteiro parte do commit upstream `44ca7770519362c8f334875477e1ceb499f8d2dd` (pacote 0.0.6). É um commit auditado para este guia, não uma afirmação de release estável. O guia de implantação registra o que muda na preparação da imagem.

## O que você terá ao concluir

Você poderá obter a URL HTTPS do serviço e conectar um cliente compatível com MCP ao caminho `/mcp`. Os checkpoints ajudam a confirmar, nesta ordem, que o Cloud Run publicou o serviço, que o acesso anônimo é recusado quando OAuth está ativo, que o cliente concluiu o login e descobriu as ferramentas, e que uma consulta autorizada à Google Ads API retornou os dados esperados.

Um `401` no teste sem login pode ser normal, mas sozinho não prova que OAuth ou a consulta de anúncios funcionam. A validação completa exige um cliente MCP, uma identidade Google com acesso à conta e uma consulta autorizada. Este tutorial não afirma que uma implantação nova foi executada ou testada na nuvem.

## Quatro verificações antes de começar

Resolva estas quatro portas de entrada antes de criar recursos. Se uma delas depender da equipe de Cloud ou de Google Ads da sua empresa, compartilhe o link correspondente e peça a liberação necessária.

1. **Projeto e faturamento do Google Cloud.** Você precisa de um projeto com faturamento habilitado e permissão para habilitar APIs, criar recursos e identidades, conceder acesso aos segredos e publicar serviços. A administração da sua organização pode exigir que alguém com permissões específicas execute parte dos comandos. Build, armazenamento, logs, tráfego e execução podem gerar custos. Alertas de orçamento ajudam a acompanhar, mas não são um limite automático de gastos.
2. **Acesso à Google Ads API.** A API precisa estar habilitada no projeto e esse projeto precisa ter o nível de acesso adequado ao ambiente: teste ou contas de produção. O Google atualizou o processo de acesso em 2026; para novos acessos, consulte a página de visão geral da API Google Ads no Console do Google Cloud. Projetos ou versões do servidor que já usam credenciais antigas podem ter requisitos adicionais: siga a documentação oficial do commit que você fixou.
3. **OAuth e acesso à conta.** Você precisa poder configurar um cliente OAuth e cadastrar a URL de retorno exata do servidor, conforme o commit fixado. O cliente MCP inicia outra etapa do fluxo; não cadastre a URL dele como callback do servidor. A pessoa que concluir o login também precisa ter acesso à conta de anúncios desejada. Acesso via conta de administrador (MCC) só é necessário quando o seu arranjo de contas depende dela.
4. **Cliente MCP e modo de uso.** Escolha um cliente que aceite Streamable HTTP e consiga concluir o OAuth descrito pela versão do servidor. O perfil deste tutorial habilita `customers`, `search` e `metadata`, e desabilita `labels` e `assets`; confirme essa lista antes de autorizar uma conta. O servidor oficial também inclui ferramentas para criar ativos ou alterar rótulos. OAuth não limita essas ferramentas nem reduz as permissões da identidade Google.

## Caminho guiado

Siga a sequência. O primeiro guia explica cada comando inicial e mostra o checkpoint antes de avançar.

| Etapa | O que acontece | Guia |
| --- | --- | --- |
| 1. Preparar | Conferir acessos, ferramentas e projeto; habilitar os serviços necessários | [Pré-requisitos](docs/getting-started/PREREQUISITES.md) |
| 2. Preparar a versão | Conferir o commit de referência e a lista de ferramentas configurada | [Implantação](docs/getting-started/DEPLOY.md) |
| 3. Preparar OAuth | Configurar o login e guardar os segredos fora do código | [OAuth e Secret Manager](docs/guides/OAUTH-AND-SECRETS.md) |
| 4. Construir e publicar | Retomar o guia de implantação para criar a imagem e publicar o serviço | [Implantação](docs/getting-started/DEPLOY.md) |
| 5. Validar | Verificar endereço, login, ferramentas visíveis e consulta de teste | [Validação](docs/guides/VALIDATION.md) |
| 6. Diagnosticar e manter | Investigar erros, custos, revisões e manutenção | [Troubleshooting](docs/guides/TROUBLESHOOTING.md) · [Custos](docs/guides/COSTS.md) · [Operação](docs/guides/OPERATIONS.md) |

Se você ainda está avaliando a ideia, comece por [Arquitetura](docs/ARCHITECTURE.md), [Custos](docs/guides/COSTS.md), [Glossário](docs/GLOSSARY.md) e os [vídeos complementares em português](docs/guides/VIDEOS-PT-BR.md). Os vídeos explicam conceitos e navegação; não substituem os passos operacionais atuais. A lista completa está no [índice da documentação](docs/README.md).

## Reprodução e homologação

Reproduzir este roteiro confirma apenas os checkpoints que você executou, na combinação de projeto, região, versão do servidor e cliente escolhida. Isso não comprova segurança, custo ou disponibilidade para todas as contas, nem transforma a implantação em uma configuração pronta para produção.

Para homologar o uso na sua organização, valide com uma conta de teste ou autorizada, confirme a lista de ferramentas e restrinja as ações expostas de acordo com o processo interno. Faça a revisão de OAuth, persistência, permissões, registros, custos, quotas e recuperação de falhas com as equipes responsáveis antes de conectar contas de produção. A lista de testes descreve evidências desejadas; não é um certificado emitido por este repositório.

## Peça ajuda a um tutor de IA

Você pode copiar o [prompt para ChatGPT ou Codex](docs/guides/AI-TUTOR.md) junto dos trechos de documentação que estiver seguindo. O prompt orienta o tutor a explicar comandos, parar em checkpoints e pedir sua escolha antes de qualquer ação que altere recursos ou possa gerar cobrança. **Não cole senhas, chaves, tokens, valores de segredos, cookies nem arquivos de credenciais**; use marcadores como `[VALOR OCULTADO]`.

## Documentação em português e inglês

- Português: [índice](docs/README.md) · [glossário](docs/GLOSSARY.md) · [tutor de IA](docs/guides/AI-TUTOR.md)
- English: [README](README.en.md) · [documentation index](docs/en/README.md) · [glossary](docs/en/GLOSSARY.md) · [AI tutor](docs/en/guides/AI-TUTOR.md)

## Referências principais

- [Servidor oficial Google Ads MCP](https://github.com/googleads/google-ads-mcp)
- [Primeiros passos na Google Ads API](https://developers.google.com/google-ads/api/docs/get-started/introduction)
- [Acesso à Google Ads API e níveis de acesso](https://developers.google.com/google-ads/api/docs/api-policy/developer-token?hl=pt-BR)
- [Documentação do Cloud Run](https://cloud.google.com/run/docs)
- [Índice de referências deste guia](docs/REFERENCES.md)
- [Licença deste guia](LICENSE) · [Avisos de componentes de terceiros](THIRD_PARTY_NOTICES.md)
