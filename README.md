# Laboratorio 6 - Análisis de redes sociales (YouTube)

Avance: Carga e integración de datos, diagnóstico de calidad y preprocesamiento de texto, análisis exploratorio (EDA) y construcción de la red bipartita autor-video.

## Correr

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/jupyter notebook notebooks/laboratorio6.ipynb
```

## Estructura del repositorio

- `notebooks/laboratorio6.ipynb` - Cuaderno Jupyter con la resolución de las actividades 1 a 4 del avance.
- `src/` - Scripts de Python modulares para reproducir el flujo de datos.
  - `carga_e_integracion.py` - Carga y verificación de la llave foránea `video_id`.
  - `limpieza_y_preprocesamiento.py` - Diagnóstico de calidad, limpieza de conteos y texto (`texto_limpio` vs `texto_original`).
  - `eda.py` - Métricas exploratorias, concentración de participación, bigramas y preguntas del inciso 3.5 y 3.6.
  - `red_bipartita.py` - Construcción del grafo autor-video y exportación de tablas de nodos y aristas.
- `data/raw/` - Archivos CSV originales (`youtube_videos.csv` y `youtube_comments.csv`).
- `data/processed/` - Datasets procesados (`dataset_integrado.csv`, `dataset_limpio_comentarios.csv`, `tabla_nodos_bipartita.csv`, `tabla_aristas_bipartita.csv`).
- `reports/` - Figuras generadas (`reports/figures/`) e informe narrativo del avance (`reports/respuestas_avance.md`).
