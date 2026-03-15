import pandas as pd
import os

paths = {
    'bus': '/Users/bharatoraon/Downloads/Chennai/bus_gtfs',
    'metro': '/Users/bharatoraon/Downloads/Chennai/metro_gtfs',
    'suburban': '/Users/bharatoraon/Downloads/Chennai/suburban_gtfs'
}

files_to_check = ['stops.txt', 'routes.txt', 'trips.txt', 'stop_times.txt']

for mode, path in paths.items():
    print(f"\n--- {mode.upper()} ---")
    for file in files_to_check:
        file_path = os.path.join(path, file)
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, low_memory=False)
                print(f"[{file}] columns: {', '.join(df.columns)}")
                print(f"[{file}] rows: {len(df)}")
            except Exception as e:
                print(f"[{file}] error reading: {e}")
        else:
            print(f"[{file}] NOT FOUND")
