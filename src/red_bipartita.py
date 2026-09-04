import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def construir_red_bipartita(df_c: pd.DataFrame, df_v: pd.DataFrame):
    """Construye un grafo no dirigido bipartita autor-video."""
    B = nx.Graph()
    author_nodes = df_c['author_channel_id'].unique()
    video_nodes = df_c['video_id'].unique()
    
    B.add_nodes_from(author_nodes, bipartite=0, node_type='author')
    B.add_nodes_from(video_nodes, bipartite=1, node_type='video')
    
    edge_weights = df_c.groupby(['author_channel_id', 'video_id']).size().reset_index(name='weight')
    for _, row in edge_weights.iterrows():
        B.add_edge(row['author_channel_id'], row['video_id'], weight=row['weight'])
        
    return B, edge_weights

def exportar_tablas_nodos_aristas(B: nx.Graph, df_c: pd.DataFrame, df_v: pd.DataFrame, output_dir: str):
    """Genera y guarda tabla_nodos_bipartita.csv y tabla_aristas_bipartita.csv."""
    os.makedirs(output_dir, exist_ok=True)
    
    node_rows = []
    v_dict = df_v.set_index('video_id')['title'].to_dict()
    
    for n, d in B.nodes(data=True):
        ntype = d['node_type']
        deg = B.degree(n)
        if ntype == 'author':
            sub = df_c[df_c['author_channel_id'] == n]
            label = sub['author_name'].iloc[0] if len(sub) > 0 else n
            handle = sub['author_handle'].iloc[0] if len(sub) > 0 else n
            total_comm = len(sub)
        else:
            label = v_dict.get(n, n)
            handle = n
            total_comm = len(df_c[df_c['video_id'] == n])
            
        node_rows.append({
            'node_id': n,
            'node_type': ntype,
            'label': label,
            'handle': handle,
            'degree': deg,
            'total_comments': total_comm
        })
        
    nodes_df = pd.DataFrame(node_rows)
    nodes_path = os.path.join(output_dir, 'tabla_nodos_bipartita.csv')
    nodes_df.to_csv(nodes_path, index=False)
    
    edge_weights = df_c.groupby(['author_channel_id', 'video_id']).size().reset_index(name='weight')
    edges_df = edge_weights.rename(columns={'author_channel_id': 'source', 'video_id': 'target'})
    edges_path = os.path.join(output_dir, 'tabla_aristas_bipartita.csv')
    edges_df.to_csv(edges_path, index=False)
    
    return nodes_df, edges_df

def visualizar_red_bipartita(B: nx.Graph, df_v: pd.DataFrame, output_path: str):
    """Dibuja y guarda la visualización de la red bipartita autor-video."""
    author_nodes = [n for n, d in B.nodes(data=True) if d['node_type'] == 'author']
    video_nodes = [n for n, d in B.nodes(data=True) if d['node_type'] == 'video']
    
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(B, k=0.15, seed=42)
    
    nx.draw_networkx_nodes(B, pos, nodelist=author_nodes, node_color='skyblue', node_size=35, alpha=0.7, label='Autores')
    nx.draw_networkx_nodes(B, pos, nodelist=video_nodes, node_color='crimson', node_size=140, alpha=0.9, label='Videos')
    nx.draw_networkx_edges(B, pos, alpha=0.3, edge_color='gray')
    
    # Etiquetar videos con grado mayor o igual a 10
    v_dict = df_v.set_index('video_id')['title'].to_dict()
    top_v = [v for v in video_nodes if B.degree(v) >= 10]
    labels = {v: v_dict.get(v, v)[:22] + '...' for v in top_v}
    nx.draw_networkx_labels(B, pos, labels=labels, font_size=8, font_weight='bold')
    
    plt.title('Red Bipartita Autor - Video (YouTube)')
    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
