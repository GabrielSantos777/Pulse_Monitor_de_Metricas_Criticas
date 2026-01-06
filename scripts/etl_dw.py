from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta
import os

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URI)
fake = Faker('pt-br')


def popular_dim_tempo():
    print("Gerando Dimensão Tempo...")
    datas = []
    data_inicio = datetime(2023, 1, 1)
    for i in range(730): # 2 anos
        dt = data_inicio + timedelta(days=i)
        datas.append({
            'data_completa': dt,
            'ano': dt.year,
            'mes': dt.month,
            'nome_mes': dt.strftime('%B'),
            'trimestre': (dt.month - 1) // 3 + 1,
            'dia_semana': dt.strftime('%A'),
            'final_semana': dt.weekday() >= 5
        })
    df = pd.DataFrame(datas)
    df.to_sql('dim_tempo', engine, if_exists='append', index=False)
    
def popular_dim_planos():
    print("Gerando Dimensão Planos...")
    planos = [
        {'nome_plano': 'Basic', 'valor_mensal': 99.00, 'limite_usuarios': 5},
        {'nome_plano': 'Pro', 'valor_mensal': 299.00, 'limite_usuarios': 20},
        {'nome_plano': 'Enterprise', 'valor_mensal': 999.00, 'limite_usuarios': 100}
    ]
    pd.DataFrame(planos).to_sql('dim_planos', engine, if_exists='append', index=False)

def popular_dim_clientes(n=100):
    print(f"Gerando {n} Clientes...")
    clientes = []
    for _ in range(n):
        clientes.append({
            'id_natural_cliente': fake.uuid4(),
            'nome_cliente': fake.name(),
            'email_cliente': fake.email(),
            'empresa_cliente': fake.company(),
            'segmento_empresa': random.choice(['Tech', 'Saúde', 'Varejo']),
            'pais': 'Brasil'
        })
    df = pd.DataFrame(clientes)
    df.to_sql('dim_clientes', engine, if_exists='append', index=False, method='multi')

def popular_fato_assinaturas(n_vendas=500):
    print(f"Gerando {n_vendas} Assinaturas...")
    
    with engine.connect() as conn:
        check_cols = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'dim_clientes'"))
        colunas_reais = [row[0] for row in check_cols]
        print(f"DEBUG: Colunas encontradas no banco para 'dim_clientes': {colunas_reais}")
        
        if 'sk_cliente' not in colunas_reais:
            print("ERRO CRÍTICO: A coluna sk_cliente realmente não existe no banco de dados!")
            return

        sk_clientes = [row[0] for row in conn.execute(text("SELECT sk_cliente FROM dim_clientes")).fetchall()]
        sk_planos = [dict(row._mapping) for row in conn.execute(text("SELECT sk_plano, valor_mensal FROM dim_planos")).fetchall()]
        sk_datas = [row[0] for row in conn.execute(text("SELECT sk_tempo FROM dim_tempo")).fetchall()]
    
if __name__ == "__main__":
    try:
        popular_dim_tempo()
        popular_dim_planos()
        popular_dim_clientes()
        popular_fato_assinaturas()
        print("\nSucesso total!")
    except Exception as e:
        print(f"\nErro durante a execução: {e}")
  