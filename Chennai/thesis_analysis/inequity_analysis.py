import pandas as pd
import numpy as np
import os

def calculate_gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    array = array.flatten()
    if np.amin(array) < 0:
        array -= np.amin(array)
    array += 0.0000001
    array = np.sort(array)
    index = np.arange(1,array.shape[0]+1)
    n = array.shape[0]
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

def analyze_inequity(base_dir):
    """
    Computes surrogate measures for Gini coefficient of accessibility based on the 
    distribution of Transfer Friction across the network.
    """
    print("Evaluating Temporal Inequity...")
    out_dir = os.path.join(base_dir, 'output')
    tfi_file = os.path.join(out_dir, 'hub_friction_index.csv')
    
    df = pd.read_csv(tfi_file)
    
    # Inequity is often measured by how unequal the *burden* of travel is distributed.
    # Here, our burden is TFI_minutes. 
    # High Gini = highly unequal (some stations have 0 friction, others have 100+ mins).
    # Low Gini = perfectly equal distribution.
    
    tfi_values = df['TFI_minutes'].values
    gini_tfi = calculate_gini(tfi_values)
    
    print(f"\nMetric: Gini Coefficient of Transfer Friction")
    print(f"Value: {gini_tfi:.3f} (0=Perfect Equality, 1=Maximum Inequality)")
    if gini_tfi > 0.4:
         print("Assessment: High structural inequity in the multimodal network.")
    else:
         print("Assessment: Moderate to low structural inequity.")
         
    # Let's break it down by mode. Which mode's stations suffer the worst friction?
    # We find the dominant mode for each interchange from earlier processing.
    # Re-link with the intermodal transfers to get the dominant mode.
    transfers = pd.read_csv(os.path.join(out_dir, 'intermodal_transfers.csv'))
    # Mode of the 'from' station
    mode_map = transfers[['from_name', 'from_mode']].drop_duplicates('from_name')
    df_merged = df.merge(mode_map, left_on='from_name', right_on='from_name', how='left')
    
    mode_burden = df_merged.groupby('from_mode')['TFI_minutes'].agg(['mean', 'median', 'std', 'max']).round(2)
    print("\n--- Transfer Friction (Burden) by Origin Mode ---")
    print(mode_burden)
    
if __name__ == "__main__":
    analyze_dir = '/Users/bharatoraon/Downloads/Chennai/thesis_analysis'
    analyze_inequity(analyze_dir)
