# 🍔 Sistema de Gestão - Take Away Asfalto 11

> **Status:** Em Produção 🚀

Este projeto é uma aplicação web desenvolvida sob medida para o **Take Away Asfalto 11**. O objetivo principal do sistema é modernizar e agilizar o processo de registro de vendas, garantindo um monitoramento preciso e em tempo real do estoque de produtos alimentícios e bebidas.

A solução substitui controles manuais ou descentralizados por uma interface intuitiva, conectada diretamente a uma base de dados na nuvem (Google Sheets), permitindo a geração de relatórios gerenciais e dashboards financeiros.

---

## 🎯 Objetivos do Projeto

*   **Agilidade no Atendimento:** Interface otimizada para registro rápido de pedidos complexos (hambúrgueres com adicionais, sanduíches, bebidas, guloseimas).
*   **Controle de Estoque Preciso:** Baixa automática de ingredientes e itens no momento da venda. O sistema impede a venda caso não haja estoque suficiente.
*   **Inteligência de Negócio:** Dashboards interativos para análise de faturamento, volume de vendas e produtos mais vendidos.
*   **Relatórios Automatizados:** Geração de PDFs prontos para impressão com o resumo de vendas diário, semanal ou mensal.

---

## 🛠️ Funcionalidades Principais

### 1. Módulo de Vendas (`Take Away`)
*   **Lógica de Exclusão:** Interface inteligente que impede seleções conflitantes (ex: selecionar Hambúrguer desabilita Sandes).
*   **Adicionais e Variações:** Suporte para múltiplos tipos de produtos (Simples, Completo, Duplo, Com Ovo, Com Queijo, etc.).
*   **Cálculo Automático:** Preços calculados dinamicamente com base nas escolhas do cliente.
*   **Validação de Estoque:** O sistema verifica a disponibilidade dos ingredientes antes de confirmar a venda.

### 2. Módulo de Estoque (`Gerenciamento`)
*   **Entrada de Produtos:** Interface simples para reposição de estoque (Hambúrgueres, Bebidas, Embalagens, Ingredientes paralelos).
*   **Classificação:** Separação lógica entre estoque de Alimentos, Bebidas e Estoque Paralelo (insumos diversos).
*   **Monitoramento de Status:** Classificação automática dos níveis de estoque em: "Normal", "Alerta" e "Crítico".

### 3. Dashboards e Relatórios (`Analytics`)
*   **Visão Geral:** KPIs de Faturamento total, volume de vendas e comparações com períodos anteriores (Ontem, Semana, Mês).
*   **Gráficos Interativos:**
    *   Faturamento por Categoria.
    *   Volume de Vendas por Produto.
    *   Linha do tempo de vendas.
*   **Exportação PDF:** Geração automática de relatórios em PDF contendo os gráficos e métricas para arquivamento ou envio à gerência.

---

## 💻 Tecnologias Utilizadas

O projeto foi desenvolvido em **Python** utilizando as seguintes bibliotecas:

*   **[Streamlit](https://streamlit.io/):** Framework principal para o front-end e lógica da aplicação.
*   **[Google Sheets API (gspread)](https://docs.gspread.org/):** Utilizado como banco de dados relacional (backend).
*   **[Pandas](https://pandas.pydata.org/):** Manipulação e análise de dados.
*   **[Plotly Express](https://plotly.com/python/):** Criação de gráficos interativos e visuais para dashboards.
*   **[ReportLab](https://www.reportlab.com/):** Geração de arquivos PDF programaticamente.
*   **Kaleido:** Motor para exportação de imagens estáticas dos gráficos (necessário para o relatório PDF).

---

## 📂 Estrutura da Planilha (Google Sheets)

O sistema foi programado para interagir com uma planilha específica contendo as seguintes abas (Worksheets):

*   **Vendas:** Registro histórico de todas as transações (Data, Refeição, Qnt, Preço, Bebida, Total, etc.).
*   **Estoque:** Controle de insumos principais (Hambúrguer, Pão, Ovos, Queijo, etc.).
*   **Estoque_Bebidas:** Controle específico de bebidas (Latas, Garrafas, Sumos, Águas).
*   **Estoque_Paralelo:** Insumos secundários ou de uso geral (Batatas, Óleo, Molhos, Embalagens).

---

## 🔒 Segurança

*   **Acesso Restrito:** O sistema possui uma tela de login simples baseada em um código de acesso (PIN) definido nas configurações de segredos.
*   **Proteção de Dados:** As credenciais da nuvem nunca são expostas no código fonte, utilizando variáveis de ambiente seguras.

---

## 📄 Licença

Este projeto é de uso exclusivo do **Take Away Asfalto 11**.
