# MCP: STDIO versus Streamable HTTP

| Aspecto | STDIO | Streamable HTTP |
| --- | --- | --- |
| Execução | Processo local iniciado pelo cliente | Servidor remoto acessado via rede |
| Melhor adequação | Desenvolvimento e uso individual | Clientes distribuídos e serviço compartilhável |
| Transporte | Entrada/saída do processo | HTTP e sessões, conforme o protocolo |
| Segurança | Credenciais e controles locais | Autenticação, rede, TLS, hospedagem e logs |

A escolha de HTTP **não autoriza automaticamente múltiplos usuários**. Identidade, permissões e governança exigem avaliação adicional.

Fonte normativa: [transportes MCP](https://modelcontextprotocol.io/specification/latest/basic/transports).
