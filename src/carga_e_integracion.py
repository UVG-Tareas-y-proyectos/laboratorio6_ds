import pandas as pd

def cargar_datos(path_videos: str, path_comentarios: str):
    """Carga los conjuntos de datos de videos y comentarios."""
    df_v = pd.read_csv(path_videos)
    df_c = pd.read_csv(path_comentarios)
    return df_v, df_c

def verificar_llaves_y_unidades(df_v: pd.DataFrame, df_c: pd.DataFrame):
    """Identifica dimensiones, llaves primarias y porcentaje de asociación."""
    n_v = len(df_v)
    n_c = len(df_c)
    pk_v_unique = df_v['video_id'].nunique() == n_v
    pk_c_unique = df_c['comment_id'].nunique() == n_c
    
    v_ids = set(df_v['video_id'])
    matched_c = df_c[df_c['video_id'].isin(v_ids)]
    match_pct = (len(matched_c) / n_c) * 100.0 if n_c > 0 else 0
    
    return {
        'total_videos': n_v,
        'pk_video_unica': pk_v_unique,
        'total_comentarios': n_c,
        'pk_comentario_unica': pk_c_unique,
        'comentarios_asociados': len(matched_c),
        'porcentaje_asociados': match_pct
    }

def integrar_datos(df_v: pd.DataFrame, df_c: pd.DataFrame) -> pd.DataFrame:
    """Realiza un inner join entre comentarios y videos mediante video_id."""
    df_merged = pd.merge(df_c, df_v, on='video_id', how='inner', suffixes=('_comentario', '_video'))
    return df_merged
