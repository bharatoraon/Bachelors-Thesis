import pandas as pd
import geopandas as gpd
import os

class GTFSProcessor:
    def __init__(self, base_dir: str):
        self.paths = {
            'bus': os.path.join(base_dir, 'bus_gtfs'),
            'metro': os.path.join(base_dir, 'metro_gtfs'),
            'suburban': os.path.join(base_dir, 'suburban_gtfs')
        }
    
    def load_and_standardize_stops(self) -> gpd.GeoDataFrame:
        """
        Loads stops.txt from all modes, standardizes column names, prefixes stop_ids with mode name 
        to prevent collision, and returns a unified GeoDataFrame.
        """
        all_stops = []
        
        for mode, path in self.paths.items():
            stops_file = os.path.join(path, 'stops.txt')
            if not os.path.exists(stops_file):
                print(f"Warning: {stops_file} not found.")
                continue
                
            df = pd.read_csv(stops_file, low_memory=False)
            
            # Keep essential columns
            cols_to_keep = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
            if 'parent_station' in df.columns:
                cols_to_keep.append('parent_station')
                
            df = df[[c for c in cols_to_keep if c in df.columns]].copy()
            
            # Prefix IDs to avoid collision
            df['original_stop_id'] = df['stop_id']
            df['stop_id'] = f"{mode}_" + df['stop_id'].astype(str)
            
            if 'parent_station' in df.columns:
                df['parent_station'] = df['parent_station'].apply(
                    lambda x: f"{mode}_{x}" if pd.notnull(x) and str(x).strip() else None
                )
            
            df['mode'] = mode
            all_stops.append(df)
            
        unified_stops = pd.concat(all_stops, ignore_index=True)
        
        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame(
            unified_stops, 
            geometry=gpd.points_from_xy(unified_stops.stop_lon, unified_stops.stop_lat),
            crs="EPSG:4326"
        )
        return gdf

    def load_and_standardize_schedules(self):
        all_routes = []
        all_trips = []
        all_stop_times = []
        
        print("Standardizing schedules...")
        for mode, path in self.paths.items():
            routes_file = os.path.join(path, 'routes.txt')
            trips_file = os.path.join(path, 'trips.txt')
            stop_times_file = os.path.join(path, 'stop_times.txt')
            
            if not all(os.path.exists(f) for f in [routes_file, trips_file, stop_times_file]):
                print(f"Warning: Missing schedule files for {mode}")
                continue
            
            print(f"  -> Processing {mode}...")
            # Routes
            r_df = pd.read_csv(routes_file, low_memory=False)
            r_df['original_route_id'] = r_df['route_id']
            r_df['route_id'] = f"{mode}_" + r_df['route_id'].astype(str)
            r_df['mode'] = mode
            cols_r = ['route_id', 'original_route_id', 'mode', 'route_short_name', 'route_long_name', 'route_type']
            all_routes.append(r_df[[c for c in cols_r if c in r_df.columns]])
            
            # Trips
            t_df = pd.read_csv(trips_file, low_memory=False)
            t_df['original_trip_id'] = t_df['trip_id']
            t_df['trip_id'] = f"{mode}_" + t_df['trip_id'].astype(str)
            t_df['route_id'] = f"{mode}_" + t_df['route_id'].astype(str)
            cols_t = ['trip_id', 'original_trip_id', 'route_id', 'service_id']
            all_trips.append(t_df[[c for c in cols_t if c in t_df.columns]])
            
            # Stop Times
            st_df = pd.read_csv(stop_times_file, low_memory=False)
            # handle potential missing / empty values
            st_df['trip_id'] = f"{mode}_" + st_df['trip_id'].astype(str)
            st_df['stop_id'] = f"{mode}_" + st_df['stop_id'].astype(str)
            cols_st = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence']
            all_stop_times.append(st_df[[c for c in cols_st if c in st_df.columns]])
            
        return pd.concat(all_routes, ignore_index=True), pd.concat(all_trips, ignore_index=True), pd.concat(all_stop_times, ignore_index=True)

if __name__ == "__main__":
    base_dir = '/Users/bharatoraon/Downloads/Chennai'
    processor = GTFSProcessor(base_dir)
    
    # Process Stops
    stops_gdf = processor.load_and_standardize_stops()
    output_dir = os.path.join(base_dir, 'thesis_analysis', 'output')
    os.makedirs(output_dir, exist_ok=True)
    out_stops = os.path.join(output_dir, 'unified_stops.geojson')
    stops_gdf.to_file(out_stops, driver='GeoJSON')
    print(f"Saved {out_stops}")
    
    # Process Schedules
    r_df, t_df, st_df = processor.load_and_standardize_schedules()
    print("\nUnified Routes:", len(r_df))
    print("Unified Trips:", len(t_df))
    print("Unified Stop Times:", len(st_df))
    
    # Save unified CSVs
    r_df.to_csv(os.path.join(output_dir, 'unified_routes.csv'), index=False)
    t_df.to_csv(os.path.join(output_dir, 'unified_trips.csv'), index=False)
    st_df.to_csv(os.path.join(output_dir, 'unified_stop_times.csv'), index=False)
    print("Saved unified schedules to output directory.")
