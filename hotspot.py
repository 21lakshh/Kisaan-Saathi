import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import folium
import os

def detect_hotspots():
    # Dummy data with latitude and longitude
    data = [
    [26.8415, 75.5659],
    [26.8418, 75.5662],  
    [26.8420, 75.5665],  
    [26.8412, 75.5661], 
    [26.8417, 75.5664],  
    [26.8510, 75.5790],  
    [26.8520, 75.5800],  
    [26.8505, 75.5785],  
    [26.8508, 75.5788],  
    [26.8515, 75.5795],  
    [26.8850, 75.7300], 
    [26.8855, 75.7305], 
    [26.8860, 75.7310],  
    [26.8858, 75.7308],  
    [26.8865, 75.7315],  
    [26.8700, 75.7800],  
    [26.8705, 75.7805],  
    [26.8710, 75.7810],  
    [26.8715, 75.7815],  
    [26.8708, 75.7808], 
    [26.9120, 75.7450],  
    [26.9125, 75.7455],  
    [26.9130, 75.7460],  
    [26.9128, 75.7458],  
    [26.9000, 75.7800],
    [26.9005, 75.7805],  
    [26.9010, 75.7810],  
    [26.8500, 75.8000], 
    [26.8505, 75.8005],  
    [26.8510, 75.8010],  
    [26.8512, 75.8012],  
    [26.8700, 75.8200],  
    [26.8705, 75.8205],  
    [26.8710, 75.8210],  
    [26.8715, 75.8215],  
    [26.9500, 75.9000],  
    [26.9600, 75.9100],  
    [26.9700, 75.9200],  
    
    # Completely Random Outliers (Not Part of Any Cluster)
    [27.1000, 76.2000],  # Completely random point
    [27.1500, 76.2500],  # Completely random point
    [26.5000, 75.3000],  # Completely random point
    [27.3000, 76.5000],  # Completely random point
    [26.7000, 75.7000],  # Completely random point
    [26.2500, 75.0500],  # Completely random point
    [27.0000, 76.0000]  # Completely random point
    ]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['latitude', 'longitude'])
    
    # Extract coordinates
    coordinates = df[['latitude', 'longitude']].values
    
    # Standardize the coordinates
    scaler = StandardScaler()
    coordinates_scaled = scaler.fit_transform(coordinates)
    
    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=0.01, min_samples=3)
    clusters = dbscan.fit_predict(coordinates_scaled)
    
    # Add cluster labels to the DataFrame
    df['cluster'] = clusters
    
    # Calculate priority based on cluster size
    cluster_sizes = df[df['cluster'] != -1].groupby('cluster').size()
    max_size = cluster_sizes.max()
    min_size = cluster_sizes.min()
    
    # Define priority levels based on cluster size
    def get_priority(size):
        if size >= max_size * 0.8:
            return "High"
        elif size >= max_size * 0.5:
            return "Medium"
        else:
            return "Low"
    
    # Add priority to DataFrame
    df['priority'] = "Low"  # Default for outliers
    for cluster_id in cluster_sizes.index:
        size = cluster_sizes[cluster_id]
        df.loc[df['cluster'] == cluster_id, 'priority'] = get_priority(size)
    
    # Create a map centered on Rajasthan
    rajasthan_center = [26.9124, 75.7873]
    m = folium.Map(location=rajasthan_center, zoom_start=8)
    
    # Define colors for clusters based on priority
    colors = {
        "High": 'red',
        "Medium": 'orange',
        "Low": 'green'
    }
    
    # Add markers for each point
    for idx, row in df.iterrows():
        color = colors.get(row['priority'], 'gray')
        
        # Create popup content
        popup_content = f"""
        <div>
            <strong>{'Outlier' if row['cluster'] == -1 else f'Cluster {row["cluster"]}'}</strong><br>
            Priority: {row['priority']}<br>
            Reports: {cluster_sizes.get(row['cluster'], 1)}
        </div>
        """
        
        # Add marker to the map
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=6,
            popup=popup_content,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
    
    # Add a simple legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; right: 50px; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
        <p style="margin: 0 0 5px 0;"><strong>Priority Levels:</strong></p>
        <p style="margin: 0 0 5px 0;"><span style="color: red">●</span> High Priority</p>
        <p style="margin: 0 0 5px 0;"><span style="color: orange">●</span> Medium Priority</p>
        <p style="margin: 0 0 5px 0;"><span style="color: green">●</span> Low Priority</p>
        <p style="margin: 0;"><span style="color: gray">●</span> Outliers</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Save the map in the static folder
    m.save('static/hotspot_map.html')
    
    return df

if __name__ == "__main__":
    df = detect_hotspots()
    if df is not None:
        print("\nHotspot Analysis Results:")
        print(f"Total Reports: {len(df)}")
        print(f"Number of Clusters: {len(set(df['cluster'])) - 1}")  # -1 for outliers
        
        # Print cluster information
        for cluster_id in sorted(set(df['cluster'])):
            if cluster_id != -1:  # Skip outliers
                cluster_reports = df[df['cluster'] == cluster_id]
                print(f"\nCluster {cluster_id}:")
                print(f"Number of Reports: {len(cluster_reports)}")
                print(f"Priority: {cluster_reports['priority'].iloc[0]}")