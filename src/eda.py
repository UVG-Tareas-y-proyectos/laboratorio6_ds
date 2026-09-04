import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

def calcular_resumen_descriptivo(df_v: pd.DataFrame, df_c: pd.DataFrame) -> dict:
    """Calcula conteos de videos, canales, comentarios, autores y visualizaciones."""
    n_videos = len(df_v)
    n_canales = df_v['channel_id'].nunique()
    n_comentarios = len(df_c)
    n_autores = df_c['author_channel_id'].nunique()
    
    videos_por_canal = df_v['channel_id'].value_counts()
    comentarios_por_video = df_c['video_id'].value_counts()
    
    resumen = {
        'total_videos': n_videos,
        'total_canales': n_canales,
        'total_comentarios': n_comentarios,
        'total_autores': n_autores,
        'promedio_videos_por_canal': videos_por_canal.mean(),
        'max_videos_por_canal': videos_por_canal.max(),
        'promedio_comentarios_por_video': comentarios_por_video.mean(),
        'max_comentarios_por_video': comentarios_por_video.max(),
        'total_visualizaciones': df_v['view_count'].sum(),
        'mediana_visualizaciones': df_v['view_count'].median()
    }
    return resumen

def analizar_concentracion(df_c: pd.DataFrame) -> dict:
    """Mide la concentración de comentarios en los videos y autores más activos."""
    comentarios_por_video = df_c['video_id'].value_counts()
    top1_video = comentarios_por_video.iloc[0] / len(df_c) * 100
    top3_videos = comentarios_por_video.iloc[:3].sum() / len(df_c) * 100
    top5_videos = comentarios_por_video.iloc[:5].sum() / len(df_c) * 100
    
    comentarios_por_autor = df_c['author_channel_id'].value_counts()
    top10_autores = comentarios_por_autor.iloc[:10].sum() / len(df_c) * 100
    
    return {
        'top1_video_pct': top1_video,
        'top3_videos_pct': top3_videos,
        'top5_videos_pct': top5_videos,
        'top10_autores_pct': top10_autores
    }

def generar_graficos_eda(df_v: pd.DataFrame, df_c: pd.DataFrame, output_dir: str):
    """Genera y guarda los gráficos exploratorios clave."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Concentración y Views vs Comentarios
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    counts_v = df_c['video_id'].value_counts().head(10)
    
    sns.barplot(x=counts_v.values, y=counts_v.index, ax=axes[0], color='steelblue')
    axes[0].set_title('Top 10 Videos por Cantidad de Comentarios')
    axes[0].set_xlabel('Comentarios')
    axes[0].set_ylabel('ID de Video')
    
    merged = df_v[['video_id', 'view_count']].copy()
    merged['comment_count'] = merged['video_id'].map(df_c['video_id'].value_counts()).fillna(0)
    
    sns.scatterplot(data=merged[merged['comment_count'] > 0], x='view_count', y='comment_count', ax=axes[1], color='darkred', s=60)
    axes[1].set_title('Visualizaciones vs. Comentarios (Escala Log)')
    axes[1].set_xscale('log')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('Visualizaciones (log)')
    axes[1].set_ylabel('Comentarios (log)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_participation.png'), dpi=300)
    plt.close()
    
    # 2. Wordcloud
    if 'texto_limpio' in df_c.columns:
        all_text = ' '.join(df_c['texto_limpio'].dropna())
        wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis', max_words=100).generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nube de Palabras Frecuentes en Comentarios')
        plt.savefig(os.path.join(output_dir, 'wordcloud_comments.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Bigramas
        words = all_text.split()
        bigrams = list(zip(words[:-1], words[1:]))
        bg_counts = Counter(bigrams).most_common(15)
        bg_df = pd.DataFrame(bg_counts, columns=['bigram', 'count'])
        bg_df['bigram_str'] = bg_df['bigram'].apply(lambda x: f'{x[0]} {x[1]}')
        
        plt.figure(figsize=(10, 5))
        sns.barplot(data=bg_df, x='count', y='bigram_str', color='teal')
        plt.title('Top 15 Bigramas Frecuentes en Comentarios')
        plt.xlabel('Frecuencia')
        plt.ylabel('Bigrama')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_bigrams.png'), dpi=300)
        plt.close()
