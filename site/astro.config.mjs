import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const site = process.env.DOCS_SITE_URL || 'https://alexandreninja.github.io';
const base = process.env.DOCS_BASE_PATH || '/google-ads-mcp-cloud-run-guide';

export default defineConfig({
  site,
  base,
  integrations: [starlight({
    title: 'Google Ads MCP · Cloud Run',
    description: 'Deployment, OAuth, validation, troubleshooting.',
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/alexandreninja/google-ads-mcp-cloud-run-guide' }],
    customCss: ['./src/styles/custom.css'],
    sidebar: [
      { label: 'Início', slug: 'index' },
      { label: 'Pré-requisitos', slug: 'getting-started' },
      { label: 'Arquitetura', slug: 'architecture' },
      { label: 'Deploy', slug: 'deployment' },
      { label: 'OAuth e segurança', slug: 'security' },
      { label: 'Testes e erros', slug: 'troubleshooting' },
      { label: 'Referências', slug: 'references' }
    ]
  })]
});
