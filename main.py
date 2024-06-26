#https://unstats.un.org/unsd/snaama/Basic#
import pandas as pd
import matplotlib.pyplot as plt

# Função para ler o arquivo e processar os dados
def processar_dados(arquivo):
    # Ler o arquivo XLSX
    df = pd.read_excel(arquivo)
    
    # Exibir as primeiras linhas e os nomes das colunas do DataFrame
    print(df.head())
    print(df.columns)
    
    # Filtrar as colunas relevantes
    colunas_interessantes = ['Country/Area', 'Year', 'Manufacturing (ISIC D)']
    df = df[colunas_interessantes]
    # Remover a linha onde Country/Area é "World"
    df = df[df['Country/Area'] != 'World']

    # Converter a coluna 'Manufacturing (ISIC D)' para numérica
    df['Manufacturing (ISIC D)'] = pd.to_numeric(df['Manufacturing (ISIC D)'], errors='coerce')

    # Remover linhas com valores nulos
    df = df.dropna()

    # Ordenar os países pelo valor de manufatura
    df = df.sort_values(by='Manufacturing (ISIC D)', ascending=False)

    # Selecionar os 10 países mais manufaturados
    top_10_paises = df.head(10)

    return top_10_paises

# Função para gerar o gráfico
# def gerar_grafico(dados):
#     plt.figure(figsize=(12, 8))
#     plt.barh(dados['Country/Area'], dados['Manufacturing (ISIC D)'], color='skyblue')
#     plt.xlabel('Valor de Manufatura (US$)')
#     plt.title('Top 10 Países Mais Manufaturados')
#     plt.gca().invert_yaxis()
#     plt.show()

def gerar_grafico(dados):
    plt.figure(figsize=(12, 8))
    colors = plt.cm.tab20.colors  # Seleciona uma paleta de cores com 20 cores
    plt.barh(dados['Country/Area'], dados['Manufacturing (ISIC D)'], color=colors[:len(dados)])
    plt.xlabel('Valor de Manufatura (US$)')
    plt.title('Top 10 Países Mais Manufaturados')
    plt.gca().invert_yaxis()
    plt.show()
# Atualize o caminho para o local onde você fez upload do arquivo
arquivo_xlsx = 'dados_industrializacao_paises.xlsx'

# Processar os dados
dados_processados = processar_dados(arquivo_xlsx)

# Gerar o gráfico
gerar_grafico(dados_processados)
