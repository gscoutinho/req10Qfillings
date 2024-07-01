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

3. O programa irá exibir os KPIs calculados para cada ação e mostrar gráficos desses indicadores. Os dados processados serão salvos como arquivos CSV no diretório atual.

## Visão Geral do Código

- `main()`: A função principal que inicializa o processo para cada ação na lista `stocks_watch`. Recupera e processa dados, calcula indicadores financeiros, plota os resultados e salva os dados em arquivos CSV.
  
- `get_data_from_sec(ticker)`: Busca dados da API da SEC para um determinado ticker de ação.

- `treat_data_from_10q(fillings_us_gaap)`: Processa os dados brutos da SEC e calcula os principais indicadores financeiros. Retorna um dicionário com os dados processados e os KPIs calculados.

## Indicadores Financeiros Calculados

- `current_ratio`: Ativos correntes divididos por passivos correntes.
- `quick_ratio`: (Ativos correntes - Estoque) divididos por passivos correntes.
- `GrossMargin`: (Receita - Custo dos Bens Vendidos) dividido por receita.
- `OperatingMargin`: Rendimento operacional dividido por receita.
- `roa`: Lucro líquido dividido por ativos correntes.
- `roe`: Lucro líquido dividido pelo patrimônio líquido.

## Contato

Para quaisquer perguntas ou sugestões, por favor entre em contato: eng.gabrielcoutinho@outlook.com.br

