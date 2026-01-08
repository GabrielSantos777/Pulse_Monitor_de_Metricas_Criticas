import pandas as pd

def processar_metricas():
    
    df = pd.read_csv('data/clientes_eventos.csv')
    
    df['data_evento'] = pd.to_datetime(df['data_evento'])
    df['mes_referencia'] = df['data_evento'].dt.to_period('M')
    
    #Calculando o MRR Mensal (Soma dos pagamentos)
    mrr_mensal = df[df['tipo_evento'] == 'Pagamento'].groupby('mes_referencia')['valor'].sum().reset_index()
    mrr_mensal.columns = ['Mes', 'MRR']

    novos_clientes = df[df['tipo_evento'] == 'Pagamento'].groupby('cliente_id')['mes_referencia'].min().value_counts().reset_index()
    novos_clientes.columns = ['Mes', 'Novos_Clientes']
    
    #Calculando churn
    churn_mensal = df[df['tipo_evento'] == 'Cancelamento'].groupby('mes_referencia')['cliente_id'].count().reset_index()
    churn_mensal.columns = ['Mes', 'Cancelamentos']
    
    # Unificando as métricas em uma única tabela (Tabela de Performance)
    performance = pd.merge(mrr_mensal, churn_mensal, on='Mes', how='left').fillna(0)
    performance['Mes'] = performance['Mes'].astype(str)
    performance.to_csv('data/metricas_performance.csv', index=False)
    
    print("Sumário de métricas gerado em 'data/metricas_performance.csv'!")
    print("\n--- RESUMO DOS ÚLTIMOS 3 MESES ---")
    print(performance.tail(3))
    
if __name__ == "__main__":
    processar_metricas()