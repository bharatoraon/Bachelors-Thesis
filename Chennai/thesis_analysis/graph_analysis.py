import pandas as pd
import networkx as nx
import os
import json

def build_multimodal_graph(base_dir):
    """
    Builds a directed geographic network graph representing physical stops as nodes
    and connectivity as edges (transit links and walking transfers).
    Note: For a full time-expanded graph, we would need to map every departure/arrival event,
    which scales to millions of nodes. For initial spatial connectivity analysis, 
    we build a static topological graph first.
    """
    print("Loading data for network construction...")
    stops_file = os.path.join(base_dir, 'output', 'unified_stops.geojson')
    transfers_file = os.path.join(base_dir, 'output', 'intermodal_transfers.csv')
    stop_times_file = os.path.join(base_dir, 'output', 'unified_stop_times.csv')
    
    import geopandas as gpd
    stops_gdf = gpd.read_file(stops_file)
    transfers_df = pd.read_csv(transfers_file)
    
    # We only need sequence relationships to build transit edges
    st_df = pd.read_csv(stop_times_file, usecols=['trip_id', 'stop_id', 'stop_sequence'])
    st_df = st_df.sort_values(by=['trip_id', 'stop_sequence'])
    
    G = nx.DiGraph()
    
    # 1. Add Nodes
    for _, row in stops_gdf.iterrows():
        G.add_node(row['stop_id'], 
                   name=row['stop_name'], 
                   mode=row['mode'], 
                   pos=(row.geometry.x, row.geometry.y))
                   
    print(f"Added {G.number_of_nodes()} stops as nodes.")
    
    # 2. Add Transit Edges (from stop_times sequence)
    st_df['next_stop'] = st_df.groupby('trip_id')['stop_id'].shift(-1)
    # Count frequency of each link as weight proxy
    transit_edges = st_df.dropna(subset=['next_stop']).groupby(['stop_id', 'next_stop']).size().reset_index(name='frequency')
    
    for _, row in transit_edges.iterrows():
        # High frequency = lower travel impedance natively
        G.add_edge(row['stop_id'], row['next_stop'], 
                   weight=1.0,  # base weight
                   type='transit',
                   frequency=row['frequency'])
                   
    print(f"Added {len(transit_edges)} unique transit links.")
    
    # 3. Add Transfer Edges
    for _, row in transfers_df.iterrows():
        # walk time sec adds friction
        # we divide by a constant to normalize roughly against transit weight if needed
        # For betweenness, distance/walk time is the impedance
        weight = row['walk_time_sec'] / 60.0  # minutes
        G.add_edge(row['from_stop_id'], row['to_stop_id'],
                   weight=weight,
                   type='transfer',
                   distance_m=row['distance_m'])
                   
    print(f"Added {len(transfers_df)} transfer walking links.")
    print(f"Graph finalized with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    
    return G

def analyze_centrality(G, output_path):
    print("Calculating Betweenness Centrality (this may take a minute)...")
    # For large graphs, betweenness is expensive. We use a sample of nodes (k=100) to approximate
    # or just run it fully if it's small enough. 8k nodes is border-line, we'll try full first.
    # We use 'weight' to represent cost (impedance).
    centrality = nx.betweenness_centrality(G, weight='weight', k=500, seed=42)
    
    # Add centrality to nodes and export
    nodes_data = []
    for node_id, data in G.nodes(data=True):
        nodes_data.append({
            'stop_id': node_id,
            'name': data.get('name'),
            'mode': data.get('mode'),
            'lat': data.get('pos', (0,0))[1],
            'lon': data.get('pos', (0,0))[0],
            'betweenness': centrality.get(node_id, 0)
        })
        
    df = pd.DataFrame(nodes_data)
    df = df.sort_values(by='betweenness', ascending=False)
    
    print("\nTop 10 Most Critical Transit Nodes (Highest Betweenness):")
    print(df.head(10)[['name', 'mode', 'betweenness']])
    
    df.to_csv(output_path, index=False)
    print(f"Saved centrality results to {output_path}")

if __name__ == "__main__":
    base_dir = '/Users/bharatoraon/Downloads/Chennai/thesis_analysis'
    G = build_multimodal_graph(base_dir)
    out_cent = os.path.join(base_dir, 'output', 'node_centrality.csv')
    analyze_centrality(G, out_cent)
