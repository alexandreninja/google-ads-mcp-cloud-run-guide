# Verificações do guia · 21 de novembro de 2026

Este registro reúne o escopo e as evidências da revisão documental. A referência do servidor é o commit `44ca7770519362c8f334875477e1ceb499f8d2dd`, registrado em [upstream.json](../config/upstream.json).

## O que mudou nesta rodada

- Abertura ligada ao artigo **Construir ou integrar?**, navegação por objetivo e detalhes técnicos revelados ao longo do percurso.
- Alertas de custos, credenciais e configuração posicionados nas respectivas etapas, com exemplos equivalentes em português e inglês.
- Permissões do operador para acompanhar o build, enviar a origem e ler a imagem explicitadas na implantação.
- Preparo da origem condicionado a repositório oficial, commit fixado e checkout limpo, antes de qualquer gravação.
- Validação com granularidade dos dados, moeda, fuso e conversão de micros por código.

## Verificações locais

| Verificação | O que cobre |
| --- | --- |
| `check_docs.py` | Links e âncoras locais, JSON e sintaxe Bash/Python; sem executar comandos Cloud |
| `check_translations.py` | Equivalência dos exemplos executáveis PT/EN |
| Testes do helper | Repositórios Git temporários: origem, commit, alterações locais e preparo da imagem |
| Parser upstream | Aceitação do perfil `customers`, `search` e `metadata`, com `labels` e `assets` desabilitados |
| Inspeção do build | Extra Firestore, imagem parametrizada e logs no Cloud Logging |
| `git diff --check` | Erros de whitespace no diff |

Nesta rodada, as verificações acima passaram. Os testes do helper executaram **11 casos em repositórios Git temporários reais**. A varredura heurística do conteúdo textual não encontrou padrões de credenciais; isso não substitui uma análise de segurança do ambiente.

Para repetir as verificações automatizadas a partir da raiz:

~~~bash
python3 scripts/check_docs.py
python3 scripts/check_translations.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
git diff --check
~~~

## Limite das evidências

> [!NOTE]
> Esta revisão não executou novo build de contêiner, deploy no Google Cloud, fluxo OAuth real ou consulta a contas Google Ads. As verificações locais avaliam o material e o preparo da origem; os checkpoints de implantação precisam ser executados no ambiente de destino.

A [matriz de validação](guides/VALIDATION.md) orienta a registrar build, revisão, login, ferramentas e consulta. Os vídeos complementares tiveram metadados conferidos, sem revisão integral do conteúdo. O scaffold em `site/` permanece experimental.

[English](en/REVIEW.md) · [Índice](README.md)

## Evidência adicional · 24 de novembro de 2026

O [experimento de migração](guides/OAUTH-PERSISTENCE.md) foi realizado em outro commit upstream do pacote 0.0.6. A revisão acima permanece como registro histórico de 21/11. A continuidade de acesso entre revisões foi observada; renovação após expiração e custo efetivo ainda não foram comprovados. Os testes automatizados da atualização documental devem ser executados antes da publicação.
