# 📧 Newsletter Agent

Um agente automatizado que coleta newsletters de múltiplas fontes, consolida o conteúdo e envia um resumo único por e-mail usando IA generativa.

## 🎯 Sobre o Projeto

O Newsletter Agent foi desenvolvido para simplificar a gestão de múltiplas newsletters, eliminando a necessidade de ler diversas fontes separadamente. O sistema coleta automaticamente as newsletters mais recentes, utiliza a **API Google Gemini** para gerar um resumo inteligente e consolidado, e envia tudo em um único e-mail bem formatado.

A solução combina:
- **Integração com Gmail (IMAP)** para coleta automatizada
- **IA Generativa (Gemini 2.5 Flash)** para síntese inteligente
- **Formatação HTML** para apresentação profissional

## 🏗️ Arquitetura

### **main.py** — Coleta de Newsletters
Responsável por conectar ao Gmail via protocolo IMAP e buscar newsletters dos últimos 24 horas de remetentes específicos. Extrai informações essenciais como assunto, data e conteúdo (em HTML ou texto puro).

### **llm.py** — Processamento e Envio
Consolida o conteúdo de todas as newsletters coletadas e envia para o **Google Gemini 2.5 Flash**, que gera um resumo massivo temático. O resultado é formatado em HTML puro e disparado automaticamente via SMTP para o destinatário configurado.

## 📋 Stack Técnico

- **Python 3.x** — Linguagem principal
- **imap_tools** — Acesso ao protocolo IMAP
- **google-genai** — Integração com API Google Gemini
- **smtplib** — Envio de e-mails
- **python-dotenv** — Gerenciamento de variáveis de ambiente

## 🔄 Fluxo de Funcionamento

1. **Coleta** → Acessa IMAP do Gmail e busca newsletters dos últimos 24h
2. **Consolidação** → Combina HTML/texto de todas as newsletters
3. **Análise IA** → Gemini gera um resumo temático e coeso em HTML
4. **Distribuição** → E-mail com resumo consolidado é enviado automaticamente

## 📧 Saída

Um e-mail contendo:
- **Subject**: `[RESUMO LLM] Todas as Newsletters de DD/MM/YYYY`
- **Corpo**: Resumo em HTML com tópicos agrupados tematicamente
- **Formato**: Puro HTML, renderizável em qualquer cliente de e-mail

## ✨ Diferenciais

- **Consolidação Inteligente** — Elimina redundâncias e agrupa conteúdo por temas
- **100% Automatizado** — Sem intervenção manual necessária
- **Pronto para Produção** — Pode ser integrado com agendadores (cron, Task Scheduler)
- **Multilíngue** — Suporta resumos em português-BR

---

**Desenvolvido como uma solução de automação pessoal para gerenciamento eficiente de informação.**
