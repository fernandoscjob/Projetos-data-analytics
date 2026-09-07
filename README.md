# 📊 Portfólio Profissional de Dados & Business Intelligence

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![Tema](https://img.shields.io/badge/Tema-Dark_Modern_(Linear/Vercel)-090a0f?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-HTML5_•_TailwindCSS_•_Chart.js_•_Vanilla_JS-sky?style=for-the-badge)

Portfólio técnico de **Fernando Cavalcante** — Analista de Dados Sênior & Especialista em Business Intelligence, com foco em tomada de decisão executiva, redução de custos operacionais, modelagem dimensional e governança analítica.

---

## 🌟 Destaques do Projeto

- **Design System Dark Modern**: Estética refinada inspirada na *Linear* e *Vercel*, com paleta grafite `#090a0f`, gradientes radiais, efeito *glassmorphism* e acabamento visual de alto padrão.
- **Identidade Pessoal & Foto de Perfil**: Foto profissional integrada no Header, Hero Section de duas colunas com tags flutuantes de impacto (`-40% Custos Frete`, `99.8% SLA Dados`) e seção de contato.
- **Barra de Métricas de Impacto (Quick Wins)**: Contadores animados via `IntersectionObserver` apresentando números de ROI, volume e automação.
- **Stack Técnica Categorizada**: Badges interativos divididos em *Linguagens & Core*, *Business Intelligence* (incluindo **Looker (LookML)**, Power BI e DAX), *Pipelines & Automação* (n8n, dbt) e *Modelagem Dimensional (Kimball)*.
- **4 Cases de Sucesso com Modal Aprofundado**:
  1. **Auditoria Contratual de Fretes & Otimização de Custos** (SQL + Looker + Python).
  2. **Modelagem de Cohort, Retenção & Prevenção de Churn** (SQL Window Functions + dbt).
  3. **Camada Semântica & Cockpit Executivo de Planejamento** (Power BI + dbt + Kimball).
  4. **Orquestração de Pipelines e Alertas Proativos** (n8n + Python + Webhooks).
  *Cada modal contém o desafio de negócio, arquitetura técnica, queries SQL reais e resultados de ROI mensuráveis.*
- **Cockpit Analítico Interativo (Chart.js & Cohort Heatmap)**:
  - *Visão 1*: Custo Real vs Meta (Linha comparativa de inflexão).
  - *Visão 2*: Volume Operacional & Acurácia de SLA (Barras e Eixo Secundário).
  - *Visão 3*: **Matriz Heatmap de Cohort & Churn** com alternância em tempo real entre *Taxa de Retenção (%)* e *Taxa de Churn (%)* com tooltips interativos por célula.
- **Formulário de Contato Integrado**: Pronto para o **Formspree** via envio assíncrono (AJAX/Fetch) com feedback via componente *Toast* sem recarregar a página.
- **Links Reais & Download de CV**: Conexão direta com WhatsApp, LinkedIn, GitHub e download nativo do arquivo `curriculo-fernando.pdf`.

---

## 📁 Estrutura de Arquivos

```
Portifólio em Dados/
├── index.html               # Estrutura HTML5 semântica e acessível
├── style.css                # Design tokens, glassmorphism e animações
├── main.js                  # Lógica interativa, Chart.js, Cohort e Formspree AJAX
├── profile.jpg              # Foto de perfil profissional em alta resolução
├── curriculo-fernando.pdf   # Arquivo de currículo para download direto
└── README.md                # Documentação técnica do projeto
```

---

## 🚀 Como Executar Localmente

### Opção 1: Abrir diretamente no Navegador
Basta dar dois cliques no arquivo `index.html` ou arrastá-lo para qualquer navegador moderno (Chrome, Edge, Firefox, Safari).

### Opção 2: VS Code Live Server
1. Abra a pasta do projeto no **Visual Studio Code**.
2. Instale a extensão **Live Server** (caso ainda não tenha).
3. Clique com o botão direito em `index.html` e selecione **"Open with Live Server"**.
4. O site abrirá automaticamente em `http://127.0.0.1:5500`.

### Opção 3: Python HTTP Server
Abra o terminal na pasta do projeto e execute:
```bash
python -m http.server 3000
```
Acesse no navegador: `http://localhost:3000`.

---

## ✉️ Configuração do Formulário de Contato (Formspree)

O formulário já está configurado e integrado com o endpoint:
```html
<form id="contactForm" action="https://formspree.io/f/xeaqrrnr" method="POST" ...>
```
O envio ocorre de forma assíncrona (AJAX/Fetch), apresentando um spinner de carregamento no botão, limpando os campos e disparando o componente Toast com mensagem de confirmação de envio sem recarregar a página. Caso deseje alterar para outro endpoint no futuro, basta atualizar o atributo `action` no arquivo `index.html`.

---

## 📄 Atualização do Currículo (PDF)

Para atualizar o currículo baixado pelos visitantes:
1. Exporte seu currículo atualizado em formato PDF.
2. Renomeie o arquivo para:
   ```
   curriculo-fernando.pdf
   ```
3. Substitua o arquivo existente na raiz do projeto mantendo o mesmo nome. O botão **"Baixar CV Completo"** fará o download da versão mais recente automaticamente.

---

## 🌐 Instruções de Publicação (Deploy)

### Deploy no GitHub Pages (Gratuito)
1. Crie um repositório no seu GitHub com o nome `portfolio` ou `portfolio-data-analytics`.
2. No terminal da pasta, inicialize o git e suba os arquivos:
   ```bash
   git init
   git add .
   git commit -m "feat: portfolio pronto para producao"
   git branch -M main
   git remote add origin https://github.com/fernandoscjob/Projetos-data-analytics.git # ou seu repositorio especifico
   git push -u origin main
   ```
3. No GitHub, acesse **Settings** > **Pages**.
4. Em **Source**, selecione `Deploy from a branch`, escolha a branch `main` e a pasta `/ (root)`.
5. Salve. Seu portfólio estará online em `https://fernandoscjob.github.io/...` com HTTPS ativo.

### Deploy na Vercel (Recomendado para SPA/Estático)
1. Acesse [vercel.com](https://vercel.com) e conecte com seu GitHub.
2. Clique em **"Add New Project"** e selecione o repositório do portfólio.
3. Clique em **Deploy**. O site será publicado instantaneamente com CDN global de altíssima velocidade.

---

## 📬 Contatos & Redes Profissionais

- **LinkedIn**: [fernando-cavalcante-a478191b1](https://www.linkedin.com/in/fernando-cavalcante-a478191b1/)
- **GitHub**: [fernandoscjob](https://github.com/fernandoscjob/Projetos-data-analytics)
- **WhatsApp**: [+55 (21) 96924-1760](https://wa.me/5521969241760?text=Ol%C3%A1%20Fernando,%20vi%20seu%20portf%C3%B3lio.)
- **E-mail**: [fernandoc.job@gmail.com](mailto:fernandoc.job@gmail.com)

---

*Desenvolvido com foco em alta performance, usabilidade moderna e impacto direto em negócios.*
