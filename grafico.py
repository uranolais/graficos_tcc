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

    # Separar o valor de manufatura mundial
    valor_mundial = df.loc[df['Country/Area'] == 'World', 'Manufacturing (ISIC D)'].values[0]

    # Remover a linha onde Country/Area é "World"
    df = df[df['Country/Area'] != 'World']

    # Converter a coluna 'Manufacturing (ISIC D)' para numérica
    df['Manufacturing (ISIC D)'] = pd.to_numeric(df['Manufacturing (ISIC D)'], errors='coerce')

    # Remover linhas com valores nulos
    df = df.dropna()

    # Calcular a porcentagem de manufatura em relação ao valor mundial
    df['Percentage'] = (df['Manufacturing (ISIC D)'] / valor_mundial) * 100

    # Ordenar os países pelo valor de manufatura
    df = df.sort_values(by='Manufacturing (ISIC D)', ascending=False)

    # Selecionar os 10 países mais manufaturados
    top_10_paises = df.head(10)

    return top_10_paises, valor_mundial

# Função para gerar o gráfico
def gerar_grafico(dados, valor_mundial):
    plt.figure(figsize=(12, 8))
    colors = plt.cm.tab20.colors  # Seleciona uma paleta de cores com 20 cores
    bars = plt.barh(dados['Country/Area'], dados['Manufacturing (ISIC D)'], color=colors[:len(dados)])
    
    # Adicionar rótulos com porcentagem
    for bar, perc in zip(bars, dados['Percentage']):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{perc:.2f}%', va='center')

    plt.xlabel('Valor de Manufatura (US$) e Porcentagem (%)')
    plt.title('Top 10 Países Mais Manufaturados')
    plt.gca().invert_yaxis()
    
    # Adicionar eixo secundário para porcentagem
    ax2 = plt.gca().twiny()
    ax2.set_xlim(plt.gca().get_xlim())
    ax2.set_xticks(plt.gca().get_xticks())
    ax2.set_xticklabels([f'{(tick/valor_mundial)*100:.2f}%' for tick in plt.gca().get_xticks()])
    ax2.set_xlabel('Porcentagem do Valor Mundial (%)')
    
    plt.show()

# Atualize o caminho para o local onde você fez upload do arquivo
arquivo_xlsx = 'dados_industrializacao_paises.xlsx'

# Processar os dados
dados_processados, valor_mundial = processar_dados(arquivo_xlsx)

# Gerar o gráfico
gerar_grafico(dados_processados, valor_mundial)
