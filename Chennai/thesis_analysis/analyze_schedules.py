import pandas as pd
import os
import matplotlib.pyplot as plt

def extract_hour(time_str):
    try:
        hours = int(str(time_str).split(':')[0])
        return hours % 24 # Handle >24hr GTFS formats gracefully
    except:
        return -1

def analyze_schedules():
    base_dir = '/Users/bharatoraon/Downloads/Chennai/thesis_analysis/output'
    st_file = os.path.join(base_dir, 'unified_stop_times.csv')
    
    print("Loading unified stop times...")
    st_df = pd.read_csv(st_file, usecols=['trip_id', 'departure_time'])
    
    # Extract mode from trip_id (format: mode_id)
    st_df['mode'] = st_df['trip_id'].apply(lambda x: str(x).split('_')[0])
    
    # Extract hour from departure_time
    st_df['hour'] = st_df['departure_time'].apply(extract_hour)
    
    # Filter invalid hours (if any)
    st_df = st_df[st_df['hour'] >= 0]
    
    # Group by mode and hour to count departures (proxy for frequency)
    grouped = st_df.groupby(['mode', 'hour']).size().unstack(level=0).fillna(0)
    
    print("\nDepartures per hour across modes:")
    print(grouped)
    
    # Plotting to save
    ax = grouped.plot(kind='line', figsize=(12, 6), marker='o')
    plt.title('Trip Frequencies by Hour of Day in Chennai')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Number of Departures')
    plt.grid(True)
    
    plot_file = os.path.join(base_dir, 'frequency_plot.png')
    plt.savefig(plot_file)
    print(f"\nSaved frequency plot to {plot_file}")

if __name__ == "__main__":
    analyze_schedules()
