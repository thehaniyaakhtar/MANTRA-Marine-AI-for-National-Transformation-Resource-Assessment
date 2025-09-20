from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np
from flask_cors import CORS
import plotly.graph_objects as go
import plotly.utils
import json
import os
import folium
from scipy.stats import pearsonr

app = Flask(__name__)
CORS(app)

# --------------------------
# Data Loading
# --------------------------
data_path = 'data/final.csv'
if not os.path.exists(data_path):
    sample_data = """Year,Catfishes,Coilia,Eels,Hilsa shad,Non-penaeid prawns,Oil sardine,Other sardines,Penaeid prawns,Rays,Setipinna,Sharks,Skates,Squids,Stolephorus,Threadfin breams,Wolf herring,Other,total_catch
1950,0,0,0,847,0,34827,0,0,0,0,0,0,0,0,0,0,604500,35675
1951,0,0,0,780,0,17449,0,0,0,0,0,0,0,0,0,0,576623,18229
1952,0,0,0,772,0,14062,0,0,0,0,0,0,0,0,0,0,575763,14835
1953,0,0,0,850,0,52475,0,0,0,0,0,0,0,0,0,0,592030,53325
1954,0,0,0,820,0,48000,0,0,0,0,0,0,0,0,0,0,585000,48820
1955,0,0,0,900,0,55000,0,1000,0,0,0,0,0,0,0,0,600000,56100
1956,0,0,0,880,0,52000,0,1200,0,0,0,0,0,0,0,0,595000,54480
1957,0,0,0,950,0,58000,0,1500,0,0,0,0,0,0,0,0,610000,59650
1958,0,0,0,910,0,54000,0,1300,0,0,0,0,0,0,0,0,602000,55410
1959,0,0,0,870,0,51000,0,1100,0,0,0,0,0,0,0,0,590000,52270
"""
    with open(data_path, 'w') as f:
        f.write(sample_data)

df_fish = pd.read_csv(data_path)
df_fish['Year'] = pd.to_numeric(df_fish['Year'])

# --------------------------
# Add Ocean Parameters
# --------------------------
def add_ocean_params(df):
    df = df.copy()
    years_numeric = pd.to_numeric(df['Year'])
    df['sst_avg'] = 27 + 0.5 * np.sin(2 * np.pi * (years_numeric - 1950) / 30) + np.random.normal(0, 0.3, len(df))
    df['chlorophyll_a'] = 0.5 + 0.2 * np.sin(2 * np.pi * (years_numeric - 1950) / 25) + np.random.normal(0, 0.1, len(df))
    return df

df = add_ocean_params(df_fish)

# --------------------------
# Routes
# --------------------------
@app.route('/')
def home():
    years_range = f"{df['Year'].min()}-{df['Year'].max()}"
    years_count = len(df)
    species_count = len([col for col in df.columns if col not in ['Year', 'total_catch', 'Other', 'sst_avg', 'chlorophyll_a']])
    record_count = len(df)
    total_catch = df['total_catch'].sum()
    top_species = ['Oil sardine', 'Hilsa shad', 'Penaeid prawns', 'Sharks', 'Squids']
    available_top_species = [s for s in top_species if s in df.columns]
    
    return render_template(
        'index.html',
        years_range=years_range,
        years_count=years_count,
        species_count=species_count,
        record_count=record_count,
        total_catch=total_catch,
        top_species=available_top_species
    )

@app.route('/api/data')
def api_data():
    fish_cols = [col for col in df.columns[1:-3] if col not in ['Other'] and df[col].sum() > 0]
    return jsonify({
        'years': sorted(df['Year'].unique().tolist()),
        'species': fish_cols[:10],
        'ocean_params': ['sst_avg', 'chlorophyll_a'],
        'total_records': len(df),
        'total_catch': float(df['total_catch'].sum())
    })

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query', '')
    year = request.args.get('year', '')
    
    filtered_df = df.copy()
    
    if query:
        species_cols = [col for col in df.columns if query.lower() in col.lower() and col not in ['Year', 'total_catch', 'sst_avg', 'chlorophyll_a']]
        if species_cols:
            filtered_df = filtered_df[['Year'] + species_cols + ['total_catch']]
    
    if year:
        filtered_df = filtered_df[filtered_df['Year'] == int(year)]
    
    if filtered_df.empty:
        return jsonify({'error': 'No results found'}), 404
    
    return jsonify(filtered_df.to_dict('records'))

@app.route('/api/trends/<species>')
def api_species_trend(species):
    if species not in df.columns:
        return jsonify({'error': f'Species "{species}" not found'}), 404
    
    species_data = df[['Year', species, 'sst_avg', 'total_catch']].to_dict('records')
    
    first_val = float(df[species].iloc[0])
    last_val = float(df[species].iloc[-1])
    trend_pct = ((last_val - first_val) / first_val * 100) if first_val > 0 else 0
    
    peak_idx = df[species].idxmax()
    peak_year = int(df.loc[peak_idx, 'Year']) if not pd.isna(peak_idx) else int(df['Year'].iloc[0])
    
    return jsonify({
        'species': species,
        'data': species_data,
        'trend_percent': round(trend_pct, 2),
        'peak_year': peak_year,
        'total_catch': float(last_val),
        'trend_direction': 'increasing' if trend_pct > 0 else 'decreasing' if trend_pct < 0 else 'stable'
    })

@app.route('/api/visualize/timeseries')
def api_timeseries_viz():
    fig = go.Figure()
    
    active_species = [col for col in df.columns[1:-3] if col not in ['Other'] and df[col].sum() > 100]
    top_species = active_species[:3]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, species in enumerate(top_species):
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df[species],
            mode='lines',
            name=species,
            line=dict(width=3, color=colors[i])
        ))
    
    fig.update_layout(
        title='Top Species Catch Trends',
        xaxis_title='Year',
        yaxis_title='Catch (tonnes)',
        height=400
    )
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({'plot': graph_json})

@app.route('/api/visualize/correlations')
def api_correlation_viz():
    ocean_params = ['sst_avg', 'chlorophyll_a']
    fish_cols = [col for col in df.columns[1:-3] if col not in ['Other'] and df[col].sum() > 100][:3]
    analysis_cols = ocean_params + fish_cols
    
    corr_matrix = df[analysis_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu_r',
        zmid=0
    ))
    
    fig.update_layout(
        title='Ocean Parameters vs Fish Catch',
        height=400
    )
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({'plot': graph_json})

@app.route('/api/visualize/map')
def api_eez_map():
    m = folium.Map(
        location=[15, 80],
        zoom_start=5,
        tiles='CartoDB positron'
    )
    
    # EEZ boundary
    eez_boundary = [[8, 68], [25, 68], [25, 95], [8, 95]]
    folium.Polygon(
        locations=eez_boundary,
        color='#1e3c72',
        weight=2,
        fill=True,
        fill_color='#1e3c72',
        fill_opacity=0.1,
        popup='Indian Exclusive Economic Zone'
    ).add_to(m)
    
    # Fishing zones
    zones = [
        {'name': 'Arabian Sea', 'lat': 18, 'lon': 70, 'catch': df['total_catch'].mean() * 0.4},
        {'name': 'Bay of Bengal', 'lat': 15, 'lon': 85, 'catch': df['total_catch'].mean() * 0.3},
        {'name': 'Lakshadweep Sea', 'lat': 10, 'lon': 72, 'catch': df['total_catch'].mean() * 0.2}
    ]
    
    # Normalize circle sizes
    max_catch = max(zone['catch'] for zone in zones)
    for zone in zones:
        radius = (zone['catch'] / max_catch) * 20
        folium.CircleMarker(
            location=[zone['lat'], zone['lon']],
            radius=radius,
            color='#1e3c72',
            fill=True,
            fill_color='#1e3c72',
            fill_opacity=0.6,
            popup=f"<strong>{zone['name']}</strong><br>Est. Catch: {int(zone['catch']):,} tonnes"
        ).add_to(m)
    
    return m.get_root().render()

@app.route('/api/latest-trends')
def api_latest_trends():
    mock_trends = [
        {"title": "New EEZ Policy 2025", "content": "India expands EEZ for sustainable fisheries..."},
        {"title": "Biodiversity Report", "content": "Increased fish diversity in Arabian Sea..."}
    ]
    return jsonify(mock_trends)

# --------------------------
# Main
# --------------------------
if __name__ == '__main__':
    print("🚀 Starting CMLRE Marine Fisheries Prototype...")
    app.run(debug=True, port=5000)
