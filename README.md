# SEC Query Data Program

Este programa recupera e processa dados financeiros dos formulários 10-Q da SEC para ações especificadas. Ele calcula e visualiza principais indicadores financeiros.

## Funcionalidades

- Recupera dados da API da SEC para ações especificadas.
- Processa dados financeiros dos formulários 10-Q.
- Calcula principais indicadores financeiros.
- Plota os indicadores financeiros para análise visual.
- Salva os dados processados em arquivos CSV.

## Requisitos

- Python 3.x
- Biblioteca Requests
- Biblioteca Pandas
- Biblioteca Matplotlib

## Instalação

1. Clone o repositório:
    ```bash
    git clone <repository_url>
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd <project_directory>
    ```

3. Instale as bibliotecas necessárias:
    ```bash
    pip install requests pandas matplotlib
    ```

## Uso

1. Edite a lista `stocks_watch` na função `main` para incluir os tickers das ações que você deseja analisar:
    ```python
    stocks_watch = ['XOM', 'CVX', 'COP', 'EOG', 'SLB']
    ```

2. Execute o programa:
    ```bash
    python sec_query_data.py
    ```


3. Aguarde enquanto o programa consulta dados da SEC e calcula os indicadores.

## Indicadores Calculados

O programa calcula os seguintes indicadores financeiros:

- Current Ratio
- Quick Ratio
- Gross Margin
- Operating Margin
- Return on Assets (ROA)
- Return on Equity (ROE)
- Debt-to-Equity Ratio
- Interest Coverage Ratio
- Assets Turnover Ratio
- Receivable Turnover Ratio
- Cash-to-Net Income Ratio
- Earnings Per Share (EPS)
- Price-to-Earnings Ratio (P/E)

## Saída

Os dados são apresentados em DataFrames do pandas e gráficos gerados usando matplotlib.

---

Este programa foi desenvolvido por [Seu Nome] como parte de um projeto de análise financeira. Para mais detalhes ou suporte, entre em contato em [seu email].

