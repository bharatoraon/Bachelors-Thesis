import pandas as pd
import geopandas as gpd
from scipy.spatial import cKDTree
import numpy as np
import os
import networkx as nx

def build_interchanges(stops_gdf: gpd.GeoDataFrame, max_distance_meters: float = 500) -> pd.DataFrame:
    """
    Identifies spatial interchanges between different transit modes based on proximity.
    Returns a dataframe of edges representing walkable transfers between stops.
    """
    print(f"Identifying interchanges within {max_distance_meters} meters...")
    
    # We must project the data to a local CRS to calculate distances in meters accurately.
    # EPSG:32644 is UTM Zone 44N, which covers Chennai.
    projected_stops = stops_gdf.to_crs(epsg=32644)
    
    # Extract coordinates
    coords = np.array(list(zip(projected_stops.geometry.x, projected_stops.geometry.y)))
    
    # Build KDTree for fast spatial queries
    tree = cKDTree(coords)
    
    # Find all pairs within max_distance_meters
    pairs = tree.query_pairs(r=max_distance_meters)
    
    interchanges = []
    modes = projected_stops['mode'].values
    stop_ids = projected_stops['stop_id'].values
    names = projected_stops['stop_name'].values
    
    for i, j in pairs:
        mode_i = modes[i]
        mode_j = modes[j]
        
        # We only care about transfers between DIFFERENT networks (or modes) or long multimodal connections.
        # But for network robustness, we can keep intra-mode transfers if they represent distinct stations.
        # To avoid massive bloat, let's strictly focus on INTER-mode transfers for our friction index,
        # or transfers between distinctly named stations.
        if mode_i != mode_j:
            dist = np.linalg.norm(coords[i] - coords[j])
            
            interchanges.append({
                'from_stop_id': stop_ids[i],
                'to_stop_id': stop_ids[j],
                'from_mode': mode_i,
                'to_mode': mode_j,
                'from_name': names[i],
                'to_name': names[j],
                'distance_m': dist,
                # Assume a walking speed of 1.2 meters per second
                'walk_time_sec': dist / 1.2
            })
            # Add reverse direction
            interchanges.append({
                'from_stop_id': stop_ids[j],
                'to_stop_id': stop_ids[i],
                'from_mode': mode_j,
                'to_mode': mode_i,
                'from_name': names[j],
                'to_name': names[i],
                'distance_m': dist,
                'walk_time_sec': dist / 1.2
            })
            
    interchange_df = pd.DataFrame(interchanges)
    print(f"Found {len(interchange_df)//2} unique undirected inter-modal transfer links.")
    return interchange_df

if __name__ == "__main__":
    base_dir = '/Users/bharatoraon/Downloads/Chennai/thesis_analysis/output'
    stops_file = os.path.join(base_dir, 'unified_stops.geojson')
    
    print("Loading unified stops...")
    stops_gdf = gpd.read_file(stops_file)
    
    transfer_edges = build_interchanges(stops_gdf, max_distance_meters=500)
    
    # Save the transfer edges
    out_file = os.path.join(base_dir, 'intermodal_transfers.csv')
    transfer_edges.to_csv(out_file, index=False)
    print(f"Saved {out_file}")
    
    # Let's peek at some of the biggest hubs
    if not transfer_edges.empty:
        hub_counts = transfer_edges.groupby('from_name').size().sort_values(ascending=False).head(10)
        print("\nTop 10 Transit Hubs by Number of Transfer Links:")
        print(hub_counts)
