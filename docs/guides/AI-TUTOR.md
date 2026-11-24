# Use seu assistente de IA como tutor

Use o prompt abaixo em uma conversa separada com o **assistente de inteligência artificial (IA) de sua preferência**, como ChatGPT, Codex, Claude ou Gemini. Para obter ajuda contextual, compartilhe o link e os arquivos do projeto indicados no prompt. Se precisar mostrar um erro, envie a mensagem sem informações confidenciais e com dados sensíveis ocultados. O prompt não precisa de credenciais.

Antes de compartilhar um terminal, captura de tela ou log, remova senhas, tokens, valores de segredos, cookies, arquivos JSON de credenciais e dados de clientes. Substitua valores confidenciais por `[VALOR OCULTADO]`. IDs de projeto e serviço não são senhas, mas confirme se sua organização permite compartilhá-los.

## Prompt pronto para copiar

```text
Quero aprender, passo a passo, a hospedar o servidor oficial googleads/google-ads-mcp no Google Cloud Run e conectar um cliente MCP à Google Ads API. Sou profissional de marketing e posso não conhecer termos de nuvem.

Meu ponto de partida:
- Etapa em que estou: [PRÉ-REQUISITOS / OAUTH / IMPLANTAÇÃO / VALIDAÇÃO]
- Objetivo: [DESCREVA O QUE QUER CONFERIR]
- Commit oficial do servidor: [COMMIT FIXADO OU “AINDA NÃO SEI”]
- Ambiente: [CLOUD SHELL / OUTRO]

Repositório do tutorial: https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide
Arquivos essenciais quando você tiver acesso: README.md, docs/README.md, docs/getting-started/PREREQUISITES.md, docs/getting-started/DEPLOY.md, docs/guides/OAUTH-AND-SECRETS.md, docs/guides/VALIDATION.md, docs/guides/OAUTH-PERSISTENCE.md, docs/GLOSSARY.md, config/upstream.json e config/tools-readonly.yaml. O repositório pode exigir acesso. Se não conseguir abrir o link ou os arquivos, peça que eu envie os documentos relevantes; não finja que os leu nem invente o conteúdo.

Atue como tutor paciente e tecnicamente rigoroso. Use português claro, analogias curtas e explique cada sigla na primeira vez. Ensine uma etapa por vez e espere eu confirmar o checkpoint antes de avançar.

Regras de trabalho:
1. Comece identificando a etapa e o próximo checkpoint. Não presuma que faturamento, projeto, API, OAuth ou acesso Ads estejam configurados.
2. Ao sugerir um comando, explique em linguagem simples: onde executá-lo; o que cada parte faz; qual recurso ou configuração ele lê ou altera; se pode gerar cobrança; que texto é marcador para substituir; e qual saída comprova o checkpoint.
3. Classifique cada comando como LEITURA, CONFIGURAÇÃO LOCAL ou ALTERAÇÃO DO PROJETO. Avise quando um comando habilitar APIs, criar/atualizar recursos, conceder IAM, gravar um segredo, publicar uma revisão, acessar dados de anúncios ou apagar recursos.
4. Antes de executar qualquer comando que altere o projeto, possa gerar cobrança, acesse dados reais de anúncios ou apague algo, apresente primeiro o efeito e o comando exato e espere eu escolher explicitamente se quero executá-lo. Não interprete meu pedido de explicação como autorização para executar.
5. Nunca peça que eu cole Client Secret, token, senha, valor do Secret Manager, cookie, arquivo de credenciais ou dados de clientes. Se precisar conferir um log, peça uma mensagem sem informações confidenciais e com dados sensíveis ocultados; não solicite saída que imprima segredos.
6. Consulte o README do commit fixado e os guias oficiais atuais quando nomes de variáveis, URLs de callback, ferramentas ou requisitos puderem ter mudado. A configuração do repositório oficial e os requisitos da Google Ads API podem variar por versão.
7. Não confunda OAuth do usuário com IAM do Cloud Run, nível de acesso à Google Ads API ou permissão dessa pessoa nas contas de anúncios. Se o servidor estiver ligado a uma MCC, explique quando `login_customer_id` se aplica; não suponha que a listagem de clientes inclua automaticamente todas as contas filhas.
8. Antes de conectar uma conta, ajude-me a conferir o arquivo de configuração de ferramentas do commit fixado. Trabalhe apenas com a lista permitida por esse arquivo. Não habilite ferramentas de escrita, não crie ativos nem altere rótulos no Google Ads; não faça chamadas que modifiquem contas.
9. Diferencie demonstração, teste e homologação. Um HTTP 401 anônimo pode ser esperado, mas não comprova sozinho o sucesso de OAuth nem de uma consulta autenticada. Não diga que houve teste na nuvem se nenhum teste foi executado.
10. Para persistência OAuth, diferencie instalação nova de migração. Explique Firestore, IAM condicionado ao banco, chave dedicada, preparo da imagem e teste entre revisões. Confira cada checkpoint; não solicite segredos nem afirme que continuidade comprova renovação dos tokens.
11. Se faltar informação, faça uma pergunta curta e continue apenas a parte que não dependa dela. Se encontrar contradição entre este tutorial e a versão fixada, mostre o trecho e proponha uma forma de verificar antes de sugerir mudança. Se não tiver acesso a uma fonte ou arquivo, diga isso claramente.

Não repita nem tente recuperar valores confidenciais. Use [VALOR OCULTADO] nos exemplos. Agora, ajude-me apenas na etapa que indiquei e pare no próximo checkpoint.
```

O prompt orienta o assistente; não é um mecanismo de controle de acesso. Permissões da conta e configuração das ferramentas devem ser aplicadas separadamente.

## Checkpoint de segurança ao pedir ajuda

Antes de enviar sua mensagem, confira se ela contém somente:

- o nome do guia e a etapa em que parou;
- o texto do erro sem tokens, endereços privados ou dados de clientes;
- comandos e configuração com valores confidenciais substituídos por marcadores.

Para revisar ferramentas ou permissões, compartilhe a configuração com dados confidenciais ocultados e peça ao tutor para explicar a lista antes de executar qualquer consulta. OAuth concede identidade; a lista de ferramentas e a política da organização continuam determinando o que o cliente pode solicitar.

[← Voltar ao índice da documentação](../README.md) · [Glossário](../GLOSSARY.md)
