import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const site = process.env.DOCS_SITE_URL || 'https://alexandreninja.github.io';
const base = process.env.DOCS_BASE_PATH || '/google-ads-mcp-cloud-run-guide';

export default defineConfig({
  site,
  base,
  integrations: [starlight({
    title: 'Google Ads MCP · Guia de implantação',
    description: 'Arquitetura, Cloud Run, OAuth, testes e troubleshooting.',
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide' }],
    customCss: ['./src/styles/custom.css'],
    sidebar: [
      { label: 'Início', slug: 'index' },
      { label: 'Comece aqui', slug: 'getting-started' },
      { label: 'Arquitetura', slug: 'architecture' },
      { label: 'Guia de deploy', slug: 'deployment' },
      { label: 'OAuth e segurança', slug: 'security' },
      { label: 'Erros e testes', slug: 'troubleshooting' },
      { label: 'Referências', slug: 'references' }
    ]
  })]
});
