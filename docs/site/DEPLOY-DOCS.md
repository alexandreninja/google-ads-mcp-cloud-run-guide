# Publicação do portal

O site em `site/` usa Astro + Starlight. O repositório GitHub é a fonte de versionamento.

1. Revise conteúdo, licenciamento, URLs, segurança e privacidade.
2. Configure `DOCS_SITE_URL` e `DOCS_BASE_PATH` para o domínio correto.
3. Execute `cd site && npm install && npm run build` em um ambiente apropriado.
4. Configure o GitHub Pages ou outro host de estáticos após a revisão.

O portal é uma navegação introdutória com links para documentos canônicos em `docs/`. Uma etapa futura pode gerar automaticamente as páginas a partir da mesma fonte Markdown, evitando divergências.
