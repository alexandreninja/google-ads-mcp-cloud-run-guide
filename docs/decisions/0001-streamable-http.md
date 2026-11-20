# ADR 0001 — Streamable HTTP

**Contexto:** a execução via STDIO atenderia um cliente local, mas o experimento pretendia estudar reutilização por diferentes computadores e usuários autorizados.

**Decisão:** investigar o transporte remoto Streamable HTTP oferecido pelo servidor oficial.

**Consequência positiva:** servidor centralizado e possibilidade de múltiplos clientes sem instalação local individual.

**Responsabilidades adicionais:** autenticação, segurança de rede, estado do OAuth, compatibilidade e custos.

**Não significa:** multiusuário homologado ou acesso institucional ampliado.
