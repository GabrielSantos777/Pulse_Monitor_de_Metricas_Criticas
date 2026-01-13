import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="SaaS Pulse Dashboard", layout="wide")
st.title("Saas Pulse: Inteligência de Negócio")
st.markdown("Monitoramento de Receita Recorrente (MRR) e Retenção de Clientes")

try:
    df = pd.read_csv('data/metricas_performance.csv')
    
    st.sidebar.header("Filtros")
    meses_selecionados = st.sidebar.multiselect(
        "Selecione os Meses:",
        options=df['Mes'].unique(),
        default=df["Mes"].unique()
    )
    
    df_filtrado = df[df["Mes"].isin(meses_selecionados)]
    
    # Principais KPIs
    mrr_total = df_filtrado['MRR'].sum()
    churn_total = df_filtrado['Cancelamentos'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("MRR Acumulado (Período)", f"R$ {mrr_total:,.2f}")
    col2.metric("Total de Cancelamentos", int(churn_total))
    col3.metric("Ticket Médio Estimado", f"R$ {df_filtrado['MRR'].mean():,.2f}")
    
    st.divider()
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("Tendência de MRR")
        fig_mrr = px.line(df_filtrado, x='Mes', y='MRR',
                          title='Crescimento da Receita Mensal',
                          markers=True, line_shape='spline')
        st.plotly_chart(fig_mrr, use_container_width=True)
        
    with col_graph2:
        st.subheader("Análise de Churn")
        fig_churn = px.bar(df_filtrado, x='Mes', y='Cancelamentos',
                           title='Cancelamentos por Mês',
                           color_discrete_sequence=['#EF553B'])
        st.plotly_chart(fig_churn, use_container_width=True)
        
    st.subheader("Dados Detalhados")
    st.dataframe(df_filtrado, use_container_width=True)
except FileNotFoundError:
    st.error("Arquivo não encontrado. Por favor, execute o script 'src/metrics.py' primeiro!") 