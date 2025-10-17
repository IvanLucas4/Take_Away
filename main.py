import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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
    batata_asinha = st.selectbox("Batatas/Asinhas:", ['Não', '6 Asinhas', '9 Asinhas', 'Dose de Batatas'], key='batata_asinha', on_change=atualizar_batata_asinhas)
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
        bebida_garrafa = st.selectbox("Bebida a Garrafa:", ['Nenhum', '2M Txoti', 'Savana', 'Pretinha', 'Lite', 'Heineken'], key='bebida_garrafa', on_change=atualizar_bebida_garrafa)
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
            restante = sheet_rs.cell(linha, 5).value  # Coluna E = Restante
            restante = int(restante) if restante else 0
            total_disponivel += restante
        if total_disponivel < quantidade:
            return False
        else:
            for linha in linhas_produto:
                restante = int(sheet_rs.cell(linha, 5).value or 0)
                if quantidade_total == 0:
                    break
                if restante > 0:
                    saida_atual = int(sheet_rs.cell(linha, 4).value or 0)  # Coluna D = Saída
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
                preco_bebidas = 40
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
            if st.session_state.bebida_lata == "2M Lata":
                preco_bebidas = 60
            if st.session_state.bebida_lata == "Impala Lata":
                preco_bebidas = 50
            if st.session_state.bebida_lata == "MY FAIR":
                preco_bebidas = 95
            if st.session_state.bebida_lata == "Txilar Lata":
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
    
    def atualizar_produto1():
        if st.session_state.produto1 != "Não":
            st.session_state.produto2 = "Não"
            st.session_state.produto3 = "Não"
            st.session_state.produto4 = "Não"
    def atualizar_produto2():
        if st.session_state.produto2 != "Não":
            st.session_state.produto1 = "Não"
            st.session_state.produto3 = "Não"
            st.session_state.produto4 = "Não"
    def atualizar_produto3():
        if st.session_state.produto3 != "Não":
            st.session_state.produto2 = "Não"
            st.session_state.produto1 = "Não"
            st.session_state.produto4 = "Não"
    def atualizar_produto4():
        if st.session_state.produto4 != "Não":
            st.session_state.produto2 = "Não"
            st.session_state.produto1 = "Não"
            st.session_state.produto3 = "Não"

    col9, col10, col11 = st.columns(3)
    with col9:
        produto1 = st.selectbox("Produto:", ['Não', 'Hambúrguer', 'Ovos', 'Queijo', 'Rachel'], key='produto1', on_change=atualizar_produto1)
    with col10:
        produto2 = st.selectbox("Bebida:", ['Não', '2M Txoti', '2M Lata', 'Savana', 'Pretinha', 'Lite', 'Heineken Txoti', 'Impala Lata', 'MY FAIR', 'Txilar Lata'], key='produto2', on_change=atualizar_produto2)
    with col11:
        produto3 = st.selectbox("Água/Sumo/Refrigerante:", ['Não', 'Água Pequena', 'Água Grande', 'Sumo Cappy', 'Sumo Compal', 'Refresco Garrafa', 'Refresco Txoti', 'Refresco 1L', 'Refresco 2L'], key='produto3', on_change=atualizar_produto3)
    if produto1 == "Hambúrguer":
        qnt_hamburguer = st.slider("Quantidade", 0, 150, 50, key="qnt_hamburguer")
    else:
        qnt_estoque = st.slider("Quantidade", 0, 20, 1, key="qnt_estoque")
    st.write("### Estoque Paralelo")
    produto4 = st.selectbox("Produto:", ["Não", "Batatas", "Palone", "Mayonnaise", "Tomato Sauce", "Óleo"], key='produto4', on_change=atualizar_produto4)
    qnt_estoque2 = st.slider("Quantidade", 0, 10, 1, key="qnt_estoque2")


    def estoque():
        global estoque_produto, quantidade_estoque

        estoque_produto = 'Sem Reposição'
        quantidade_estoque = 0
        if st.session_state.produto1 != "Não" and st.session_state.produto2 == 'Não' and st.session_state.produto3 == 'Não' and st.session_state.produto4 == 'Nao':
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
            sheet_estoque_atualizar()
        if st.session_state.produto1 == "Não" and st.session_state.produto2 != 'Não' and st.session_state.produto3 == 'Não'and st.session_state.produto4 == 'Nao':
            estoque_produto = st.session_state.produto2
            quantidade_estoque = st.session_state.qnt_estoque * 6
            sheet_estoque_atualizar_bebida()
        if st.session_state.produto1 == "Não" and st.session_state.produto2 == 'Não' and st.session_state.produto3 != 'Não'and st.session_state.produto4 == 'Nao':
            estoque_produto = st.session_state.produto3
            if st.session_state.produto3 == "Água Pequena" or st.session_state.produto3 == "Sumo Cappy" or st.session_state.produto3 == "Refresco Txoti":
                quantidade_estoque = st.session_state.qnt_estoque * 12
            elif st.session_state.produto3 == "Refresco 1L" or st.session_state.produto3 == "Refresco 2L" or st.session_state.produto3 == "Água Grande":
                quantidade_estoque = st.session_state.qnt_estoque * 6
            elif st.session_state.produto3 == "Refresco Garrafa":
                quantidade_estoque = st.session_state.qnt_estoque * 24
            elif st.session_state.produto3 == "Sumo Compal":
                quantidade_estoque = st.session_state.qnt_estoque * 10
            sheet_estoque_atualizar_bebida()
        if st.session_state.produto1 == "Não" and st.session_state.produto2 == 'Não' and st.session_state.produto3 == 'Não'and st.session_state.produto4 != 'Nao':
            estoque_produto = st.session_state.produto4
            quantidade_estoque = st.session_state.qnt_estoque2
            sheet_estoque_paralelo_atualizar()

        repor_valores()

    def sheet_estoque_atualizar():
        global count

        values = sheet_estoque.get_all_values()
        count = len(values) + 1

        estoque_adicionar = [[estoque_produto, date, quantidade_estoque, 0, f"=C{count}-D{count}"]]
        sheet_estoque.append_rows(estoque_adicionar, value_input_option="USER_ENTERED")
    def sheet_estoque_paralelo_atualizar():
        global count3

        values = sheet_estoque.get_all_values()
        count3 = len(values) + 1

        estoque_adicionar = [[estoque_produto, date, quantidade_estoque]]
        sheet_estoque_paralelo.append_rows(estoque_adicionar, value_input_option="USER_ENTERED")
    def sheet_estoque_atualizar_bebida():
        global count2

        values = sheet_estoque_bebida.get_all_values()
        count2 = len(values) + 1

        estoque_adicionar = [[estoque_produto, date, quantidade_estoque, 0, f"=C{count2}-D{count2}"]]
        sheet_estoque_bebida.append_rows(estoque_adicionar, value_input_option="USER_ENTERED")

    def repor_valores():
        st.session_state.produto1 = 'Não'
        st.session_state.produto2 = 'Não'
        st.session_state.produto3 = 'Não'
        st.session_state.qnt_estoque = 1

    st.button("Registrar Entrada", on_click=estoque)

if options == 'Relatório':
    st.title("📊 Dashboard e Relatórios")
    st.write("## Em Breve!")
    


















