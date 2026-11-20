# ADR 0002 — Google Cloud Run

**Contexto:** após decidir por HTTP remoto, era necessário escolher a hospedagem. VPS e servidores internos eram alternativas tecnicamente possíveis.

**Decisão:** utilizar o Cloud Run no Google Cloud institucional disponível, com um caminho de implantação documentado pelo próprio projeto oficial.

**Motivação:** viabilidade prática e menor dependência de um novo processo de disponibilização de infraestrutura, mantendo a implantação em recursos corporativos já acessíveis.

**Riscos e limites:** gestão de IAM, autenticação, segredo, persistência de estado, custos, cliente externo e controles organizacionais.

**Não significa:** que o Google exija Cloud Run ou que a arquitetura esteja formalmente homologada.
