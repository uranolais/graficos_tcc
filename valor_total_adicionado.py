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
    colunas_interessantes = ['Country/Area', 'Year', 'Total Value Added']
    df = df[colunas_interessantes]

    # Separar o valor mundial de Total Value Added
    valor_mundial = df.loc[df['Country/Area'] == 'World', 'Total Value Added'].values[0]

    # Remover a linha onde Country/Area é "World"
    df = df[df['Country/Area'] != 'World']

    # Converter a coluna 'Total Value Added' para numérica
    df['Total Value Added'] = pd.to_numeric(df['Total Value Added'], errors='coerce')

    # Remover linhas com valores nulos
    df = df.dropna()

    # Calcular a porcentagem de Total Value Added em relação ao valor mundial
    df['Percentage'] = (df['Total Value Added'] / valor_mundial) * 100

    # Ordenar os países pelo valor de Total Value Added
    df = df.sort_values(by='Total Value Added', ascending=False)

    # Selecionar os 10 países mais relevantes
    top_10_paises = df.head(10)

    return top_10_paises, valor_mundial

# Função para gerar o gráfico
def gerar_grafico(dados, valor_mundial):
    plt.figure(figsize=(12, 8))
    colors = plt.cm.tab20.colors  # Seleciona uma paleta de cores com 20 cores
    bars = plt.barh(dados['Country/Area'], dados['Total Value Added'], color=colors[:len(dados)])
    
    # Adicionar rótulos com porcentagem
    for bar, perc in zip(bars, dados['Percentage']):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{perc:.2f}%', va='center')

    plt.xlabel('Valor Adicionado Total (US$) e Porcentagem (%)')
    plt.title('Top 10 Países por Valor Adicionado Total')
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
