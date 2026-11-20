# Operação e checklist

Antes de ampliar o experimento, verifique:

- [ ] Versão do upstream fixada e changelog revisado.
- [ ] Contas de serviço e IAM com menor privilégio.
- [ ] Credenciais no Secret Manager e política de rotação definida.
- [ ] Persistência adequada de estado OAuth em escala variável.
- [ ] Metadados, logs de acesso e política de minimização de dados.
- [ ] Monitoramento do Cloud Run, quotas da Google Ads API, custos e alertas.
- [ ] Backups, rollback, recuperação e processo de atualização.
- [ ] Clientes MCP avaliados pela política de dados da organização.
- [ ] Aprovação do uso com pessoas e contas adicionais.
- [ ] Testes negativos e evidências sanitizadas registrados.

Não exponha publicamente o endpoint institucional nem dados das contas. Para uma nova revisão, veja [Segurança](../../SECURITY.md).
