from altair import Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import os


# Configurações para os gráficos
plt.rcParams['axes.formatter.use_locale'] = True
plt.rcParams['figure.figsize'] = (12, 8)
sns.set(style="whitegrid")
plt.style.use('ggplot')

# Visualização
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

print('🔍 PROJETO NOSEDIVE DIGITAL - ANÁLISE DE INFLUÊNCIA SOCIAL.')
print("Inspirado no episódio 'NoseDive' de Black Mirror")
print("=" * 30)

# Carrega os dados com API (colocar)
print("/n Carregando dados das interações sociais...")

# Simulando dados de posts da rede social
np.random.seed(42) # Para reproduzibilidade

# Criar dataframe com dados simulados de posts
n_posts = 1000
data = {
    'id': range(1, n_posts + 1),
    'timestamp': pd.date_range(start='2023-01-01', periods=n_posts, freq='H'),
    'likes': np.random.exponential(scale=50, size=n_posts).astype(int),
    'compartilhamentos': np.random.exponential(scale=10, size=n_posts).astype(int),
    'comentarios': np.random.exponential(scale=5, size=n_posts).astype(int),
    'sentimento_texto': np.random.choice(['positivo', 'neutro', 'negativo'], size=n_posts, p=[0.4, 0.4, 0.2]),
    'categoria': np.random.choice(['pessoal', 'profissional', 'entretenimento', 'notícia', 'opinião'], size=n_posts),
    'hora_do_dia': None,
    'dia_semana': None
}

# Criar DataFrame
df = pd.DataFrame(data)

# Adicionar Colunas
df['hora_do_dia'] = df['timestamp'].dt.hour
df['dia_semana'] = df['timestamp'].dt.day_name()
df['engajamento'] = df['likes'] + df['compartilhamentos'] + df['comentarios']
df['raio_likes_comentarios'] = df['likes'] / df['comentarios'].replace(0, 1)

# Adicionar colunas de pontuação scoial 
df['pontuacao_social'] = (
    df['likes'] * 0.5 +
    df['compartilhamentos'] * 2 +
    df['comentarios'] * 1.5
)

# Normalizando a pontuação para escala 0-5
max_score = df['pontuacao_social'].max()
df['pontuacao_nosedive'] = (df['pontuacao_social'] / max_score * 5).round(2)

# Coluna Classe Sócial
def classificar_pontuacao(score):
    if score >= 4.5:
        return 'Elite'
    elif score >= 4.0:
        return 'Privilegiado'
    elif score >= 3.0:
        return'Popular'
    elif score >= 2.0:
        return 'Visto'
    else:
        return 'Invisível'

df['classe_social'] = df['pontuacao_nosedive'].apply(classificar_pontuacao)

print(f'Total de posts analisados: {len(df)}')
print(f'/n Primeiras entradas do conjunto de dados:')
print(df[['likes', 'compartilhamentos', 'comentarios', 'sentimento_texto', 'pontuacao_nosedive', 'classe_social']].head())

# 1 - Distribuição de pontuação social
print("\n\n ANÁLISE 1: Distribuição de Pontuação Social")
print("=" * 70)
print("Analisando como as pontuações sociais estão distribuindo na população digital.")

plt.figure(figsize = (10,6))
sns.histplot(df['pontuacao_nosedive'], bins=20, kde=True)
plt.title('Distribuição de Pontuação Sociais (Escala 0-5)', fontsize = 16)
plt.xlabel('Pontuação Social', fontsize = 12)
plt.ylabel('Frequência', fontsize = 12)
plt.axvline(df['pontuacao_nosedive'].mean(), color='red', linestyle='--', label=f'Média: {df["pontuacao_nosedive"].mean():.2f}')
plt.legend()
plt.tight_layout()


# Estatísticas de Distribuição
print(f"\nEstatísticas de pontuação social: ")
print(f" - Média: {df['pontuacao_nosedive'].mean():.2f})")
print(f" - Mediana: {df['pontuacao_nosedive'].median():.2f}")
print(f" - Desvio padrão; {df['pontuacao_nosedive'].std():.2f}")
print(f" - Mínimo: {df['pontuacao_nosedive'].min():.2f}")
print(f" - Máximo: {df['pontuacao_nosedive'].max():.2f}") 

# Distribuição por classe social
class_counts = df['classe_social'].value_counts()
print(f"\nDistribuição por classe social:")
for classe, count in class_counts.items():
    print(f"- {classe}: {count} posts ({count/len(df)*100:.1f}%)")

# Análise 2: Relação entre sentimento e aprovação social
print("\n\nANÁLISE 2: Relação entre Sentimento e Aprovação Social")
print("=" * 70)
print("Analisando como o sentimento do do conteúdo se relaciona com a aprovação social.")

# Média de pontuação por sentimento
sentiment_scores = df.groupby('sentimento_texto')['pontuacao_nosedive'].mean().sort_values(ascending=False)
for sentimento, score in sentiment_scores.items():
    print(f" - {sentimento.capitalize()}: {score:.2f}")
    
plt.figure(figsize=(10, 6))
sns.boxplot(x='sentimento_texto', y='pontuacao_nosedive', data=df, order=['positivo', 'neutro', 'negativo'])
plt.title('Pontuação Social por Sentimento do Conteúdo', fontsize=16)
plt.xlabel('Sentimento', fontsize=12)
plt.ylabel('Pontuação Social', fontsize=12)
plt.tight_layout()


# Análise 3: Padrões temporais de engajamento
