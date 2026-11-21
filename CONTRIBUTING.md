# Contribuindo

Correções de documentação, exemplos, acessibilidade e links são bem-vindas. Este guia atende principalmente pessoas de marketing que não trabalham com nuvem no dia a dia. Explique o resultado esperado e o próximo passo em linguagem direta; defina termos técnicos quando aparecem pela primeira vez.

## Ao alterar instruções

- Diga em qual diretório, terminal e projeto um comando deve ser executado. Mostre claramente o que é exemplo, o que deve ser substituído e qual saída confirma a etapa.
- Informe antes de comandos que habilitam APIs, criam recursos, alteram acesso ou podem gerar custos.
- Fixe e registre a tag ou commit upstream usada para os exemplos. Variáveis, callbacks, transporte e ferramentas podem mudar entre versões do Google Ads MCP.
- Separe autenticação no Google Cloud, acesso ao projeto e à API Google Ads, OAuth do aplicativo, acesso do usuário à conta Ads e autenticação do cliente MCP. Não use “login” como se todos fossem a mesma etapa.
- Para fatos que mudam, como preços, limites, nomes de menus, versões e políticas de acesso, cite a fonte oficial e a data em que ela foi conferida. Para vídeos, verifique título, idioma, canal, assunto e data de publicação; não apresente uma busca como se fosse um vídeo validado.
- Preserve placeholders em exemplos. Não envie credenciais, tokens OAuth, chaves, cookies, dados pessoais ou identificadores de contas reais em commits, issues, capturas de tela e registros.
- Antes de reutilizar conteúdo de terceiros, confira a licença e a atribuição exigida. Prefira resumir e apontar para a fonte original; preserve os avisos de licença aplicáveis.

## Revisão

Antes de abrir uma contribuição, confira se os links locais funcionam, se os passos seguem a versão upstream indicada e se nenhuma instrução sugere copiar um segredo para o terminal, repositório ou histórico do shell. Mudanças no código do servidor oficial devem ser relatadas em suas [issues](https://github.com/googleads/google-ads-mcp/issues); este repositório documenta a implantação e não mantém o código upstream.

O conteúdo original deste repositório segue a licença indicada em [LICENSE](LICENSE). O código do Google Ads MCP upstream está sob Apache 2.0; isso não altera a licença do nosso conteúdo. As fontes e datas de conferência estão em [docs/REFERENCES.md](docs/REFERENCES.md).

## Verificações locais

Execute na raiz do repositório; estes comandos não implantam recursos nem acessam contas de anúncios:

~~~bash
python3 scripts/check_docs.py
python3 scripts/check_translations.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
git diff --check
~~~

Mantenha os exemplos executáveis em português e inglês equivalentes. A revisão e seus limites estão em [docs/REVIEW.md](docs/REVIEW.md).
