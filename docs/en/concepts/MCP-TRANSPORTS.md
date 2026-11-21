# STDIO and Streamable HTTP

Both transports connect an MCP client to tools. The difference is where the server runs and how the client reaches it.

| Question | STDIO | Streamable HTTP |
| --- | --- | --- |
| Where does the server run? | As a local process | As a separately hosted HTTP service |
| What does the client do? | Starts the process and exchanges standard input/output | Connects to an endpoint such as the service URL followed by /mcp |
| Where is it installed? | In each local environment | Once on the chosen server infrastructure |
| Authentication in this project | Application Default Credentials for local use | Google OAuth through the FastMCP proxy |
| A common use | Individual experiments and local clients | Authorized remote clients |
| Operational responsibility | Local dependencies and credentials | Hosting, access, secrets, persistence, availability, and cost |

This guide chooses **Streamable HTTP on Cloud Run**, based on [upstream commit 44ca777](https://github.com/googleads/google-ads-mcp/tree/44ca7770519362c8f334875477e1ceb499f8d2dd). Configuring both OAuth Client ID and Client Secret enables this mode in the pinned server. Remote hosting creates an opportunity for shared access; it does not automatically authorize every colleague or provide high availability.

## Two callback flows

Google returns to the server's fixed /auth/callback route. The MCP client's own callback can be local or dynamic; the OAuth proxy records and forwards it. Register the server callback in the Google OAuth Web client, not every client's local port. The MCP endpoint /mcp is different from the Google callback.

The authentication discovery routes are also separate: the protected resource is described at /.well-known/oauth-protected-resource/mcp, while OAuth authorization-server metadata is at /.well-known/oauth-authorization-server. A client should discover and use these routes rather than treating the service's root page as an MCP tool endpoint.

## State is more than one thing

The baseline keeps stateful HTTP for compatibility with clients using MCP session identifiers and GET/SSE as well as newer sessionless POST and subscriptions/listen connections. The upstream advises against enabling stateless_http on this shared endpoint because it removes the older GET/SSE channel.

Firestore persists **OAuth state**. It does not preserve in-memory MCP sessions, subscriptions, or open network connections. A stopped instance, new revision, or request timeout may require the client to reconnect. Cloud Run session affinity is best effort, not durable storage. The one-instance pilot described here needs to be assessed again before serving more users.

## Sources

- [Pinned upstream HTTP interoperability notes](https://github.com/googleads/google-ads-mcp/blob/44ca7770519362c8f334875477e1ceb499f8d2dd/README.md#http-interoperability-notes).
- [FastMCP OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy).
- [MCP Python SDK authentication routes](https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/server/auth/routes.py).
- [MCP transport specification](https://modelcontextprotocol.io/specification/latest/basic/transports).
- [Cloud Run session affinity](https://docs.cloud.google.com/run/docs/configuring/session-affinity).

[Architecture](../ARCHITECTURE.md) · [Deployment](../getting-started/DEPLOY.md)
