import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import os
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.patches as mpatches
import networkx as nx
import random
from collections import Counter

# Configurações para os gráficos
plt.rcParams['axes.formatter.use_locale'] = True
plt.rcParams['figure.figsize'] = (12, 8)
sns.set(style="whitegrid")
plt.style.use('ggplot')

# Tentar configurar o locale
try:
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        print("Aviso: Não foi possível configurar o locale para pt_BR. Usando locale padrão.")

print('🔍 PROJETO SOCIALDVIE DIGITAL - ANÁLISE DE IMPACTO SOCIAL DAS REDES SOCIAIS')
print("Inspirado no episódio 'SocialDive' de Black Mirror")
print("=" * 70)

# Dados dos artigos fornecidos
print("\n📚 ANÁLISE DE ARTIGOS SOBRE IMPACTO SOCIAL DAS REDES SOCIAIS")
print("=" * 70)

artigos = [
    {
        'titulo': 'O efeito da rede social em nosso cotidiano',
        'fonte': 'Brasil Escola',
        'url': 'https://meuartigo.brasilescola.uol.com.br/sociologia/o-efeito-rede-social-nosso-cotidiano.htm',
        'conceitos_chave': [
            'Relacionamentos horizontais',
            'Diminuição de hierarquias',
            'Redução de preconceitos',
            'Controle de uso',
            'Dependência digital'
        ],
        'citacoes': [
            'As redes sociais permitem relacionamentos mais horizontais, diminuindo hierarquias.',
            'O uso descontrolado pode levar a perdas significativas na qualidade de vida.',
            'As redes sociais podem tanto aproximar quanto afastar pessoas.'
        ],
        'impactos_positivos': [
            'Facilidade de comunicação',
            'Democratização da informação',
            'Diminuição de hierarquias sociais'
        ],
        'impactos_negativos': [
            'Dependência digital',
            'Isolamento social físico',
            'Ansiedade e depressão'
        ]
    },
    {
        'titulo': 'Echo Chambers on Social Media: A comparative analysis',
        'fonte': 'arXiv',
        'url': 'https://arxiv.org/abs/2004.09603',
        'conceitos_chave': [
            'Câmaras de eco',
            'Bolhas informacionais',
            'Polarização',
            'Viés de confirmação',
            'Algoritmos de recomendação'
        ],
        'citacoes': [
            'Usuários tendem a formar câmaras de eco que reforçam suas crenças pré-existentes.',
            'A exposição limitada a perspectivas diversas reduz a compreensão de diferentes pontos de vista.',
            'Algoritmos de recomendação frequentemente amplificam o efeito de bolha informacional.'
        ],
        'impactos_positivos': [
            'Fortalecimento de comunidades de interesse',
            'Maior engajamento com conteúdo relevante'
        ],
        'impactos_negativos': [
            'Polarização social e política',
            'Desinformação e fake news',
            'Radicalização de opiniões',
            'Fragmentação social'
        ]
    },
    {
        'titulo': 'Sociedade em rede',
        'fonte': 'Wikipedia',
        'url': 'https://pt.wikipedia.org/wiki/Sociedade_em_rede',
        'conceitos_chave': [
            'Ciberespaço',
            'Comunicação mediada',
            'Interações digitais',
            'Reorganização social',
            'Capital informacional'
        ],
        'citacoes': [
            'A sociedade em rede reorganiza as estruturas sociais tradicionais através da mediação tecnológica.',
            'O ciberespaço se torna um novo território para interações humanas significativas.',
            'A comunicação mediada por tecnologia cria novas formas de capital social e cultural.'
        ],
        'impactos_positivos': [
            'Novas formas de organização social',
            'Democratização do conhecimento',
            'Superação de barreiras geográficas'
        ],
        'impactos_negativos': [
            'Exclusão digital',
            'Vigilância e controle',
            'Perda de privacidade'
        ]
    },
    {
        'titulo': 'Da Rede para a Sociedade',
        'fonte': 'Eumed',
        'url': 'https://www.eumed.net/rev/cccss/2017/01/redes.html',
        'conceitos_chave': [
            'Influência política',
            'Transformação de relações',
            'Mobilização social',
            'Ativismo digital',
            'Novas sociabilidades'
        ],
        'citacoes': [
            'As redes sociais transformaram fundamentalmente como nos organizamos politicamente.',
            'O ativismo digital criou novas formas de mobilização social não possíveis anteriormente.',
            'As relações interpessoais são cada vez mais mediadas e transformadas por plataformas digitais.'
        ],
        'impactos_positivos': [
            'Mobilização social facilitada',
            'Novas formas de participação política',
            'Ampliação de vozes marginalizadas'
        ],
        'impactos_negativos': [
            'Superficialidade nas relações',
            'Manipulação política',
            'Vigilância e controle social'
        ]
    }
]

# Exibir informações sobre os artigos
print("\nArtigos analisados:")
for i, artigo in enumerate(artigos, 1):
    print(f"{i}. {artigo['titulo']} ({artigo['fonte']})")

# Extrair todos os conceitos-chave
todos_conceitos = []
for artigo in artigos:
    todos_conceitos.extend(artigo['conceitos_chave'])

# Contar frequência dos conceitos
conceito_counts = Counter(todos_conceitos)

print("\n\nANÁLISE 1: CONCEITOS-CHAVE NO IMPACTO SOCIAL DAS REDES SOCIAIS")
print("=" * 70)
print("Principais conceitos identificados na literatura:")

for conceito, count in conceito_counts.most_common(10):
    print(f" - {conceito}: mencionado em {count} artigos")

# Extrair impactos positivos e negativos
todos_impactos_positivos = []
todos_impactos_negativos = []

for artigo in artigos:
    todos_impactos_positivos.extend(artigo['impactos_positivos'])
    todos_impactos_negativos.extend(artigo['impactos_negativos'])

# Contar frequência dos impactos
impactos_positivos_counts = Counter(todos_impactos_positivos)
impactos_negativos_counts = Counter(todos_impactos_negativos)

print("\n\nANÁLISE 2: IMPACTOS POSITIVOS E NEGATIVOS DAS REDES SOCIAIS")
print("=" * 70)

print("\nImpactos Positivos mais citados:")
for impacto, count in impactos_positivos_counts.most_common(5):
    print(f" - {impacto}: mencionado {count} vezes")

print("\nImpactos Negativos mais citados:")
for impacto, count in impactos_negativos_counts.most_common(5):
    print(f" - {impacto}: mencionado {count} vezes")

# Visualizar comparação entre impactos positivos e negativos
impactos_positivos_df = pd.DataFrame(impactos_positivos_counts.most_common(5), 
                                    columns=['Impacto', 'Frequência'])
impactos_positivos_df['Tipo'] = 'Positivo'

impactos_negativos_df = pd.DataFrame(impactos_negativos_counts.most_common(5), 
                                    columns=['Impacto', 'Frequência'])
impactos_negativos_df['Tipo'] = 'Negativo'

impactos_df = pd.concat([impactos_positivos_df, impactos_negativos_df])

plt.figure(figsize=(12, 8))
colors = {'Positivo': 'green', 'Negativo': 'red'}
ax = sns.barplot(x='Frequência', y='Impacto', hue='Tipo', data=impactos_df, palette=colors)
plt.title('Impactos Positivos vs. Negativos das Redes Sociais', fontsize=16)
plt.xlabel('Frequência nas Fontes Analisadas', fontsize=12)
plt.ylabel('Tipo de Impacto', fontsize=12)
plt.tight_layout()
plt.savefig('impactos_redes_sociais.png')
plt.close()

print("\nGráfico de impactos positivos vs. negativos gerado com sucesso!")

# SIMULAÇÃO DE CENÁRIO SOCIALDIVE
print("\n\n🔮 SIMULAÇÃO DE CENÁRIO FUTURO: SOCIEDADE BASEADA EM PONTUAÇÃO SOCIAL")
print("=" * 70)
print("Inspirado no episódio 'Nosedive' de Black Mirror e nos artigos analisados")

# Parâmetros da simulação
n_pessoas = 1000
n_interacoes = 5000
n_dias = 365

# Criar população inicial com características diversas
np.random.seed(42)  # Para reprodutibilidade

# Características das pessoas
populacao = pd.DataFrame({
    'id': range(1, n_pessoas + 1),
    'pontuacao_inicial': np.random.normal(3.5, 0.8, n_pessoas).clip(1, 5),  # Pontuação entre 1-5
    'classe_socioeconomica': np.random.choice(['Baixa', 'Média', 'Alta'], size=n_pessoas, p=[0.3, 0.5, 0.2]),
    'nivel_educacional': np.random.choice(['Fundamental', 'Médio', 'Superior', 'Pós-graduação'], 
                                         size=n_pessoas, p=[0.2, 0.4, 0.3, 0.1]),
    'idade': np.random.randint(18, 80, n_pessoas),
    'conformidade_social': np.random.normal(0.7, 0.2, n_pessoas).clip(0, 1),  # Tendência a seguir normas sociais
    'autenticidade': np.random.normal(0.5, 0.2, n_pessoas).clip(0, 1),  # Tendência a ser autêntico vs. fake
    'acesso_tecnologia': np.random.normal(0.8, 0.15, n_pessoas).clip(0.3, 1)  # Nível de acesso à tecnologia
})

# Definir pontuação inicial baseada em fatores socioeconômicos (simulando desigualdade digital)
# Classe socioeconômica influencia a pontuação inicial
class_bonus = {'Baixa': -0.5, 'Média': 0, 'Alta': 0.5}
populacao['pontuacao_inicial'] += populacao['classe_socioeconomica'].map(class_bonus)

# Nível educacional influencia a pontuação inicial
edu_bonus = {'Fundamental': -0.3, 'Médio': -0.1, 'Superior': 0.2, 'Pós-graduação': 0.4}
populacao['pontuacao_inicial'] += populacao['nivel_educacional'].map(edu_bonus)

# Acesso à tecnologia influencia a pontuação inicial
populacao['pontuacao_inicial'] += (populacao['acesso_tecnologia'] - 0.5) * 0.5

# Garantir que a pontuação esteja entre 1 e 5
populacao['pontuacao_inicial'] = populacao['pontuacao_inicial'].clip(1, 5)
populacao['pontuacao_atual'] = populacao['pontuacao_inicial'].copy()

# Simular evolução da pontuação ao longo do tempo
print("\nSimulando evolução da pontuação social ao longo de 1 ano...")

# Criar matriz para armazenar pontuações ao longo do tempo
pontuacoes_tempo = np.zeros((n_pessoas, n_dias))
pontuacoes_tempo[:, 0] = populacao['pontuacao_atual'].values

# Parâmetros que influenciam a evolução da pontuação
# Baseados nos conceitos dos artigos
parametros = {
    'peso_conformidade': 0.3,  # Quanto a conformidade social influencia a pontuação
    'peso_autenticidade': -0.1,  # Autenticidade pode reduzir pontuação (sistema valoriza conformidade)
    'peso_classe': 0.2,  # Influência da classe socioeconômica
    'peso_educacao': 0.15,  # Influência do nível educacional
    'peso_acesso_tecnologia': 0.25,  # Influência do acesso à tecnologia
    'volatilidade': 0.1,  # Quanto a pontuação pode variar aleatoriamente
    'momentum': 0.8,  # Quanto a tendência atual influencia a futura (efeito Mateus)
    'polarizacao': 0.05  # Tendência de pontuações extremas se distanciarem mais
}

# Simular evolução diária
for dia in range(1, n_dias):
    # Fator aleatório (eventos diários, interações)
    fator_aleatorio = np.random.normal(0, parametros['volatilidade'], n_pessoas)
    
    # Fator de conformidade (pessoas conformes tendem a ganhar pontos)
    fator_conformidade = populacao['conformidade_social'] * parametros['peso_conformidade']
    
    # Fator de autenticidade (pode reduzir pontos em um sistema que valoriza conformidade)
    fator_autenticidade = populacao['autenticidade'] * parametros['peso_autenticidade']
    
    # Fator socioeconômico (classe social influencia oportunidades de pontuação)
    fator_classe = pd.get_dummies(populacao['classe_socioeconomica'])
    fator_classe = fator_classe['Alta'] * 0.1 - fator_classe['Baixa'] * 0.1
    fator_classe *= parametros['peso_classe']
    
    # Fator educacional
    fator_educacao = pd.get_dummies(populacao['nivel_educacional'])
    fator_educacao = (fator_educacao['Superior'] * 0.05 + 
                      fator_educacao['Pós-graduação'] * 0.1 - 
                      fator_educacao['Fundamental'] * 0.05)
    fator_educacao *= parametros['peso_educacao']
    
    # Fator de acesso à tecnologia
    fator_tecnologia = (populacao['acesso_tecnologia'] - 0.5) * parametros['peso_acesso_tecnologia']
    
    # Efeito Mateus (rico fica mais rico, pobre fica mais pobre)
    pontuacao_atual = pontuacoes_tempo[:, dia-1]
    fator_momentum = (pontuacao_atual - 3) * 0.01 * parametros['momentum']
    
    # Efeito de polarização (pontuações extremas tendem a se distanciar mais)
    fator_polarizacao = np.abs(pontuacao_atual - 3) * np.sign(pontuacao_atual - 3) * parametros['polarizacao']
    
    # Calcular nova pontuação
    nova_pontuacao = (pontuacao_atual + 
                     fator_aleatorio + 
                     fator_conformidade + 
                     fator_autenticidade + 
                     fator_classe + 
                     fator_educacao + 
                     fator_tecnologia + 
                     fator_momentum +
                     fator_polarizacao)
    
    # Garantir que a pontuação esteja entre 1 e 5
    nova_pontuacao = np.clip(nova_pontuacao, 1, 5)
    
    # Armazenar pontuação
    pontuacoes_tempo[:, dia] = nova_pontuacao

# Atualizar pontuação final
populacao['pontuacao_final'] = pontuacoes_tempo[:, -1]
populacao['variacao_pontuacao'] = populacao['pontuacao_final'] - populacao['pontuacao_inicial']

# Classificar em estratos sociais baseados na pontuação final
def classificar_estrato(pontuacao):
    if pontuacao >= 4.5:
        return 'Elite Digital'
    elif pontuacao >= 4.0:
        return 'Privilegiado'
    elif pontuacao >= 3.0:
        return 'Cidadão Padrão'
    elif pontuacao >= 2.0:
        return 'Marginalizado'
    else:
        return 'Excluído Digital'

populacao['estrato_social'] = populacao['pontuacao_final'].apply(classificar_estrato)

# Análise dos resultados da simulação
print("\n\nANÁLISE 3: ESTRATIFICAÇÃO SOCIAL NO CENÁRIO SOCIALDIVE")
print("=" * 70)

# Distribuição dos estratos sociais
estrato_counts = populacao['estrato_social'].value_counts()
print("\nDistribuição da população por estrato social:")
for estrato, count in estrato_counts.items():
    print(f" - {estrato}: {count} pessoas ({count/n_pessoas*100:.1f}%)")

# Visualizar distribuição de pontuação final
plt.figure(figsize=(10, 6))
sns.histplot(populacao['pontuacao_final'], bins=20, kde=True)
plt.title('Distribuição de Pontuação Social Final', fontsize=16)
plt.xlabel('Pontuação (1-5)', fontsize=12)
plt.ylabel('Número de Pessoas', fontsize=12)

# Adicionar linhas verticais para os limites dos estratos
plt.axvline(x=4.5, color='red', linestyle='--', alpha=0.7, label='Elite Digital (4.5+)')
plt.axvline(x=4.0, color='orange', linestyle='--', alpha=0.7, label='Privilegiado (4.0-4.5)')
plt.axvline(x=3.0, color='green', linestyle='--', alpha=0.7, label='Cidadão Padrão (3.0-4.0)')
plt.axvline(x=2.0, color='blue', linestyle='--', alpha=0.7, label='Marginalizado (2.0-3.0)')
plt.legend()
plt.tight_layout()
plt.savefig('distribuicao_pontuacao_final.png')
plt.close()

# Analisar relação entre classe socioeconômica inicial e estrato social final
cross_tab = pd.crosstab(populacao['classe_socioeconomica'], 
                        populacao['estrato_social'], 
                        normalize='index') * 100

print("\nRelação entre classe socioeconômica inicial e estrato social final (%):")
print(cross_tab.round(1))

# Visualizar a relação entre classe socioeconômica e estrato social
plt.figure(figsize=(12, 8))
cross_tab.plot(kind='bar', stacked=True, colormap='viridis')
plt.title('Estrato Social Digital por Classe Socioeconômica', fontsize=16)
plt.xlabel('Classe Socioeconômica', fontsize=12)
plt.ylabel('Percentual (%)', fontsize=12)
plt.legend(title='Estrato Social Digital')
plt.tight_layout()
plt.savefig('classe_vs_estrato.png')
plt.close()

# Analisar evolução da pontuação média por classe socioeconômica
pontuacoes_por_classe = {}
classes = populacao['classe_socioeconomica'].unique()

for classe in classes:
    indices = populacao[populacao['classe_socioeconomica'] == classe].index
    pontuacoes_por_classe[classe] = pontuacoes_tempo[indices].mean(axis=0)

# Visualizar evolução temporal da pontuação por classe
plt.figure(figsize=(12, 6))
for classe, pontuacoes in pontuacoes_por_classe.items():
    plt.plot(range(n_dias), pontuacoes, label=f'Classe {classe}')

plt.title('Evolução da Pontuação Social Média por Classe Socioeconômica', fontsize=16)
plt.xlabel('Dias', fontsize=12)
plt.ylabel('Pontuação Média (1-5)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('evolucao_pontuacao_por_classe.png')
plt.close()

print("\nGráficos de estratificação social gerados com sucesso!")

# Análise de mobilidade social
print("\n\nANÁLISE 4: MOBILIDADE SOCIAL NO CENÁRIO SOCIALDIVE")
print("=" * 70)

# Definir mobilidade como a variação na pontuação
populacao['mobilidade'] = populacao['variacao_pontuacao']

# Estatísticas de mobilidade por classe
mobilidade_por_classe = populacao.groupby('classe_socioeconomica')['mobilidade'].agg(['mean', 'std', 'min', 'max'])
print("\nMobilidade social por classe socioeconômica:")
print(mobilidade_por_classe.round(2))

# Visualizar mobilidade por classe
plt.figure(figsize=(10, 6))
sns.boxplot(x='classe_socioeconomica', y='mobilidade', data=populacao, palette='viridis')
plt.title('Mobilidade Social por Classe Socioeconômica', fontsize=16)
plt.xlabel('Classe Socioeconômica', fontsize=12)
plt.ylabel('Variação na Pontuação Social', fontsize=12)
plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('mobilidade_por_classe.png')
plt.close()

# Análise de fatores que influenciam a mobilidade
print("\n\nANÁLISE 5: FATORES QUE INFLUENCIAM A MOBILIDADE SOCIAL")
print("=" * 70)

# Calcular correlações entre características e mobilidade
correlacoes = populacao[['idade', 'conformidade_social', 'autenticidade', 
                         'acesso_tecnologia', 'pontuacao_inicial', 'mobilidade']].corr()['mobilidade'].sort_values()

print("\nCorrelação entre características e mobilidade social:")
for caracteristica, corr in correlacoes.items():
    if caracteristica != 'mobilidade':
        print(f" - {caracteristica}: {corr:.3f}")

# Visualizar correlações
plt.figure(figsize=(10, 6))
correlacoes = correlacoes.drop('mobilidade')
sns.barplot(x=correlacoes.values, y=correlacoes.index, palette='RdBu_r')
plt.title('Fatores que Influenciam a Mobilidade Social', fontsize=16)
plt.xlabel('Correlação com Mobilidade Social', fontsize=12)
plt.axvline(x=0, color='black', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('fatores_mobilidade.png')
plt.close()

# Simulação de rede social
print("\n\nANÁLISE 6: SIMULAÇÃO DE REDE SOCIAL E FORMAÇÃO DE BOLHAS")
print("=" * 70)
print("Simulando formação de conexões e bolhas sociais baseadas em pontuação...")

# Criar grafo de rede social
G = nx.Graph()

# Adicionar nós (pessoas)
for idx, row in populacao.iterrows():
    G.add_node(row['id'], 
               pontuacao=row['pontuacao_final'], 
               estrato=row['estrato_social'],
               classe=row['classe_socioeconomica'])

# Função para determinar probabilidade de conexão baseada em pontuações
def prob_conexao(p1, p2, homofilia=0.7):
    # Diferença de pontuação
    diff = abs(p1 - p2)
    # Probabilidade base (quanto menor a diferença, maior a probabilidade)
    prob_base = max(0, 1 - (diff / 4) * homofilia)
    return prob_base

# Adicionar arestas (conexões)
# Pessoas tendem a se conectar com outras de pontuação similar (homofilia)
n_conexoes = min(20000, n_pessoas * 20)  # Limitar número de conexões para visualização
conexoes_realizadas = 0

while conexoes_realizadas < n_conexoes:
    # Selecionar duas pessoas aleatórias
    p1 = np.random.randint(1, n_pessoas + 1)
    p2 = np.random.randint(1, n_pessoas + 1)
    
    if p1 != p2 and not G.has_edge(p1, p2):
        # Obter pontuações
        p1_score = populacao.loc[populacao['id'] == p1, 'pontuacao_final'].values[0]
        p2_score = populacao.loc[populacao['id'] == p2, 'pontuacao_final'].values[0]
        
        # Calcular probabilidade de conexão
        prob = prob_conexao(p1_score, p2_score)
        
        # Decidir se conecta
        if np.random.random() < prob:
            G.add_edge(p1, p2)
            conexoes_realizadas += 1

print(f"\nRede social simulada com {G.number_of_nodes()} pessoas e {G.number_of_edges()} conexões.")

# Detectar comunidades na rede
try:
    from community import best_partition
    partition = best_partition(G)
    nx.set_node_attributes(G, partition, 'community')
    
    # Contar número de comunidades
    n_communities = len(set(partition.values()))
    print(f"Detectadas {n_communities} comunidades distintas na rede social.")
    
    # Analisar homogeneidade das comunidades
    community_scores = {}
    for community in set(partition.values()):
        nodes_in_community = [node for node in G.nodes() if partition[node] == community]
        scores = [G.nodes[node]['pontuacao'] for node in nodes_in_community]
        community_scores[community] = {
            'size': len(nodes_in_community),
            'mean_score': np.mean(scores),
            'std_score': np.std(scores)
        }
    
    # Ordenar comunidades por tamanho
    sorted_communities = sorted(community_scores.items(), key=lambda x: x[1]['size'], reverse=True)
    
    print("\nAnálise das 5 maiores comunidades:")
    for i, (comm, stats) in enumerate(sorted_communities[:5], 1):
        print(f"Comunidade {i}: {stats['size']} membros, pontuação média: {stats['mean_score']:.2f} ± {stats['std_score']:.2f}")
    
except ImportError:
    print("Biblioteca 'community' não disponível. Análise de comunidades não realizada.")
    # Alternativa: usar algoritmo de clustering
    # Extrair matriz de adjacência
    adj_matrix = nx.to_numpy_array(G)
    # Aplicar K-means
    kmeans = KMeans(n_clusters=5, random_state=42)
    # Usar as primeiras 2 componentes principais para clustering
    clusters = kmeans.fit_predict(adj_matrix[:, :2])
    # Atribuir clusters aos nós
    for i, node in enumerate(G.nodes()):
        G.nodes[node]['community'] = int(clusters[i])
    
    print("Análise alternativa: agrupamento de nós em 5 clusters.")

# CONCLUSÕES E IMPLICAÇÕES SOCIAIS
print("\n\n📝 CONCLUSÕES E IMPLICAÇÕES SOCIAIS")
print("=" * 70)

# Conclusões baseadas nos artigos e na simulação
conclusoes = [
    "A estratificação social digital tende a reproduzir e amplificar desigualdades socioeconômicas existentes.",
    "O acesso à tecnologia e o nível educacional são fatores determinantes para a mobilidade social em um sistema de pontuação.",
    "Pessoas com maior conformidade social tendem a se beneficiar mais em sistemas de pontuação, enquanto a autenticidade pode ser penalizada.",
    "A formação de bolhas sociais (câmaras de eco) é um fenômeno natural em redes baseadas em pontuação, reforçando a polarização.",
    "O 'Efeito Mateus' digital (rico fica mais rico, pobre fica mais pobre) é observado na evolução das pontuações ao longo do tempo.",
    "A mobilidade social ascendente é mais difícil para classes socioeconômicas mais baixas, criando um ciclo de exclusão digital."
]

for i, conclusao in enumerate(conclusoes, 1):
    print(f"{i}. {conclusao}")

# Implicações éticas e sociais
print("\nImplicações éticas e sociais de um sistema de pontuação social:")
implicacoes = [
    "Erosão da privacidade: sistemas de pontuação social requerem vigilância constante das ações individuais.",
    "Conformismo excessivo: pessoas podem sacrificar autenticidade e pensamento crítico para maximizar pontuação.",
    "Discriminação algorítmica: vieses nos algoritmos podem perpetuar e amplificar desigualdades existentes.",
    "Exclusão digital: pessoas sem acesso adequado à tecnologia ficam cada vez mais marginalizadas.",
    "Saúde mental: ansiedade, depressão e outros problemas podem surgir da pressão constante por aprovação social.",
    "Manipulação comportamental: o sistema pode ser usado como ferramenta de controle social e político."
]

for i, implicacao in enumerate(implicacoes, 1):
    print(f"{i}. {implicacao}")

# Recomendações para mitigar impactos negativos
print("\nRecomendações para mitigar impactos negativos:")
recomendacoes = [
    "Políticas de inclusão digital para garantir acesso equitativo à tecnologia.",
    "Transparência algorítmica para permitir auditoria e correção de vieses.",
    "Educação digital crítica para promover uso consciente das redes sociais.",
    "Regulamentação para proteger privacidade e prevenir discriminação.",
    "Valorização da diversidade de pensamento e expressão autêntica nas plataformas digitais.",
    "Desenvolvimento de métricas de valor social que vão além de likes e compartilhamentos."
]

for i, recomendacao in enumerate(recomendacoes, 1):
    print(f"{i}. {recomendacao}")

print("\n✅ Análise concluída! Todos os gráficos foram gerados.")