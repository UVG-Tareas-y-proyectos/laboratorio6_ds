import re
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

def obtener_stopwords_espanol():
    spanish_sw = set(stopwords.words('spanish'))
    custom_sw = {'si', 'asi', 'va', 'ver', 'hacer', 'tan', 'solo', 'mas', 'q', 'que', 'x', 'para', 'por', 'con', 'del', 'los', 'las', 'una', 'uno', 'unos', 'unas'}
    return spanish_sw.union(custom_sw)

def diagnostico_calidad(df_v: pd.DataFrame, df_c: pd.DataFrame) -> dict:
    """Calcula dimensiones, valores faltantes, duplicados y constantes."""
    diag = {
        'videos_shape': df_v.shape,
        'comentarios_shape': df_c.shape,
        'videos_nulos': df_v.isnull().sum().to_dict(),
        'comentarios_nulos': df_c.isnull().sum().to_dict(),
        'videos_duplicados': df_v.duplicated().sum(),
        'comentarios_duplicados': df_c.duplicated().sum(),
        'variables_constantes_comentarios': [col for col in df_c.columns if df_c[col].nunique() <= 1]
    }
    return diag

def limpiar_conteo_likes(val) -> int:
    """Convierte texto de likes a entero manejando espacios y vacíos."""
    if pd.isna(val):
        return 0
    s = str(val).strip()
    if not s or s == '':
        return 0
    s_digits = re.sub(r'[^\d]', '', s)
    return int(s_digits) if s_digits else 0

def limpiar_texto_comentario(txt: str, stop_words: set) -> str:
    """Aplica minúsculas, elimina URLs, hashtags/menciones, números y stopwords."""
    if not txt or pd.isna(txt):
        return ''
    t = str(txt).lower()
    t = re.sub(r'https?://\S+|www\.\S+', '', t)
    t = re.sub(r'[@#]\w+', '', t)
    t = re.sub(r'[^\w\s]', '', t)
    t = re.sub(r'\d+', '', t)
    words = [w for w in t.split() if w not in stop_words and len(w) > 2]
    return ' '.join(words)

def preprocesar_comentarios(df_c: pd.DataFrame) -> pd.DataFrame:
    """Genera las columnas like_count, texto_original y texto_limpio."""
    df_res = df_c.copy()
    df_res['like_count'] = df_res['like_count_text'].apply(limpiar_conteo_likes)
    df_res['texto_original'] = df_res['text'].astype(str)
    sw = obtener_stopwords_espanol()
    df_res['texto_limpio'] = df_res['texto_original'].apply(lambda x: limpiar_texto_comentario(x, sw))
    return df_res
