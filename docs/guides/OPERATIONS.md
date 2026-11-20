# 06 · Operação e manutenção

## Verificações

- [ ] Registrar a tag ou o commit exato do Google Ads MCP utilizado.
- [ ] Revisar notas de versão antes de reconstruir a imagem.
- [ ] Acompanhar erros e latência do Cloud Run.
- [ ] Conferir uso de quotas da Google Ads API.
- [ ] Validar validade, rotação e acesso aos segredos.
- [ ] Monitorar faturamento de Cloud Run e dos demais serviços.
- [ ] Planejar persistência e limpeza do estado OAuth.
- [ ] Manter processo de rollback para imagem anterior.
- [ ] Revisar permissões e registrar alterações de configuração.

## Consultas úteis

```bash
gcloud run services describe google-ads-mcp --region=us-central1

gcloud run revisions list \
  --service=google-ads-mcp \
  --region=us-central1

gcloud builds list --limit=10
```

Para custos, veja [Custos](COSTS.md). Para segurança, [SECURITY.md](../../SECURITY.md).
