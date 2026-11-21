# Google Ads MCP no Google Cloud Run

[English](README.en.md) · [Documentação](docs/README.md) · [Licença MIT](LICENSE)

<p align="center">
  <img src="docs/assets/github-header.svg" alt="Cliente MCP conectado ao servidor Google Ads MCP no Cloud Run e à Google Ads API" width="100%">
</p>

**Construir ou integrar?** No artigo, essa pergunta nasceu de um desafio no Sebrae Rio: modernizar os dashboards de marketing e explorar como a IA poderia ajudar a interpretar dados validados. Entre uma integração gerenciada e uma implantação própria, o experimento seguiu pelo servidor oficial [Google Ads MCP](https://github.com/googleads/google-ads-mcp), hospedado no Cloud Run.

O artigo conta as decisões, os erros de autenticação e os aprendizados. **Este repositório transforma esse percurso em um passo a passo**, pensado também para quem vem do marketing e está começando a trabalhar com nuvem e IA.

## 🧭 Comece por aqui

| Quero… | Por onde seguir |
| --- | --- |
| Entender a escolha e os componentes | [Arquitetura](docs/ARCHITECTURE.md) · [STDIO ou HTTP?](docs/concepts/MCP-TRANSPORTS.md) |
| Implementar, uma etapa por vez | [01 · Pré-requisitos](docs/getting-started/PREREQUISITES.md) → [02 · Implantação](docs/getting-started/DEPLOY.md) |
| Aprender com um assistente de IA | [Prompt para seu assistente de IA](docs/guides/AI-TUTOR.md) |
| Resolver um erro | [Diagnóstico por sintoma](docs/guides/TROUBLESHOOTING.md) |
| Manter ou encerrar o laboratório | [Custos](docs/guides/COSTS.md) · [Operação e limpeza](docs/guides/OPERATIONS.md) |

## 🔎 O que você vai construir

Um serviço HTTPS que permite a um cliente de IA consultar a Google Ads API por meio do MCP. O roteiro usa o **Cloud Shell**, terminal disponível no navegador, e organiza a implantação em etapas com checkpoints:

1. Preparar o projeto, os acessos e as identidades de build e execução.
2. Configurar o login Google com OAuth e guardar as credenciais no Secret Manager.
3. Construir a imagem, publicar no Cloud Run e conectar um cliente MCP.
4. Conferir as ferramentas disponíveis e validar uma consulta à conta autorizada.

Essa integração cuida do **acesso aos dados**. Na arquitetura discutida no artigo, cálculos e regras de negócio continuam em código e SQL; o modelo de linguagem ajuda na interpretação. Dashboards, pipelines e a integração ao fluxo corporativo são etapas de evolução.

> [!IMPORTANT]
> Antes de começar, confira os [pré-requisitos](docs/getting-started/PREREQUISITES.md): projeto com faturamento, permissões de implantação, acesso à API e à conta Google Ads. Os recursos podem gerar cobrança. Em ambiente institucional, combine essas liberações com a equipe responsável.

## 🧪 Aprenda fazendo

Cada checkpoint diz o que conferir antes de avançar. Encontrou uma sigla nova? Consulte o [glossário](docs/GLOSSARY.md). Precisa acompanhar a navegação na tela? Os [vídeos em português](docs/guides/VIDEOS-PT-BR.md) complementam os passos escritos.

Você também pode compartilhar este repositório com o **assistente de IA de sua preferência**, como ChatGPT, Codex, Claude ou Gemini, e pedir acompanhamento com o [prompt de tutoria](docs/guides/AI-TUTOR.md). Ele orienta a explicar os comandos e verificar os resultados com você. Use valores ocultados ao compartilhar erros ou configurações; mantenha credenciais fora da conversa.

<details>
<summary>Versão de referência e verificações do guia</summary>

O roteiro fixa o commit `44ca7770519362c8f334875477e1ceb499f8d2dd` do servidor oficial. A [implantação](docs/getting-started/DEPLOY.md) explica como preparar essa origem; o [registro de revisão](docs/REVIEW.md) lista as verificações locais e o que ainda depende de teste no seu ambiente.

</details>

## 📚 Para consultar

[Índice completo](docs/README.md) · [Segurança](SECURITY.md) · [Fontes oficiais](docs/REFERENCES.md) · [Como contribuir](CONTRIBUTING.md)

O guia e seus arquivos originais estão sob [licença MIT](LICENSE): você pode usar, estudar, adaptar e redistribuir, inclusive comercialmente, preservando o aviso de licença. O servidor é mantido pelo projeto oficial do Google e segue sua própria licença, descrita nos [avisos de terceiros](THIRD_PARTY_NOTICES.md).
