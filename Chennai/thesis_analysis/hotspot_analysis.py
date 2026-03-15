import pandas as pd
import geopandas as gpd
import os

def identify_friction_hotspots(base_dir):
    """
    Combines Transfer Friction Index (TFI) with geographic data to map spatial 
    temporal inequity gaps. Output maps logic to QGIS/visualizer.
    """
    print("Loading TFI results and geospatial stops...")
    out_dir = os.path.join(base_dir, 'output')
    
    tfi_file = os.path.join(out_dir, 'hub_friction_index.csv')
    stops_file = os.path.join(out_dir, 'unified_stops.geojson')
    
    tfi_df = pd.read_csv(tfi_file)
    stops_gdf = gpd.read_file(stops_file)
    
    # We aggregate geometry to the unique 'stop_name' to map the hubs
    hub_geoms = stops_gdf.dissolve(by='stop_name', aggfunc='first').reset_index()
    
    # Merge friction data onto geometry
    friction_hubs = hub_geoms.merge(tfi_df, left_on='stop_name', right_on='from_name', how='inner')
    
    # Drop outlier noise to focus on substantial interchanges 
    # (Require wait sec > 300 to exclude instant same-platform pseudo-transfers if any)
    friction_hubs = friction_hubs[friction_hubs['avg_wait_sec'] > 300]
    
    # Identify top 10% worst friction locations (Hotspots)
    threshold = friction_hubs['TFI_minutes'].quantile(0.90)
    
    print("\n--- Identifying High Transfer Friction Hotspots (Top 10%) ---")
    hotspots = friction_hubs[friction_hubs['TFI_minutes'] >= threshold]
    
    print(hotspots[['stop_name', 'TFI_minutes', 'mode', 'avg_wait_sec']].sort_values(by='TFI_minutes', ascending=False).head(15))
    
    # Export full dataset for mapping
    out_map = os.path.join(out_dir, 'spatial_friction_hotspots.geojson')
    # Keep only subset of columns for file size
    export_gdf = friction_hubs[['stop_name', 'mode', 'TFI_minutes', 'avg_walk_dist_m', 'avg_wait_sec', 'geometry']]
    export_gdf.to_file(out_map, driver='GeoJSON')
    print(f"\nSaved Spatial Friction map to {out_map}")
    
    # Basic zone-based temporal burden check
    # Without ward polygons, we can just bin lat/lon to proxy zones
    print("\n--- Basic Spatial Segregation Analysis (North vs South vs Central) ---")
    
    # Extract centroids first to ensure we have Points, since dissolve can create MultiPoints
    friction_hubs['centroid'] = friction_hubs.geometry.centroid
    lat_median = friction_hubs['centroid'].y.median()
    lon_median = friction_hubs['centroid'].x.median()
    
    def classify_zone(geom):
        if geom.y > lat_median + 0.05: return 'North (Peripheral)'
        elif geom.y < lat_median - 0.05: return 'South (Peripheral)'
        else: return 'Central Core'
        
    friction_hubs['zone'] = friction_hubs['centroid'].apply(classify_zone)
    zone_burden = friction_hubs.groupby('zone')['TFI_minutes'].mean().reset_index()
    print(zone_burden.sort_values(by='TFI_minutes', ascending=False))
    
if __name__ == "__main__":
    analyze_dir = '/Users/bharatoraon/Downloads/Chennai/thesis_analysis'
    identify_friction_hotspots(analyze_dir)
