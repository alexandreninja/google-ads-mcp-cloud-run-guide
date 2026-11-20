# Segurança

## Antes da implantação

- Utilize projeto e contas autorizados.
- Armazene Client Secret e chave JWT no Secret Manager.
- Conceda acesso aos segredos apenas à conta de serviço necessária.
- Cadastre redirect URIs exatas.
- Revise escopos OAuth e permissões das contas Google Ads.
- Configure TLS, logs, limites e controle de acesso apropriados.
- Avalie o tratamento das respostas pelo cliente MCP utilizado.

## Cuidados com o repositório

Não publique `.env` com segredos, tokens, arquivos de credenciais, IDs privados de contas, URLs internas ou logs com dados sensíveis.

## Recurso de leitura

Desabilitar ferramentas que modificam recursos **não reduz automaticamente os escopos OAuth**. A configuração do servidor e as permissões do usuário devem ser verificadas separadamente.

Consulte [OAuth e Secret Manager](docs/guides/OAUTH-AND-SECRETS.md).
