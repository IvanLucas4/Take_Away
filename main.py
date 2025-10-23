import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.io as pio
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

pio.templates.default = "plotly_white"

# tela de login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.title("🔏 Acesso Restrito")
    codigo = st.text_input("Digite o Código de Acesso", type="password", max_chars=4)
    if st.button("Entrar"):
        if codigo == st.secrets["auth"]["access_code"]:
            st.session_state.authenticated = True
            st.success("Acesso Autorizado ✅")
            st.rerun()
        else:
            st.error("Código Incorreto! Tente Novamente.")
    st.stop()

dt = datetime.today().date()
date = dt.strftime("%d-%m-%Y")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_resource
def carregar_planilhas():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1HURNDK9zCl4Cj9BYvRptYa_zJfb3MPcYVkXwhY5W2o4").worksheet("Vendas")
    sheet_estoque = client.open_by_key("1HURNDK9zCl4Cj9BYvRptYa_zJfb3MPcYVkXwhY5W2o4").worksheet("Estoque")
    sheet_estoque_bebida = client.open_by_key("1HURNDK9zCl4Cj9BYvRptYa_zJfb3MPcYVkXwhY5W2o4").worksheet("Estoque_Bebidas")
    sheet_estoque_paralelo = client.open_by_key("1HURNDK9zCl4Cj9BYvRptYa_zJfb3MPcYVkXwhY5W2o4").worksheet("Estoque_Paralelo")
    return sheet, sheet_estoque, sheet_estoque_bebida, sheet_estoque_paralelo

sheet, sheet_estoque, sheet_estoque_bebida, sheet_estoque_paralelo = carregar_planilhas()

with st.sidebar:
    st.header('Options')
    options = st.selectbox("Modo", ['Vendas', 'Estoque', 'Relatório'])
    if options == "Relatório":
        st.write("## Filtros do Dashboard")
        aba = st.selectbox("Venda/Estoque", ['Relatório de Vendas', 'Relatório de Estoque'])
    st.markdown("[📁 Planilha](https://docs.google.com/spreadsheets/d/1HURNDK9zCl4Cj9BYvRptYa_zJfb3MPcYVkXwhY5W2o4/edit?gid=1947090066#gid=1947090066)")

if options == 'Vendas':
    st.title("🍔 Take Away App!")

    if 'hamburguer' not in st.session_state:
        st.session_state.hamburguer = 'Não'
    if 'sandes' not in st.session_state:
        st.session_state.sandes = 'Não'
    if 'batata_asinha' not in st.session_state:
        st.session_state.batata_asinha = 'Não'
    if 'refrigerante' not in st.session_state:
        st.session_state.refrigerante = 'Nenhum'
    if 'sumo' not in st.session_state:
        st.session_state.sumo = 'Nenhum'
    if 'agua' not in st.session_state:
        st.session_state.agua = 'Nenhuma'
    if 'bebida_garrafa' not in st.session_state:
        st.session_state.bebida_garrafa = 'Nenhuma'
    if 'bebida_lata' not in st.session_state:
        st.session_state.bebida_lata = 'Nenhuma'
    if 'bolacha' not in st.session_state:
        st.session_state.bolacha = 'Não'
    if 'doce' not in st.session_state:
        st.session_state.doce = 'Não'
    if 'pipoca' not in st.session_state:
        st.session_state.pipoca = 'Não'

    def atualizar_hamburguer():
        if st.session_state.hamburguer != "Não":
            st.session_state.sandes = "Não"
            st.session_state.batata_asinha = "Não"
    def atualizar_sandes():
        if st.session_state.sandes != "Não":
            st.session_state.hamburguer = "Não"
            st.session_state.batata_asinha = "Não"
    def atualizar_batata_asinhas():
        if st.session_state.batata_asinha != "Não":
            st.session_state.sandes = "Não"
            st.session_state.hamburguer = "Não"
    def atualizar_agua():
        if st.session_state.agua != "Nenhuma":
            st.session_state.sumo = "Nenhum"
            st.session_state.refrigerante = "Nenhum"
            st.session_state.bebida_garrafa = "Nenhuma"
            st.session_state.bebida_lata = "Nenhuma"
    def atualizar_refrigerante():
        if st.session_state.refrigerante != "Nenhum":
            st.session_state.sumo = "Nenhum"
            st.session_state.agua = "Nenhuma"
            st.session_state.bebida_garrafa = "Nenhuma"
            st.session_state.bebida_lata = "Nenhuma"
    def atualizar_sumo():
        if st.session_state.sumo != "Nenhum":
            st.session_state.agua = "Nenhuma"
            st.session_state.refrigerante = "Nenhum"
            st.session_state.bebida_garrafa = "Nenhuma"
            st.session_state.bebida_lata = "Nenhuma"
    def atualizar_bebida_garrafa():
        if st.session_state.bebida_garrafa != "Nenhuma":
            st.session_state.sumo = "Nenhum"
            st.session_state.refrigerante = "Nenhum"
            st.session_state.agua = "Nenhuma"
            st.session_state.bebida_lata = "Nenhuma"
    def atualizar_bebida_lata():
        if st.session_state.bebida_lata != "Nenhuma":
            st.session_state.sumo = "Nenhum"
            st.session_state.refrigerante = "Nenhum"
            st.session_state.bebida_garrafa = "Nenhuma"
            st.session_state.agua = "Nenhuma"
    def atualizar_bolacha():
        if st.session_state.bolacha != "Não":
            st.session_state.doce = "Não"
            st.session_state.pipoca = "Não"
    def atualizar_doce():
        if st.session_state.doce != "Não":
            st.session_state.bolacha = "Não"
            st.session_state.pipoca = "Não"
    def atualizar_pipoca():
        if st.session_state.pipoca != "Não":
            st.session_state.bolacha = "Não"
            st.session_state.doce = "Não"

    st.write("### Refeição")
    hamburguer = st.selectbox("Hambúrguer:", ['Não', 'Simples 1 com Ovo', 'Simples 1 com Queijo', 'Simples 2', 'Completo 1', 'Completo 2', 'Duplo 1', 'Duplo 2'], key='hamburguer', on_change=atualizar_hamburguer)
    sandes = st.selectbox("Sandes:", ['Não', 'Rachel ', 'Ovo', 'Palone'], key='sandes', on_change=atualizar_sandes)
    if sandes == 'Rachel ':
        opcao = st.radio("",options=["Com Queijo", 
                                    "Com Ovo", 
                                    "Com Queijo e Ovo", 
                                    "Com Batatas", 
                                    "Com Queijo e Batatas", 
                                    "Com Ovo e Batatas", 
                                    "Com Queijo, Ovo e Batatas"], 
                                    key='opcao')
    batata_asinha = st.selectbox("Batatas/Asinhas/Adicional:", ['Não', '6 Asinhas', '9 Asinhas', 'Dose de Batatas', 'Rachel', 'Ovos', 'Queijo'], key='batata_asinha', on_change=atualizar_batata_asinhas)
    qnt_refeicao = st.slider("Quantidade", 0, 10, 1, key='qnt_refeicao')

    st.write("### Bebidas")
    col4, col5, col6 = st.columns(3)
    with col6:
        refrigerante = st.selectbox("Refresco:", ['Nenhum', 'Garrafa', 'Txoti', '1L', '2L'], key='refrigerante', on_change=atualizar_refrigerante)
    with col5:
        sumo = st.selectbox("Sumo:", ['Nenhum', 'Compal', 'Cappy'], key='sumo', on_change=atualizar_sumo)
    with col4:
        agua = st.selectbox("Água:", ['Nenhuma', 'Água Pequena', 'Água Grande'], key='agua', on_change=atualizar_agua)
    col7, col8 = st.columns(2)
    with col7:
        bebida_garrafa = st.selectbox("Bebida a Garrafa:", ['Nenhum', '2M Txoti', 'Savana', 'Pretinha', 'Lite', 'Heineken Txoti'], key='bebida_garrafa', on_change=atualizar_bebida_garrafa)
    with col8:
        bebida_lata = st.selectbox("Bebida a Lata:", ['Nenhum', '2M', 'Impala', 'MY FAIR', 'Txilar'], key='bebida_lata', on_change=atualizar_bebida_lata)
    qnt_bebidas = st.slider("Quantidade", 0, 10, 1, key='qnt_bebidas')

    st.write("### Bolachas e Doces")
    col1, col2, col3 = st.columns(3)
    with col1:
        bolacha = st.selectbox("Bolachas:", ["Não", "Maria", "Água e Sal", "Coco"], key="bolacha", on_change=atualizar_bolacha)
    with col2:
        doce = st.selectbox("Doces:", ["Não", "Pastilha", "Menta", "PinPop/Yogueta"], key="doce", on_change=atualizar_doce)
    with col3:
        pipoca = st.selectbox("Pipocas:", ["Não", "Pipoca"], key="pipoca", on_change=atualizar_pipoca)
    qnt_guloseimas = st.slider("Quantidade", 0, 10, 1, key="qnt_guloseimas")

    def atualizar_saida(sheet_rs, produto_nome, quantidade):
        produtos = sheet_rs.col_values(1)
        quantidade_total = quantidade
        linhas_produto = [i+1 for i,p in enumerate(produtos) if p == produto_nome]
        # se o produto existe
        if not linhas_produto:
            return False
        total_disponivel = 0
        for linha in linhas_produto:
            restante = sheet_rs.cell(linha, 6).value  # Coluna E = Restante
            restante = int(restante) if restante else 0
            total_disponivel += restante
        if total_disponivel < quantidade:
            return False
        else:
            for linha in linhas_produto:
                restante = int(sheet_rs.cell(linha, 6).value or 0)
                if quantidade_total == 0:
                    break
                if restante > 0:
                    saida_atual = int(sheet_rs.cell(linha, 5).value or 0)  # Coluna D = Saída
                    if quantidade_total <= restante:
                        sheet_rs.update_acell(f"D{linha}", saida_atual + quantidade_total)
                        return True
                    else:
                        sheet_rs.update_acell(f"D{linha}", saida_atual + restante)
                        quantidade_total -= restante

    def main():
        # Lê os dados existentes
        values = sheet.get_all_values()
        values_count = len(values)

        # Escreve a nova linha (automático, não precisa calcular o range)
        sucesso = True

        # --- Hambúrgueres ---
        if "Hambúrguer" in produto_adicionar:
            if "Duplo" in produto_adicionar:
                sucesso &= atualizar_saida(sheet_estoque, "Hambúrguer", quantidade_refeicao2 * 2)
            elif "Completo" in produto_adicionar or "Simples" in produto_adicionar:
                sucesso &= atualizar_saida(sheet_estoque, "Hambúrguer", quantidade_refeicao2)

            if any(p in produto_adicionar for p in ["Simples 1 com Ovo", "Simples 2", "Completo", "Duplo"]):
                sucesso &= atualizar_saida(sheet_estoque, "Ovos", quantidade_refeicao2)

            if any(q in produto_adicionar for q in ["Simples 1 com Queijo", "Completo", "Duplo"]):
                sucesso &= atualizar_saida(sheet_estoque, "Queijo", quantidade_refeicao2)

        # --- Sandes ---
        elif "Sandes" in produto_adicionar:
            if "Sandes de Ovo" in produto_adicionar:
                sucesso &= atualizar_saida(sheet_estoque, "Ovos", quantidade_refeicao2)
            if "Rachel" in produto_adicionar:
                sucesso &= atualizar_saida(sheet_estoque, "Rachel", quantidade_refeicao2)
                if "Ovo" in produto_adicionar:
                    sucesso &= atualizar_saida(sheet_estoque, "Ovos", quantidade_refeicao2)
                if "Queijo" in produto_adicionar:
                    sucesso &= atualizar_saida(sheet_estoque, "Queijo", quantidade_refeicao2)

        # --- Adicional ---
        if produto_adicionar == "Rachel":
            sucesso &= atualizar_saida(sheet_estoque, "Rachel", quantidade_refeicao2)
        elif produto_adicionar == "Ovo":
            sucesso &= atualizar_saida(sheet_estoque, "Ovos", quantidade_refeicao2)
        elif produto_adicionar == "Queijo":
            sucesso &= atualizar_saida(sheet_estoque, "Queijo", quantidade_refeicao2)

        # --- Bebidas ---
        if bebida_adicionar != "Sem Bebida":
            sucesso &= atualizar_saida(sheet_estoque_bebida, bebida_adicionar, quantidade_bebidas2)
    
        if not sucesso:
            st.session_state["mensagem_venda"] = "🚫 Venda Cancelada — Estoque insuficiente para um ou mais produtos"
            st.session_state["tipo_mensagem"] = "erro"
        else:
            # Escreve a nova linha (automático, não precisa calcular o range)
            sheet.append_rows(valores_adicionar, value_input_option="USER_ENTERED")
            st.session_state["mensagem_venda"] = "✅ Venda Registrada com Sucesso!"
            st.session_state["tipo_mensagem"] = "sucesso"


    def reset_inputs():
        st.session_state.hamburguer = 'Não'
        st.session_state.sandes = 'Não'
        st.session_state.batata_asinha = 'Não'
        st.session_state.bolacha = 'Não'
        st.session_state.doce = 'Não'
        st.session_state.pipoca = 'Não'
        st.session_state.refrigerante = 'Nenhum'
        st.session_state.sumo = 'Nenhum'
        st.session_state.agua = 'Nenhuma'
        st.session_state.bebida_garrafa = 'Nenhuma'
        st.session_state.bebida_lata = 'Nenhuma'
        st.session_state.qnt_bebidas = 1
        st.session_state.qnt_refeicao = 1
        st.session_state.qnt_guloseimas = 1

    def registrar():
        global valores_adicionar, produto_adicionar, quantidade_refeicao2, bebida_adicionar, quantidade_bebidas2

        refeicao = "Sem Refeição"
        quantidade_refeicao = 0
        preco_refeicao = 0
        if st.session_state.hamburguer != 'Não' and st.session_state.sandes == 'Não' and st.session_state.batata_asinha == 'Não':
            refeicao = f'Hambúrguer {st.session_state.hamburguer}'
            if st.session_state.hamburguer == "Simples 1 com Ovo" or st.session_state.hamburguer == "Simples 1 com Queijo":
                preco_refeicao = 100
            if st.session_state.hamburguer == "Simples 2":
                preco_refeicao = 150
            if st.session_state.hamburguer == "Completo 1":
                preco_refeicao = 120
            if st.session_state.hamburguer == "Completo 2":
                preco_refeicao = 170
            if st.session_state.hamburguer == "Duplo 1":
                preco_refeicao = 140
            if st.session_state.hamburguer == "Duplo 2":
                preco_refeicao = 190
        elif st.session_state.sandes != 'Não' and st.session_state.hamburguer == 'Não' and st.session_state.batata_asinha == 'Não':
            if st.session_state.sandes == 'Rachel ':
                refeicao = f"Sandes de {st.session_state.sandes}{st.session_state.opcao}"
                if st.session_state.opcao == "Com Ovo" or st.session_state.opcao == "Com Queijo":
                    preco_refeicao = 60
                if st.session_state.opcao == "Com Queijo e Batatas" or st.session_state.opcao == "Com Ovo e Batatas":
                    preco_refeicao = 110
                if st.session_state.opcao == "Com Batatas":
                    preco_refeicao = 100
                if st.session_state.opcao == "Com Queijo e Ovo":
                    preco_refeicao = 70
                if st.session_state.opcao == "Com Queijo, Ovo e Batatas":
                    preco_refeicao = 120
            else:
                refeicao = f'Sandes de {st.session_state.sandes}'
                if st.session_state.sandes == "Ovo" or st.session_state.sandes == "Palone":
                    preco_refeicao = 30
        elif st.session_state.batata_asinha != 'Não' and st.session_state.hamburguer == 'Não' and st.session_state.sandes == 'Não':
            refeicao = st.session_state.batata_asinha
            if st.session_state.batata_asinha == "6 Asinhas":
                preco_refeicao = 100
            if st.session_state.batata_asinha == "9 Asinhas":
                preco_refeicao = 150
            if st.session_state.batata_asinha == "Dose de Batatas":
                preco_refeicao = 60
            if st.session_state.batata_asinha == "Rachel":
                preco_refeicao = 30
            if st.session_state.batata_asinha == "Ovos":
                preco_refeicao = 10
            if st.session_state.batata_asinha == "Queijo":
                preco_refeicao = 20
        if refeicao != "Sem Refeição":
            quantidade_refeicao = st.session_state.qnt_refeicao

        bebida = "Sem Bebida"
        quantidade_bebida = 0
        preco_bebidas = 0
        if st.session_state.refrigerante != "Nenhum":
            bebida = f"Refresco {st.session_state.refrigerante}"
            if st.session_state.refrigerante == "Garrafa" or st.session_state.refrigerante == "Txoti":
                preco_bebidas = 25
            if st.session_state.refrigerante == "1L":
                preco_bebidas = 60
            if st.session_state.refrigerante == "2L":
                preco_bebidas = 110
        elif st.session_state.sumo != "Nenhum":
            bebida = f"Sumo {st.session_state.sumo}"
            if st.session_state.sumo == "Compal":
                preco_bebidas = 65
            if st.session_state.sumo == "Cappy":
                preco_bebidas = 35
        elif st.session_state.agua != "Nenhuma":
            bebida = st.session_state.agua
            if st.session_state.agua == "Água Pequena":
                preco_bebidas = 25
            if st.session_state.agua == "Água Grande":
                preco_bebidas = 50
        elif st.session_state.bebida_garrafa != "Nenhuma":
            bebida = st.session_state.bebida_garrafa
            if st.session_state.bebida_garrafa == "2M Txoti":
                preco_bebidas = 60
            if st.session_state.bebida_garrafa == "Savana":
                preco_bebidas = 80
            if st.session_state.bebida_garrafa == "Pretinha":
                preco_bebidas = 55
            if st.session_state.bebida_garrafa == "Lite":
                preco_bebidas = 70
            if st.session_state.bebida_garrafa == "Heineken Txoti":
                preco_bebidas = 85
        elif st.session_state.bebida_lata != "Nenhuma":
            bebida = st.session_state.bebida_lata if st.session_state.bebida_lata == 'MY FAIR' else f'{st.session_state.bebida_lata} Lata'
            if st.session_state.bebida_lata == "2M":
                preco_bebidas = 60
            if st.session_state.bebida_lata == "Impala":
                preco_bebidas = 50
            if st.session_state.bebida_lata == "MY FAIR":
                preco_bebidas = 95
            if st.session_state.bebida_lata == "Txilar":
                preco_bebidas = 55
        if bebida != "Sem Bebida":
            quantidade_bebida = st.session_state.qnt_bebidas

        guloseima = "Sem Guloseima"
        quantidade_guloseima = 0
        preco_guloseima = 0
        if st.session_state.bolacha != "Não" and st.session_state.doce == "Não" and st.session_state.pipoca == "Não":
            guloseima = f'Bolacha {st.session_state.bolacha}'
            preco_guloseima = 20
        if st.session_state.bolacha == "Não" and st.session_state.doce != "Não" and st.session_state.pipoca == "Não":
            guloseima = st.session_state.doce
            if st.session_state.doce == "PinPop/Yogueta":
                preco_guloseima = 5
            else:
                preco_guloseima = 2
        if st.session_state.bolacha == "Não" and st.session_state.doce == "Não" and st.session_state.pipoca != "Não":
            guloseima = st.session_state.pipoca
            preco_guloseima = 6
        if guloseima != "Sem Guloseima":
            quantidade_guloseima = st.session_state.qnt_guloseimas

        total = (preco_bebidas * quantidade_bebida) + (preco_refeicao * quantidade_refeicao) + (preco_guloseima * quantidade_guloseima)

        valores_adicionar = [
            [date, refeicao, quantidade_refeicao, preco_refeicao, guloseima, quantidade_guloseima, preco_guloseima, bebida, quantidade_bebida, preco_bebidas, total]
        ]
        bebida_adicionar = valores_adicionar[0][7]
        produto_adicionar = valores_adicionar[0][1]
        quantidade_refeicao2 = valores_adicionar[0][2]
        quantidade_bebidas2 = valores_adicionar[0][8]

        main()
        reset_inputs()

    container = st.container()
    but1, but2 = st.columns(2)
    with but1:
        st.button("Registrar", on_click=registrar)
    with but2:
        if st.button("Sair"):
            st.session_state.authenticated = False
            st.rerun()
    if "mensagem_venda" in st.session_state:
        if st.session_state["tipo_mensagem"] == "sucesso":
            with container:
                st.success(st.session_state["mensagem_venda"])
        elif st.session_state["tipo_mensagem"] == "erro":
            with container:
                st.error(st.session_state["mensagem_venda"])

if options == 'Estoque':
    st.title("📦 Gerenciamento de Estoque")

    if "produto1" not in st.session_state:
        st.session_state.produto1 = 'Não'
    if "produto2" not in st.session_state:
        st.session_state.produto2 = 'Não'
    if "produto3" not in st.session_state:
        st.session_state.produto3 = 'Não'
    if "produto4" not in st.session_state:
        st.session_state.produto4 = 'Não'
    if "preco_produto4" not in st.session_state:
        st.session_state.preco_produto4 = 0
    if "preco_produto123" not in st.session_state:
        st.session_state.preco_produto123 = 0
    
    def atualizar_produto1():
        if st.session_state.produto1 != "Não":
            st.session_state.produto2 = "Não"
            st.session_state.produto3 = "Não"
            st.session_state.produto4 = "Não"
            st.session_state.preco_produto4 = 0
    def atualizar_produto2():
        if st.session_state.produto2 != "Não":
            st.session_state.produto1 = "Não"
            st.session_state.produto3 = "Não"
            st.session_state.produto4 = "Não"
            st.session_state.preco_produto4 = 0
    def atualizar_produto3():
        if st.session_state.produto3 != "Não":
            st.session_state.produto2 = "Não"
            st.session_state.produto1 = "Não"
            st.session_state.produto4 = "Não"
            st.session_state.preco_produto4 = 0
    def atualizar_produto4():
        if st.session_state.produto4 != "Não":
            st.session_state.produto2 = "Não"
            st.session_state.produto1 = "Não"
            st.session_state.produto3 = "Não"
            st.session_state.preco_produto123 = 0
    def atualizar_preco_produto4():
        if st.session_state.preco_produto4 != 0:
            st.session_state.preco_produto123 = 0
            st.session_state.produto2 = "Não"
            st.session_state.produto1 = "Não"
            st.session_state.produto3 = "Não"
    def atualizar_preco_produto123():
        if st.session_state.preco_produto123 != 0:
            st.session_state.preco_produto4 = 0
            st.session_state.produto4 = "Não"

    col9, col10, col11 = st.columns(3)
    with col9:
        produto1 = st.selectbox("Produto:", ['Não', 'Hambúrguer', 'Ovos', 'Queijo', 'Rachel'], key='produto1', on_change=atualizar_produto1)
    with col10:
        produto2 = st.selectbox("Bebida:", ['Não', '2M Txoti', '2M Lata', 'Savana', 'Pretinha', 'Lite', 'Heineken Txoti', 'Impala Lata', 'MY FAIR', 'Txilar Lata'], key='produto2', on_change=atualizar_produto2)
    with col11:
        produto3 = st.selectbox("Água/Sumo/Refrigerante:", ['Não', 'Água Pequena', 'Água Grande', 'Sumo Cappy', 'Sumo Compal', 'Refresco Garrafa', 'Refresco Txoti', 'Refresco 1L', 'Refresco 2L'], key='produto3', on_change=atualizar_produto3)
    preco_produto123 = st.number_input("Preço:", key="preco_produto123", on_change=atualizar_preco_produto123)
    if produto1 == "Hambúrguer":
        qnt_hamburguer = st.slider("Quantidade", 0, 150, 50, key="qnt_hamburguer")
    else:
        qnt_estoque = st.slider("Quantidade", 0, 20, 1, key="qnt_estoque")
    st.write("### Estoque Paralelo")
    pr, p = st.columns(2)
    with pr:
        produto4 = st.selectbox("Produto:", ["Não", "Batatas", "Palone", "Mayonnaise", "Tomato Sauce", "Óleo"], key='produto4', on_change=atualizar_produto4)
    with p:
        preco_produto4 = st.number_input("Preço:", key="preco_produto4", on_change=atualizar_preco_produto4)
    qnt_estoque2 = st.slider("Quantidade", 0, 10, 1, key="qnt_estoque2")


    def estoque():
        global estoque_produto, quantidade_estoque, preco_produto_paralelo, preco_produto_estoque

        estoque_produto = 'Sem Reposição'
        quantidade_estoque = 0
        preco_produto_paralelo = 0
        preco_produto_estoque = 0
        if st.session_state.produto1 != "Não" and st.session_state.produto2 == 'Não' and st.session_state.produto3 == 'Não' and st.session_state.produto4 == 'Não':
            estoque_produto = st.session_state.produto1
            if st.session_state.produto1 == "Hambúrguer":
                quantidade_estoque = st.session_state.qnt_hamburguer
            if st.session_state.produto1 == "Ovos":
                quantidade_estoque = st.session_state.qnt_estoque * 6
            if st.session_state.produto1 == "Palone":
                quantidade_estoque = st.session_state.qnt_estoque
            if st.session_state.produto1 == "Rachel":
                quantidade_estoque = st.session_state.qnt_estoque * 10
            if st.session_state.produto1 == "Queijo":
                quantidade_estoque = st.session_state.qnt_estoque * 12
            preco_produto_estoque = preco_produto123
            sheet_estoque_atualizar()
        if st.session_state.produto1 == "Não" and st.session_state.produto2 != 'Não' and st.session_state.produto3 == 'Não'and st.session_state.produto4 == 'Não':
            estoque_produto = st.session_state.produto2
            quantidade_estoque = st.session_state.qnt_estoque * 6
            preco_produto_estoque = preco_produto123
            sheet_estoque_atualizar_bebida()
        if st.session_state.produto1 == "Não" and st.session_state.produto2 == 'Não' and st.session_state.produto3 != 'Não'and st.session_state.produto4 == 'Não':
            estoque_produto = st.session_state.produto3
            if st.session_state.produto3 == "Água Pequena" or st.session_state.produto3 == "Sumo Cappy" or st.session_state.produto3 == "Refresco Txoti":
                quantidade_estoque = st.session_state.qnt_estoque * 12
            elif st.session_state.produto3 == "Refresco 1L" or st.session_state.produto3 == "Refresco 2L" or st.session_state.produto3 == "Água Grande":
                quantidade_estoque = st.session_state.qnt_estoque * 6
            elif st.session_state.produto3 == "Refresco Garrafa":
                quantidade_estoque = st.session_state.qnt_estoque * 24
            elif st.session_state.produto3 == "Sumo Compal":
                quantidade_estoque = st.session_state.qnt_estoque * 10
            preco_produto_estoque = preco_produto123
            sheet_estoque_atualizar_bebida()
        if st.session_state.produto1 == "Não" and st.session_state.produto2 == 'Não' and st.session_state.produto3 == 'Não'and st.session_state.produto4 != 'Não':
            estoque_produto = st.session_state.produto4
            quantidade_estoque = st.session_state.qnt_estoque2
            preco_produto_paralelo = st.session_state.preco_produto4
            sheet_estoque_paralelo_atualizar()

        repor_valores()

    def sheet_estoque_atualizar():
        global count

        values = sheet_estoque.get_all_values()
        count = len(values) + 1

        estoque_adicionar = [[estoque_produto, date, quantidade_estoque, preco_produto_estoque, 0, f"=C{count}-D{count}", f'=SE(E{count}<10;"Crítico";SE(E{count}<20;"Alerta";"Normal"))']]
        sheet_estoque.append_rows(estoque_adicionar, value_input_option="USER_ENTERED")
    def sheet_estoque_paralelo_atualizar():
        global count3

        values = sheet_estoque.get_all_values()
        count3 = len(values) + 1

        estoque_adicionar = [[estoque_produto, date, quantidade_estoque, preco_produto_paralelo]]
        sheet_estoque_paralelo.append_rows(estoque_adicionar, value_input_option="USER_ENTERED")
    def sheet_estoque_atualizar_bebida():
        global count2

        values = sheet_estoque_bebida.get_all_values()
        count2 = len(values) + 1

        estoque_adicionar = [[estoque_produto, date, quantidade_estoque, preco_produto_estoque, 0, f"=C{count2}-D{count2}", f'=SE(E{count2}<6;"Crítico";SE(E{count2}<12;"Alerta";"Normal"))']]
        sheet_estoque_bebida.append_rows(estoque_adicionar, value_input_option="USER_ENTERED")

    def repor_valores():
        st.session_state.produto1 = 'Não'
        st.session_state.produto2 = 'Não'
        st.session_state.produto3 = 'Não'
        st.session_state.produto4 = 'Não'
        st.session_state.preco_produto4 = 0
        st.session_state.preco_produto123 = 0
        st.session_state.qnt_estoque = 1
        st.session_state.qnt_estoque2 = 1

    st.button("Registrar Entrada", on_click=estoque)

if options == 'Relatório':
    st.title("📊 Dashboards e Relatórios")
    dts = datetime.today()
    def bordered_chart(fig):
        fig.add_shape(
                    type="rect",
                    xref="paper",
                    yref="paper",
                    x0=0,
                    y0=0,
                    x1=1,
                    y1=1,
                    line=dict(
                        color="white",
                        width=2,
                    ))
        st.plotly_chart(fig, use_container_width=True)
        
    if aba == 'Relatório de Vendas':
        dados_vendas = sheet.get_all_values()
        data = pd.DataFrame(dados_vendas[1:], columns=dados_vendas[0])
        data["Qnt_Refeição"] = pd.to_numeric(data["Qnt_Refeição"], errors="coerce")
        data["Qnt_Bebida"] = pd.to_numeric(data["Qnt_Bebida"], errors="coerce")
        data["Qnt_Guloseima"] = pd.to_numeric(data["Qnt_Guloseima"], errors="coerce")
        data["Preço_Unitário_Refeição"] = pd.to_numeric(data["Preço_Unitário_Refeição"], errors="coerce")
        data["Preço_Unitário_Guloseima"] = pd.to_numeric(data["Preço_Unitário_Guloseimas"], errors="coerce")
        data["Preço_Unitário_Bebida"] = pd.to_numeric(data["Preço_Unitário_Bebidas"], errors="coerce")
        data["Total"] = pd.to_numeric(data["Total"], errors="coerce")
        data["total_refeicao"] = (data["Qnt_Refeição"])*(data["Preço_Unitário_Refeição"])
        data["total_bebida"] = (data["Qnt_Bebida"])*(data["Preço_Unitário_Bebida"])
        data["total_guloseima"] = (data["Qnt_Guloseima"])*(data["Preço_Unitário_Guloseima"])
        data["Data_Venda"] = pd.to_datetime(data["Data_Venda"], format="%d-%m-%Y")
        data["Data"] = data["Data_Venda"].dt.date
        date_ontem = dts.date() - timedelta(days=1)
        date_ontem2 = dts.date() - timedelta(days=2)
        date_7 = (dts - timedelta(days=7))
        date_14 = (dts - timedelta(days=14))
        date_30 = (dts - timedelta(days=30))
        date_60 = (dts - timedelta(days=60))
        fil1, fil2 = st.columns(2)
        with fil1:
            filtro_categoria = st.selectbox("Categoria", ["Todos", "Produtos Alimentícios", "Bebidas"])
        with fil2:
            filtro_data = st.selectbox("Data", ["Hoje", "Ontem", "Últimos 7 dias", "Últimos 30 dias"])
        st.divider()
        if filtro_categoria == "Todos":
            if filtro_data == "Hoje":
                data_anterior = data[data["Data"] == date_ontem]
                data = data[data["Data_Venda"] == date]
                data_geral = data[data["Data_Venda"] == date]
            elif filtro_data == "Ontem":
                data_anterior = data[data["Data"] == date_ontem2]
                data = data[data["Data"] == date_ontem]
                data_geral = data[data["Data"] == date_ontem]
            elif filtro_data == "Últimos 7 dias":
                data_anterior = data[(data["Data_Venda"] >= date_14) & (data["Data_Venda"] <= date_7)]
                data = data[data["Data_Venda"] >= date_7]
                data_geral = data[data["Data_Venda"] >= date_7]
                msg = "a Semana"
            elif filtro_data == "Últimos 30 dias":
                data_anterior = data[(data["Data_Venda"] >= date_60) & (data["Data_Venda"] <= date_30)]
                data = data[data["Data_Venda"] >= date_30]
                data_geral = data[data["Data_Venda"] >= date_30]
                msg = "o Mês"
            
            if data.empty:
                st.write("### Sem Vendas Realizadas Ainda!")
            else:
                data_refeicao = data[data["Refeição"] != "Sem Refeição"]
                data_bebida = data[data["Bebida"] != "Sem Bebida"]
                kp1, kp2 = st.columns(2)
                with kp1:
                    faturamento = data_geral["Total"].sum()
                    faturamento2 = data_anterior["Total"].sum()
                    diferenca = (faturamento - faturamento2) if not data_anterior.empty else 0
                    diferenca = int(diferenca) if diferenca else 0
                    st.metric("Faturamento Total", f'{faturamento}.00 MZN', delta=f"{diferenca}.00 MZN", border=True, delta_color="off" if diferenca == 0 else "normal")
                with kp2:
                    volume1 = data_geral["Qnt_Bebida"].sum()
                    volume2 = data_geral["Qnt_Guloseima"].sum()
                    volume3 = data_geral["Qnt_Refeição"].sum()
                    volume = volume1 + volume2 + volume3
                    volume4 = data_anterior["Qnt_Bebida"].sum()
                    volume5 = data_anterior["Qnt_Guloseima"].sum()
                    volume6 = data_anterior["Qnt_Refeição"].sum()
                    volume_anterior = volume4 + volume5 + volume6
                    volume_diferenca = (volume - volume_anterior) if not data_anterior.empty else 0
                    volume_diferenca = int(volume_diferenca) if volume_diferenca else 0
                    st.metric("Volume de Vendas Total", f'{volume} Vendidos', delta=volume_diferenca, border=True, delta_color="off" if volume_diferenca == 0 else "normal")
                st.divider()
                df_junto = data.melt(
                                        id_vars=["Data_Venda"],
                                        value_vars=["total_refeicao", "total_bebida", "total_guloseima"],
                                        var_name="Categoria",
                                        value_name="Quantidade"
                                        )
                df_sum_tot = df_junto.groupby("Categoria", as_index=False)["Quantidade"].sum()
                fig_pie1 = px.pie(df_sum_tot, values="Quantidade", names="Categoria", title="Faturamento por Categoria", hole=.4)
                st.plotly_chart(fig_pie1, use_container_width=True)
                st.divider()
                df_junto = data.melt(
                                        id_vars=["Data_Venda"],
                                        value_vars=["Qnt_Refeição", "Qnt_Bebida", "Qnt_Guloseima"],
                                        var_name="Categoria",
                                        value_name="Quantidade"
                                        )
                df_sum_qnt = df_junto.groupby("Categoria", as_index=False)["Quantidade"].sum()
                fig_pie2 = px.pie(df_sum_qnt, values="Quantidade", names="Categoria", title="Volume de Vendas por Categoria", hole=.4)
                st.plotly_chart(fig_pie2, use_container_width=True)
                st.divider()
                if filtro_data == "Últimos 7 dias" or filtro_data == "Últimos 30 dias":
                    data["Qnt_Total"] = data["Qnt_Refeição"] + data["Qnt_Bebida"] + data["Qnt_Guloseima"]
                    
                    df_grouped = (data.groupby("Data_Venda", as_index=False)
                                    .agg({"Qnt_Total": "sum"})  # soma as quantidades por data
                                    )
                    fig_line = px.line(df_grouped, x="Data_Venda", y="Qnt_Total", markers=True, title=f"Volume de Vendas ao Longo d{msg}")
                    fig_line.update_xaxes(tickformat="%d-%m-%Y")
                    bordered_chart(fig_line)


        elif filtro_categoria == "Produtos Alimentícios":
            data1 = data[data["Refeição"] != "Sem Refeição"]
            if filtro_data == "Hoje":
                data_anterior = data[data["Data"] == date_ontem]
                data1 = data1[data1["Data_Venda"] == date]
                data_geral = data[data["Data_Venda"] == date]
            elif filtro_data == "Ontem":
                data_anterior = data[data["Data"] == date_ontem2]
                data1 = data1[data1["Data"] == date_ontem]
                data_geral = data[data["Data"] == date_ontem]
            elif filtro_data == "Últimos 7 dias":
                data_anterior = data[(data["Data_Venda"] >= date_14) & (data["Data_Venda"] <= date_7)]
                data1 = data1[data1["Data_Venda"] >= date_7]
                data_geral = data[data["Data_Venda"] >= date_7]
                msg = "a Semana"
            elif filtro_data == "Últimos 30 dias":
                data_anterior = data[(data["Data_Venda"] >= date_60) & (data["Data_Venda"] <= date_30)]
                data1 = data1[data1["Data_Venda"] >= date_30]
                data_geral = data[data["Data_Venda"] >= date_30]
                msg = "o Mês"

            if data1.empty:
                st.write("### Sem Vendas Realizadas Ainda!")
            else:
                vendas_por_produto = data1.groupby("Refeição")["Qnt_Refeição"].sum().reset_index()
                mais_vendido = vendas_por_produto.loc[vendas_por_produto["Qnt_Refeição"].idxmax(), "Refeição"]
                kp1, kp2, kp3 = st.columns(3)
                with kp1:
                    faturamento = data_geral["Total"].sum()
                    faturamento2 = data_anterior["Total"].sum()
                    diferenca = (faturamento - faturamento2) if not data_anterior.empty else 0
                    diferenca = int(diferenca) if diferenca else 0
                    st.metric("Faturamento Total", f'{faturamento}.00 MZN', delta=f"{diferenca}.00 MZN", border=True, delta_color="off" if diferenca == 0 else "normal")
                with kp2:
                    volume1 = data_geral["Qnt_Bebida"].sum()
                    volume2 = data_geral["Qnt_Guloseima"].sum()
                    volume3 = data_geral["Qnt_Refeição"].sum()
                    volume = volume1 + volume2 + volume3
                    volume4 = data_anterior["Qnt_Bebida"].sum()
                    volume5 = data_anterior["Qnt_Guloseima"].sum()
                    volume6 = data_anterior["Qnt_Refeição"].sum()
                    volume_anterior = volume4 + volume5 + volume6
                    volume_diferenca = (volume - volume_anterior) if not data_anterior.empty else 0
                    volume_diferenca = int(volume_diferenca) if volume_diferenca else 0
                    st.metric("Volume de Vendas Total", f'{volume} Vendidos', delta=volume_diferenca, border=True, delta_color="off" if volume_diferenca == 0 else "normal")
                with kp3:
                    st.metric("Produto mais vendido", mais_vendido, border=True)
                st.divider()
                fig_bar1 = px.bar(data1, x="Refeição", y="Total", title="Faturamento por Refeição")
                bordered_chart(fig_bar1)
                st.divider()
                fig_bar2 = px.bar(data1, x="Refeição", y="Qnt_Refeição", title="Volume de Vendas por Refeição")
                bordered_chart(fig_bar2)
                st.divider()
                if filtro_data == "Últimos 7 dias" or filtro_data == "Últimos 30 dias":
                    df_grouped = (data1.groupby("Data_Venda", as_index=False)
                                    .agg({"Qnt_Refeição": "sum"})  # soma as quantidades por data
                                    )
                    fig_line = px.line(df_grouped, x="Data_Venda", y="Qnt_Refeição", markers=True, title=f"Volume de Vendas ao Longo d{msg}")
                    fig_line.update_xaxes(tickformat="%d-%m-%Y")
                    bordered_chart(fig_line)


        elif filtro_categoria == "Bebidas":
            data1 = data[data["Bebida"] != "Sem Bebida"]
            if filtro_data == "Hoje":
                data_anterior = data[data["Data"] == date_ontem]
                data1 = data1[data1["Data_Venda"] == date]
                data_geral = data[data["Data_Venda"] == date]
            elif filtro_data == "Ontem":
                data_anterior = data[data["Data"] == date_ontem2]
                data1 = data1[data1["Data"] == date_ontem]
                data_geral = data[data["Data"] == date_ontem]
            elif filtro_data == "Últimos 7 dias":
                data_anterior = data[(data["Data_Venda"] >= date_14) & (data["Data_Venda"] <= date_7)]
                data1 = data1[data1["Data_Venda"] >= date_7]
                data_geral = data[data["Data_Venda"] >= date_7]
                msg = "a Semana"
            elif filtro_data == "Últimos 30 dias":
                data_anterior = data[(data["Data_Venda"] >= date_60) & (data["Data_Venda"] <= date_30)]
                data1 = data1[data1["Data_Venda"] >= date_30]
                data_geral = data[data["Data_Venda"] >= date_30]
                msg = "o Mês"

            if data1.empty:
                st.write("### Sem Vendas Realizadas Ainda!")
            else:
                vendas_por_produto = data1.groupby("Bebida")["Qnt_Bebida"].sum().reset_index()
                mais_vendido = vendas_por_produto.loc[vendas_por_produto["Qnt_Bebida"].idxmax(), "Bebida"]
                kp1, kp2, kp3 = st.columns(3)
                with kp1:
                    faturamento = data_geral["Total"].sum()
                    faturamento2 = data_anterior["Total"].sum()
                    diferenca = (faturamento - faturamento2) if not data_anterior.empty else 0
                    diferenca = int(diferenca) if diferenca else 0
                    st.metric("Faturamento Total", f'{faturamento}.00 MZN', delta=f"{diferenca}.00 MZN", border=True, delta_color="off" if diferenca == 0 else "normal")
                with kp2:
                    volume1 = data_geral["Qnt_Bebida"].sum()
                    volume2 = data_geral["Qnt_Guloseima"].sum()
                    volume3 = data_geral["Qnt_Refeição"].sum()
                    volume = volume1 + volume2 + volume3
                    volume4 = data_anterior["Qnt_Bebida"].sum()
                    volume5 = data_anterior["Qnt_Guloseima"].sum()
                    volume6 = data_anterior["Qnt_Refeição"].sum()
                    volume_anterior = volume4 + volume5 + volume6
                    volume_diferenca = (volume - volume_anterior) if not data_anterior.empty else 0
                    volume_diferenca = int(volume_diferenca) if volume_diferenca else 0
                    st.metric("Volume de Vendas Total", f'{volume} Vendidos', delta=volume_diferenca, border=True, delta_color="off" if volume_diferenca == 0 else "normal")
                with kp3:
                    st.metric("Bebida mais vendida", mais_vendido, border=True)
                st.divider()
                fig_bar1 = px.bar(data1, x="Bebida", y="Total", title="Faturamento por Bebida")
                bordered_chart(fig_bar1)
                st.divider()
                fig_bar2 = px.bar(data1, x="Bebida", y="Qnt_Bebida", title="Volume de Vendas por Bebida")
                bordered_chart(fig_bar2)
                st.divider()
                if filtro_data == "Últimos 7 dias" or filtro_data == "Últimos 30 dias":
                    df_grouped = (data1.groupby("Data_Venda", as_index=False)
                                    .agg({"Qnt_Bebida": "sum"})  # soma as quantidades por data
                                    )
                    fig_line = px.line(df_grouped, x="Data_Venda", y="Qnt_Bebida", markers=True, title=f"Volume de Vendas ao Longo d{msg}")
                    fig_line.update_xaxes(tickformat="%d-%m-%Y")
                    bordered_chart(fig_line)

        def relatorio():
            date_relatorio = dts.date()
            if filtro_categoria == "Todos":
                cat_most_selled = df_sum_qnt.max()
                if cat_most_selled[0] == "Qnt_Refeição":
                    mais_vendido_todos = "Refeição"
                elif cat_most_selled[0] == "Qnt_Guloseima":
                    mais_vendido_todos = "Guloseima"
                else:
                    mais_vendido_todos = "Bebidas"
                most_selled = f'A Categoria com mais Vendas foi: {mais_vendido_todos}.'
                if filtro_data == "Hoje" or filtro_data == "Ontem":
                    fig_pie1.write_image("Figura1.jpg", engine='kaleido', scale=2)
                    fig1 = "Figura1.jpg"
                    writter = f'Faturamento por Categoria de Produtos e Bebidas'
                    fig_pie2.write_image("Figura2.jpg", engine='kaleido', scale=2)
                    fig2 = "Figura2.jpg"
                    writter2 = f'Volume de Vendas por Categoria de Produtos e Bebidas'
                    data_relatorio = f'{date}' if filtro_data == "Hoje" else f'{date_ontem}'
                else:
                    fig_pie1.write_image("Figura1.jpg", engine='kaleido', scale=2)
                    fig1 = "Figura1.jpg"
                    writter = f'Faturamento por Categoria de Produtos e Bebidas'
                    fig_pie2.write_image("Figura2.jpg", engine='kaleido', scale=2)
                    fig2 = "Figura2.jpg"
                    writter2 = f'Volume de Vendas por Categoria de Produtos e Bebidas'
                    fig_line.write_image("Figura3.jpg", engine='kaleido', scale=2)
                    fig3 = "Figura3.jpg"
                    writter3 = f'Volume de Vendas ao Longo da Semana' if filtro_data == 'Últimos 7 dias' else f'Volume de Vendas ao Longo do Mês'
                    data_relatorio = f'{date_7.date()} a {date_relatorio}' if filtro_data == "Últimos 7 dias" else f'{date_30.date()} a {date_relatorio}'
            else:
                most_selled = f'A Refeição mais Vendida foi: {mais_vendido}.' if filtro_categoria == "Produtos Alimentícios" else f'A Bebida mais Vendida foi: {mais_vendido}.'
                if filtro_data == "Hoje" or filtro_data == "Ontem":
                    fig_bar1.write_image("Figura1.jpg", engine='kaleido', scale=2)
                    fig1 = "Figura1.jpg"
                    writter = f'Faturamento por Refeição' if filtro_categoria == "Produtos Alimentícios" else f'Faturamento por Bebida'
                    fig_bar2.write_image("Figura2.jpg", engine='kaleido', scale=2)
                    fig2 = "Figura2.jpg"
                    writter2 = f'Volume de Vendas por Refeição' if filtro_categoria == "Produtos Alimentícios" else f'Volume de Vendas por Bebida'
                    data_relatorio = f'{date}' if filtro_data == "Hoje" else f'{date_ontem}'
                else:
                    fig_bar1.write_image("Figura1.jpg", engine='kaleido', scale=2)
                    fig1 = "Figura1.jpg"
                    writter = f'Faturamento por Refeição' if filtro_categoria == "Produtos Alimentícios" else f'Faturamento por Bebida'
                    fig_bar2.write_image("Figura2.jpg", engine='kaleido', scale=2)
                    fig2 = "Figura2.jpg"
                    writter2 = f'Volume de Vendas por Refeição' if filtro_categoria == "Produtos Alimentícios" else f'Volume de Vendas por Bebida'
                    fig_line.write_image("Figura3.jpg", engine='kaleido', scale=2)
                    fig3 = "Figura3.jpg"
                    writter3 = f'Volume de Vendas ao Longo da Semana' if filtro_data == 'Últimos 7 dias' else f'Volume de Vendas ao Longo do Mês'
                    data_relatorio = f'{date_7.date()} a {date_relatorio}' if filtro_data == "Últimos 7 dias" else f'{date_30.date()} a {date_relatorio}'

            documento_pdf = canvas.Canvas('Relatorio de Vendas.pdf', A4)

            documento_pdf.setFont('Helvetica-Bold', 18)
            if filtro_data == "Hoje" or filtro_data == "Ontem":
                documento_pdf.drawString(150, 765, f'Relatório de Vendas de {data_relatorio}')
            else:
                documento_pdf.drawString(90, 765, f'Relatório de Vendas de {data_relatorio}')

            # escrever o texto
            documento_pdf.setFont('Helvetica', 12)
            documento_pdf.drawString(75, 700, f'O Faturamento Total é de: {faturamento}.00 MZN.')
            documento_pdf.drawString(75, 675, f'O Volume total de Vendas é de: {volume}.')
            documento_pdf.drawString(75, 650, f'{most_selled}')
            documento_pdf.drawString(75, 600, f'{writter}:')
            documento_pdf.drawImage(fig1, 75, 330, width=500, height=265)
            documento_pdf.drawString(75, 270, f'{writter2}:')
            documento_pdf.drawImage(fig2, 75, 0, width=500, height=265)
            if filtro_data == "Últimos 7 dias" or filtro_data == "Últimos 30 dias":
                documento_pdf.showPage()
                documento_pdf.setFont('Helvetica', 12)
                documento_pdf.drawString(75, 765, f'{writter3}:')
                documento_pdf.drawImage(fig3, 75, 495, width=500, height=265)

            # salvar relatorio
            documento_pdf.save()

        but3, but4 = st.columns(2)
        with but3:
            if st.button("🔄 Atualizar Dados"):
                st.rerun()
        with but4:
            if not data.empty:
                st.button("⏬ Baixar Relatório", on_click=relatorio)
    
    if aba == 'Relatório de Estoque':
        categoria = st.selectbox("Categoria", ["Produtos Alimentícios", "Bebidas"])
        if categoria == "Produtos Alimentícios":
            st.columns(3)[1].write("### Produtos Alimentícios")
            st.divider()
            dados_estoque = sheet_estoque.get_all_values()
            data_estoque = pd.DataFrame(dados_estoque[1:], columns=dados_estoque[0])
            data_estoque["Quantidade_Restante"] = pd.to_numeric(data_estoque["Quantidade_Restante"], errors="coerce")
            data_estoque["Saída"] = pd.to_numeric(data_estoque["Saída"], errors="coerce")
            data_estoque["Entrada"] = pd.to_numeric(data_estoque["Entrada"], errors="coerce")
            color_discrete_map={
                    "Crítico": "#dc3545",
                    "Alerta": "#ffc107",
                    "Normal": "#28a745"
                }
            fig = px.bar(data_estoque, x="Quantidade_Restante", y="Produto", color="Nível de Estoque", color_discrete_map=color_discrete_map, orientation="h", title="Quantidade Restante")
            bordered_chart(fig)
            st.divider()
            df_melted = data_estoque.melt(
            id_vars=["Produto"],
            value_vars=["Entrada", "Saída"],
            var_name="Tipo",
            value_name="Quantidade"
            )
            fig = px.bar(df_melted, x="Produto", y="Quantidade", color="Tipo", barmode="group", title="Entrada vs Saída")
            bordered_chart(fig)
        if categoria == "Bebidas":
            st.columns(3)[1].write("### Bebidas")
            dados_estoque_bebidas = sheet_estoque_bebida.get_all_values()
            data_estoque_bebidas = pd.DataFrame(dados_estoque_bebidas[1:], columns=dados_estoque_bebidas[0])
            data_estoque_bebidas["Quantidade_Restante"] = pd.to_numeric(data_estoque_bebidas["Quantidade_Restante"], errors="coerce")
            data_estoque_bebidas["Saída"] = pd.to_numeric(data_estoque_bebidas["Saída"], errors="coerce")
            data_estoque_bebidas["Entrada"] = pd.to_numeric(data_estoque_bebidas["Entrada"], errors="coerce")
            color_discrete_map={
                    "Crítico": "#dc3545",
                    "Alerta": "#ffc107",
                    "Normal": "#28a745"
                }
            fig = px.bar(data_estoque_bebidas, x="Quantidade_Restante", y="Bebida",color="Nível de Estoque", color_discrete_map=color_discrete_map, orientation="h", title="Quantidade Restante")
            bordered_chart(fig)
            st.divider()
            df_melted = data_estoque_bebidas.melt(
            id_vars=["Bebida"],
            value_vars=["Entrada", "Saída"],
            var_name="Tipo",
            value_name="Quantidade"
            )
            fig = px.bar(df_melted, x="Bebida", y="Quantidade", color="Tipo", barmode="group", title="Entrada vs Saída")
            bordered_chart(fig)
        
        if st.button("🔄 Atualizar Dados"):
            st.rerun()
