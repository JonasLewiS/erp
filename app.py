import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def grafico_fornecedores():
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    df = pd.read_sql_query("SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor", conn)
    conn.close()

    fig, ax = plt.subplots()
    ax.bar(df['fornecedor'], df['total'])
    ax.set_title("Distribuição das Contas a Pagar por Fornecedor")
    ax.set_xlabel("Fornecedor")
    ax.set_ylabel("Valor Devido")
    plt.xticks(rotation=90)
    
    st.pyplot(fig)

def top_5_clientes():
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    query = """
    SELECT clientes.nome, SUM(contas_receber.valor) as total_receita
    FROM contas_receber
    JOIN clientes ON contas_receber.cliente_id = clientes.id
    GROUP BY clientes.id
    ORDER BY total_receita DESC
    LIMIT 5
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df['nome'], df['total_receita'])
    ax.set_title("Top 5 Clientes com Maior Receita")
    ax.set_xlabel("Cliente")
    ax.set_ylabel("Valor Total")
    plt.xticks(rotation=45)
    
    st.pyplot(fig)

def comparacao_receita_despesa():
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    query_receita = "SELECT SUM(valor) as total_receita FROM lancamentos WHERE tipo = 'Receita' AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')"
    query_despesa = "SELECT SUM(valor) as total_despesa FROM lancamentos WHERE tipo = 'Despesa' AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')"
    
    receita = pd.read_sql_query(query_receita, conn)['total_receita'][0]
    despesa = pd.read_sql_query(query_despesa, conn)['total_despesa'][0]
    conn.close()

    categorias = ['Receita', 'Despesa']
    valores = [receita if receita else 0, despesa if despesa else 0]

    fig, ax = plt.subplots()
    ax.bar(categorias, valores, color=['green', 'red'])
    ax.set_title("Comparação Receita vs Despesa")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Valor Total")
    
    st.pyplot(fig)

def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        grafico_fornecedores()  # Chamando a função para gráfico de fornecedores
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)
        comparacao_receita_despesa()  # Chamando a função para comparação Receita vs Despesa
        top_5_clientes()  # Chamando a função para o Top 5 Clientes com Maior Receita
    
    conn.close()

if __name__ == "__main__":
    main()
