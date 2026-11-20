# Troubleshooting — erros reais e correções

## `redirect_uri_mismatch`

**Sintoma:** o login OAuth não consegue concluir o retorno ao cliente. **Hipótese:** redirect URI ausente ou divergente.

**Correção observada:** ajustar a lista de URIs autorizadas, incluindo callback do servidor. Compare URLs exatas, sem divulgar endpoints privados.

## `invalid_client`

**Sintoma:** credenciais OAuth rejeitadas.

**Correção observada:** criar nova versão do segredo no Secret Manager e atualizar o serviço para utilizá-la.

**Limite de evidência:** foi levantada hipótese de caractere indevido na cópia do segredo, mas **não se confirmou a causa**.

## HTTP 401 sem login

**Sintoma:** uma requisição anônima recebe `401 Unauthorized`. **Interpretação:** na configuração que exige autenticação, é resultado esperado de teste negativo, não erro de deploy.

## Ordem de investigação

1. Versão exata do upstream e status do Cloud Run.
2. URLs e metadados do OAuth.
3. IAM e acesso à versão correta do segredo.
4. Nova tentativa de login com cliente de teste.
5. Descoberta de ferramentas e consulta autorizada.

[Consultar a matriz de testes](VALIDATION.md).
