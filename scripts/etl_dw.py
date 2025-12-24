from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine
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


def popular_dim_tempo(anos=2):
    datas = []
    data_inicio = datetime(2023, 1, 1)
    for i in range(anos * 365):
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
    df_tempo = pd.DataFrame(datas)
    df_tempo.to_sql('dim_tempo', engine, if_exists='append', index=False)
    
def popular_dim_planos():
    planos = [
        {'nome_plano': 'Basic', 'valor_mensal': 99.00, 'limite_usuarios': 5},
        {'nome_plano': 'Pro', 'valor_mensal': 299.00, 'limite_usuarios': 20},
        {'nome_plano': 'Enterprise', 'valor_mensal': 999.00, 'limite_usuarios': 100}
    ]
    pd.DataFrame(planos).to_sql('dim_planos', engine, if_exists='append', index=False)

def popular_dim_clientes(n=500):
    clientes = []
    segmentos = ['Tecnologia', 'Educação', 'Saúde', 'Varejo', 'Finanças']
    for _ in range(n):
        clientes.append({
            'id_natural_cliente': fake.uuid4(),
            'nome_cliente': fake.name(),
            'email_cliente': fake.email(),
            'empresa_cliente': fake.company(),
            'segmento_empresa': random.choice(segmentos),
            'pais': 'Brasil'
        })
    pd.DataFrame(clientes).to_sql('dim_clientes', engine, if_exists='append', index=False)

def popular_fato_assinaturas(n_vendas=2000):

    sk_clientes = pd.read_sql('SELECT "sk_cliente" FROM dim_clientes', engine)['sk_cliente'].tolist()
    sk_planos =pd.read_sql("SELECT sk_plano, valor_mensal FROM dim_planos", engine).to_dict('records')
    sk_datas = pd.read_sql("SELECT sk_tempo FROM dim_tempo", engine)['sk_tempo'].tolist()
    
    assinaturas = []
    for _ in range(n_vendas):
        plano_sorteado = random.choice(sk_planos)
        assinaturas.append({
            'fk_cliente': random.choice(sk_clientes),
            'fk_planos': plano_sorteado['sk_plano'],
            'fk_data_inicio': random.choice(sk_datas),
            'valor_contrato': plano_sorteado['valor_mensal'] * random.randint(1, 12),
            'status_assinatura': random.choice(['Ativa', 'Ativa', 'Ativa', 'Cancelada'])
        })
    pd.DataFrame(assinaturas).to_sql('fato_assinaturas', engine, if_exists='append', index=False)
    
if __name__ == "__main__":
    popular_dim_tempo()
    popular_dim_planos()
    popular_dim_clientes()
    popular_fato_assinaturas()
    print("\n Data Warehouse populado com sucesso!")
  