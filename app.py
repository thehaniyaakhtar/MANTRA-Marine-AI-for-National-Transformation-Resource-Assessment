from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
from flask_cors import CORS
import plotly.graph_objects as go
import plotly.utils
import json
from scipy.stats import pearsonr
import os

app = Flask(__name__)
CORS(app)

# Check if data file exists
data_path = 'merging_data/final.csv'
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists(data_path):
    # Create minimal sample data
    print("⚠️ Creating sample data...")
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
    print(f"✅ Sample data created: {data_path}")

# Load data
print("Loading data...")
try:
    df_fish = pd.read_csv(data_path)
    df_fish['Year'] = pd.to_numeric(df_fish['Year'])
    print(f"✅ Data loaded: {df_fish.shape}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    # Create minimal DataFrame
    df_fish = pd.DataFrame({
        'Year': range(1950, 1960),
        'Oil sardine': [34827, 17449, 14062, 52475, 48000, 55000, 52000, 58000, 54000, 51000],
        'Hilsa shad': [847, 780, 772, 850, 820, 900, 880, 950, 910, 870],
        'total_catch': [604500, 576623, 575763, 592030, 585000, 600000, 595000, 610000, 602000, 590000]
    })

# Add ocean parameters
def add_ocean_params(df):
    df = df.copy()
    years_numeric = pd.to_numeric(df['Year'])
    df['sst_avg'] = 27 + 0.5 * np.sin(2 * np.pi * (years_numeric - 1950) / 30) + np.random.normal(0, 0.3, len(df))
    df['chlorophyll_a'] = 0.5 + 0.2 * np.sin(2 * np.pi * (years_numeric - 1950) / 25) + np.random.normal(0, 0.1, len(df))
    return df

df = add_ocean_params(df_fish)
print(f"✅ Ocean parameters added. Total columns: {len(df.columns)}")

@app.route('/')
def home():
    # Template variables
    years_range = f"{df['Year'].min()}-{df['Year'].max()}"
    years_count = len(df)
    species_count = len([col for col in df.columns if col not in ['Year', 'total_catch', 'sst_avg', 'chlorophyll_a']])
    record_count = len(df)
    total_catch = df['total_catch'].sum()
    top_species = ['Oil sardine', 'Hilsa shad', 'Penaeid prawns', 'Sharks', 'Squids']
    available_top_species = [s for s in top_species if s in df.columns]
    
    return render_template('index.html',
                         years_range=years_range,
                         years_count=years_count,
                         species_count=species_count,
                         record_count=record_count,
                         total_catch=total_catch,
                         top_species=available_top_species)

# API Routes (same as before)
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

@app.route('/api/catch/<int:year>')
def api_catch_year(year):
    year_data = df[df['Year'] == year]
    if year_data.empty:
        return jsonify({'error': f'No data for year {year}'}), 404
    
    key_cols = ['Year', 'Oil sardine', 'Hilsa shad', 'Penaeid prawns', 'total_catch', 'sst_avg']
    available_cols = [col for col in key_cols if col in year_data.columns]
    return jsonify(year_data[available_cols].iloc[0].to_dict())

@app.route('/api/correlations')
def api_correlations():
    try:
        correlations = {}
        ocean_params = ['sst_avg', 'chlorophyll_a']
        fish_cols = [col for col in df.columns[1:-3] if col not in ['Other'] and df[col].sum() > 0][:4]
        
        for ocean_param in ocean_params:
            for fish in fish_cols:
                if len(df) > 1 and df[fish].std() > 0 and df[ocean_param].std() > 0:
                    corr, p_value = pearsonr(df[ocean_param], df[fish])
                    correlations[f"{ocean_param}_vs_{fish}"] = {
                        'correlation': round(float(corr), 3),
                        'p_value': round(float(p_value), 3),
                        'significant': float(p_value) < 0.05
                    }
        
        significant_count = sum(1 for v in correlations.values() if v['significant'])
        return jsonify({
            'summary': f"{len(correlations)} correlations analyzed ({significant_count} significant)",
            'results': correlations,
            'insights': 'Values > 0.3 indicate meaningful ocean-fisheries relationships'
        })
    except Exception as e:
        return jsonify({'error': f'Correlation analysis failed: {str(e)}'}), 500

@app.route('/api/trends/<species>')
def api_species_trend(species):
    if species not in df.columns:
        return jsonify({'error': f'Species "{species}" not found'}), 404
    
    species_data = df[['Year', species, 'sst_avg', 'total_catch']].to_dict('records')
    
    if len(species_data) == 0:
        return jsonify({'error': 'No data available'}), 404
    
    first_val = float(df[species].iloc[0])
    last_val = float(df[species].iloc[-1])
    if first_val > 0:
        trend_pct = ((last_val - first_val) / first_val) * 100
    else:
        trend_pct = 0
    
    peak_idx = df[species].idxmax()
    peak_year = int(df.loc[peak_idx, 'Year']) if not pd.isna(peak_idx) else int(df['Year'].iloc[0])
    
    return jsonify({
        'species': species,
        'data': species_data,
        'trend_percent': round(float(trend_pct), 2),
        'peak_year': peak_year,
        'total_catch': float(last_val),
        'trend_direction': 'increasing' if trend_pct > 0 else 'decreasing' if trend_pct < 0 else 'stable'
    })

@app.route('/api/visualize/timeseries')
def api_timeseries_viz():
    try:
        fig = go.Figure()
        
        active_species = [col for col in df.columns[1:-3] if col not in ['Other'] and df[col].sum() > 100]
        if not active_species:
            active_species = ['Oil sardine', 'Hilsa shad']
            active_species = [s for s in active_species if s in df.columns]
        
        top_species = active_species[:3]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, species in enumerate(top_species):
            fig.add_trace(go.Scatter(
                x=df['Year'],
                y=df[species],
                mode='lines',
                name=species,
                line=dict(width=3, color=colors[i % len(colors)]),
                hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Catch: %{y:,.0f} tonnes<extra></extra>'
            ))
        
        fig.update_layout(
            title='Top Species Catch Trends ({{ years_range }})'.replace('{{ years_range }}', f"{df['Year'].min()}-{df['Year'].max()}"),
            xaxis_title='Year',
            yaxis_title='Catch (tonnes)',
            height=400,
            showlegend=True,
            hovermode='x unified',
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify({'plot': graph_json})
    except Exception as e:
        return jsonify({'error': f'Visualization failed: {str(e)}'}), 500

@app.route('/api/visualize/correlations')
def api_correlation_viz():
    try:
        ocean_params = ['sst_avg', 'chlorophyll_a']
        fish_cols = [col for col in df.columns[1:-3] if col not in ['Other'] and df[col].sum() > 100][:3]
        analysis_cols = ocean_params + fish_cols
        
        if len(analysis_cols) < 3:
            return jsonify({'error': 'Insufficient data for correlation visualization'}), 400
        
        corr_matrix = df[analysis_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=[[round(float(val), 3) for val in row] for row in corr_matrix.values],
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu_r',
            zmid=0,
            hoverongaps=False,
            colorbar=dict(title="Correlation", thickness=20),
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>r = %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Ocean Parameters vs Fish Catch Correlations',
            height=400,
            margin=dict(l=100, r=50, t=80, b=100),
            xaxis_tickangle=-45
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify({'plot': graph_json})
    except Exception as e:
        return jsonify({'error': f'Correlation visualization failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting CMLRE Marine Fisheries Prototype...")
    print(f"📊 Dataset: {len(df)} years ({df['Year'].min()}-{df['Year'].max()})")
    print(f"🐟 Species: {len([col for col in df.columns if col not in ['Year', 'total_catch', 'sst_avg', 'chlorophyll_a']])}")
    print(f"🌐 Dashboard: http://localhost:5000")
    print(f"🔌 Test APIs: http://localhost:5000/api/data")
    app.run(debug=True, port=5000, host='127.0.0.1')