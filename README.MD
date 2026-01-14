# 📊 SaaS Pulse: Inteligência de Negócio para Plataformas SaaS

O **SaaS Pulse** é um projeto de Business Intelligence de ponta a ponta, focado no monitoramento das métricas vitais de empresas de Software as a Service (SaaS). O objetivo é transformar logs de eventos brutos em insights estratégicos sobre receita e retenção.

---

## 🎯 Resultados e Funcionalidades

| Funcionalidade | Descrição | Status |
| :--- | :--- | :--- |
| **Simulação de Realidade** | Geração de dados sintéticos realistas de clientes (assinaturas e cancelamentos) usando `Faker`. | ✅ Completo |
| **Cálculo de MRR** | Motor de métricas que processa a Receita Recorrente Mensal acumulada. | ✅ Completo |
| **Análise de Churn** | Monitoramento da taxa de cancelamento e perda de clientes mês a mês. | ✅ Completo |
| **Dashboard Interativo** | Interface visual moderna construída com `Streamlit` e `Plotly`. | ✅ Completo |

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.x
* **Manipulação de Dados:** Pandas, Numpy
* **Visualização:** Plotly Express, Streamlit
* **Geração de Dados:** Faker (Simulação estatística de comportamento de clientes)

---

## 🧠 Conceitos de Negócio Aplicados

Este projeto não foca apenas em código, mas na aplicação de KPIs reais do mercado de tecnologia:

1.  **MRR (Monthly Recurring Revenue):** Cálculo da receita previsível gerada pelas assinaturas ativas.
2.  **Churn Rate:** Identificação do momento em que o cliente deixa a plataforma, permitindo análise de retenção.
3.  **Ticket Médio:** Valor médio gerado por cada cliente no período selecionado.

---

## 📂 Estrutura do Projeto

* `src/generator.py`: Simula 5 anos de histórico de eventos de clientes.
* `src/metrics.py`: Transforma os eventos em um sumário de performance mensal.
* `src/dashboard.py`: Aplicação web interativa para visualização dos KPIs.

---

## 🚀 Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/saas-pulse.git](https://github.com/seu-usuario/saas-pulse.git)
    ```
2.  **Instale as dependências:**
    ```bash
    pip install pandas plotly streamlit faker
    ```
3.  **Execute o fluxo de dados:**
    ```bash
    python src/generator.py   # Gera os dados brutos
    python src/metrics.py     # Processa as métricas
    ```
4.  **Inicie o Dashboard:**
    ```bash
    streamlit run src/dashboard.py
    ```

---
## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para criar problemas (issues) ou enviar solicitações de pull (pull requests) para melhorias ou correções.

## :memo: Licença

Esse projeto está sob a licença MIT.

---

*Este projeto foi desenvolvido por [Gabriel Santos/GabrielSantos777].*