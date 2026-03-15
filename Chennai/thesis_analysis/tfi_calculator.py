import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def time_to_seconds(time_str):
    """Converts HH:MM:SS to seconds from midnight, handling >24h GTFS times."""
    if pd.isna(time_str): return None
    try:
        h, m, s = map(int, str(time_str).split(':'))
        return h * 3600 + m * 60 + s
    except:
        return None

def calculate_transfer_friction(base_dir):
    """
    Computes Transfer Friction parameters (Waiting Time, Walk Time, Missed Connection Probability).
    """
    print("Loading datasets for TFI computation...")
    out_dir = os.path.join(base_dir, 'output')
    
    st_file = os.path.join(out_dir, 'unified_stop_times.csv')
    tr_file = os.path.join(out_dir, 'intermodal_transfers.csv')
    
    st_df = pd.read_csv(st_file, usecols=['trip_id', 'stop_id', 'arrival_time', 'departure_time'])
    transfers = pd.read_csv(tr_file)
    
    print("Parsing schedule timestamps...")
    # Convert string times to seconds to allow arithmetic
    st_df['arrival_sec'] = st_df['arrival_time'].apply(time_to_seconds)
    st_df['departure_sec'] = st_df['departure_time'].apply(time_to_seconds)
    st_df = st_df.dropna(subset=['arrival_sec', 'departure_sec'])
    
    # To calculate friction, we need to map arrivals at a 'From' node 
    # and find the next valid 'Departure' at a 'To' node within a reasonable time window
    # Because computing cross-joins for millions of rows is intractable linearly,
    # we aggregate average headways (Wait Times) at each node as a proxy for the static TFI.
    
    print("Calculating proxy headways per stop...")
    # Sort chronological departures to find headways at each stop
    departures = st_df[['stop_id', 'departure_sec']].sort_values(by=['stop_id', 'departure_sec'])
    departures['headway_sec'] = departures.groupby('stop_id')['departure_sec'].diff()
    
    # Filter headways: >0 and < 3 hours (10800s) to exclude overnight gaps
    valid_headways = departures[(departures['headway_sec'] > 0) & (departures['headway_sec'] < 10800)]
    avg_node_headways = valid_headways.groupby('stop_id')['headway_sec'].mean().reset_index()
    avg_node_headways.rename(columns={'headway_sec': 'avg_wait_sec'}, inplace=True)
    
    print("Integrating Wait Times and Walk Times into Transfers...")
    # Merge receiving node's average wait time onto the transfer edges
    tfi_edges = transfers.merge(avg_node_headways, left_on='to_stop_id', right_on='stop_id', how='left')
    tfi_edges['avg_wait_sec'] = tfi_edges['avg_wait_sec'].fillna(900) # Default 15 min wait if missing
    
    # Since we lack real-time delay feeds, we use a probabilistic formulation for Missed Connection.
    # High frequency = low missed probability penalty. Low frequency = high penalty.
    # Buffer time proxy = 20% of headway
    tfi_edges['reliability_buffer_sec'] = tfi_edges['avg_wait_sec'] * 0.20
    
    # Transfer Friction Index (TFI) Formula:
    # TFI = Walk_Time + Wait_Time + (Missed_Probability * Wait_Time)
    # Using a simple heuristic where Missed Probability scales with Walk distance and low frequency
    tfi_edges['missed_prob'] = np.clip( (tfi_edges['walk_time_sec'] / 600) * (tfi_edges['avg_wait_sec'] / 1800), 0.05, 0.4)
    
    tfi_edges['TFI_minutes'] = (tfi_edges['walk_time_sec'] + tfi_edges['avg_wait_sec'] + 
                                (tfi_edges['missed_prob'] * tfi_edges['avg_wait_sec'])) / 60.0
                                
    # Aggregate TFI back up to the interchange station level to find Friction Hotspots
    hub_friction = tfi_edges.groupby('from_name').agg({
        'TFI_minutes': 'mean',
        'walk_time_sec': 'mean',
        'avg_wait_sec': 'mean',
        'distance_m': 'mean'
    }).rename(columns={'distance_m': 'avg_walk_dist_m'})
    
    hub_friction = hub_friction.sort_values(by='TFI_minutes', ascending=False)
    
    print("\nTop 10 Interchanges with Highest Transfer Friction (Worst Performance):")
    print(hub_friction.head(10)[['TFI_minutes', 'avg_walk_dist_m', 'avg_wait_sec']].round(2))
    
    hub_tfi_file = os.path.join(out_dir, 'hub_friction_index.csv')
    hub_friction.to_csv(hub_tfi_file)
    print(f"\nSaved Transfer Friction metrics to {hub_tfi_file}")

if __name__ == "__main__":
    analyze_dir = '/Users/bharatoraon/Downloads/Chennai/thesis_analysis'
    calculate_transfer_friction(analyze_dir)
