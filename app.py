from flask import Flask, jsonify, render_template, request, send_file
import pandas as pd
import numpy as np
from flask_cors import CORS
import plotly.graph_objects as go
import plotly.utils
import json
import os
import folium
from scipy.stats import pearsonr
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import cv2
from PIL import Image
import io
import base64
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import xml.etree.ElementTree as ET
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# --------------------------
# AI-Driven Data Integration Classes
# --------------------------
class MolecularBiologyAnalyzer:
    """AI-powered molecular biology data analysis for eDNA and species identification"""
    
    def __init__(self):
        self.sequence_database = {}
        self.species_classifier = None
        
    def analyze_edna_sequence(self, sequence_data):
        """Analyze eDNA sequences for species identification"""
        try:
            # Simulate DNA sequence analysis
            sequence = sequence_data.get('sequence', '')
            if len(sequence) < 10:
                return {'error': 'Sequence too short for analysis'}
            
            # Basic sequence statistics
            gc_content = (sequence.count('G') + sequence.count('C')) / len(sequence) * 100
            at_content = (sequence.count('A') + sequence.count('T')) / len(sequence) * 100
            
            # Simulate species identification confidence
            confidence = min(95, 60 + np.random.normal(0, 10))
            
            return {
                'sequence_length': len(sequence),
                'gc_content': round(gc_content, 2),
                'at_content': round(at_content, 2),
                'predicted_species': self._predict_species(sequence),
                'confidence': round(confidence, 2),
                'analysis_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _predict_species(self, sequence):
        """Predict species based on sequence characteristics"""
        # Simulate species prediction based on sequence patterns
        species_candidates = [
            'Sardinella longiceps', 'Rastrelliger kanagurta', 'Lutjanus argentimaculatus',
            'Epinephelus coioides', 'Lates calcarifer', 'Mugil cephalus'
        ]
        return np.random.choice(species_candidates)

class OtolithAnalyzer:
    """AI-powered otolith shape and morphometrics analysis"""
    
    def __init__(self):
        self.morphometric_features = []
        
    def analyze_otolith_shape(self, image_data):
        """Analyze otolith shape and extract morphometric features"""
        try:
            # Convert base64 image to OpenCV format
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return {'error': 'No otolith contours detected'}
            
            # Get largest contour (assuming it's the otolith)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Calculate morphometric features
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 0
            
            # Circularity
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # Ellipse fitting
            if len(largest_contour) >= 5:
                ellipse = cv2.fitEllipse(largest_contour)
                (center, axes, angle) = ellipse
                major_axis = max(axes)
                minor_axis = min(axes)
                ellipticity = major_axis / minor_axis if minor_axis > 0 else 0
            else:
                ellipticity = 0
                major_axis = minor_axis = 0
            
            return {
                'area': round(area, 2),
                'perimeter': round(perimeter, 2),
                'aspect_ratio': round(aspect_ratio, 3),
                'circularity': round(circularity, 3),
                'ellipticity': round(ellipticity, 3),
                'major_axis': round(major_axis, 2),
                'minor_axis': round(minor_axis, 2),
                'analysis_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f'Otolith analysis failed: {str(e)}'}

class AdvancedAnalytics:
    """AI-driven advanced analytics for cross-disciplinary correlation analysis"""
    
    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()
        
    def perform_pca_analysis(self, features):
        """Perform Principal Component Analysis on selected features"""
        try:
            # Prepare data
            feature_data = self.data[features].dropna()
            
            if len(feature_data) < 2:
                return {'error': 'Insufficient data for PCA analysis'}
            
            # Standardize features
            scaled_data = self.scaler.fit_transform(feature_data)
            
            # Perform PCA
            pca = PCA(n_components=min(3, len(features)))
            pca_result = pca.fit_transform(scaled_data)
            
            return {
                'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
                'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist(),
                'components': pca.components_.tolist(),
                'feature_names': features,
                'pca_scores': pca_result.tolist()
            }
        except Exception as e:
            return {'error': f'PCA analysis failed: {str(e)}'}
    
    def predict_fish_abundance(self, ocean_params, species):
        """Predict fish abundance using machine learning"""
        try:
            # Prepare features (ocean parameters)
            X = self.data[ocean_params].dropna()
            y = self.data[species].dropna()
            
            # Align data
            common_idx = X.index.intersection(y.index)
            if len(common_idx) < 10:
                return {'error': 'Insufficient data for prediction'}
            
            X_aligned = X.loc[common_idx]
            y_aligned = y.loc[common_idx]
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_aligned, y_aligned, test_size=0.2, random_state=42
            )
            
            # Train Random Forest model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            r2 = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            
            # Feature importance
            feature_importance = dict(zip(ocean_params, model.feature_importances_))
            
            return {
                'r2_score': round(r2, 3),
                'mse': round(mse, 2),
                'feature_importance': feature_importance,
                'predictions': y_pred.tolist(),
                'actual_values': y_test.tolist()
            }
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}

# Initialize AI modules
molecular_analyzer = MolecularBiologyAnalyzer()
otolith_analyzer = OtolithAnalyzer()

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
# AI-Enhanced API Endpoints
# --------------------------

@app.route('/api/molecular/analyze-edna', methods=['POST'])
def api_analyze_edna():
    """Analyze eDNA sequences for species identification"""
    try:
        data = request.get_json()
        if not data or 'sequence' not in data:
            return jsonify({'error': 'Sequence data required'}), 400
        
        result = molecular_analyzer.analyze_edna_sequence(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/otolith/analyze-shape', methods=['POST'])
def api_analyze_otolith():
    """Analyze otolith shape and extract morphometric features"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'Image data required'}), 400
        
        result = otolith_analyzer.analyze_otolith_shape(data['image'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/pca', methods=['POST'])
def api_pca_analysis():
    """Perform Principal Component Analysis on selected features"""
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'Features list required'}), 400
        
        analytics = AdvancedAnalytics(df)
        result = analytics.perform_pca_analysis(data['features'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/predict-abundance', methods=['POST'])
def api_predict_abundance():
    """Predict fish abundance using machine learning"""
    try:
        data = request.get_json()
        if not data or 'ocean_params' not in data or 'species' not in data:
            return jsonify({'error': 'Ocean parameters and species required'}), 400
        
        analytics = AdvancedAnalytics(df)
        result = analytics.predict_fish_abundance(data['ocean_params'], data['species'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadata/eml', methods=['GET'])
def api_get_eml_metadata():
    """Get EML metadata for datasets"""
    try:
        eml_path = 'data/cmlre-platform/eml.xml'
        if os.path.exists(eml_path):
            tree = ET.parse(eml_path)
            root = tree.getroot()
            
            # Extract key metadata
            metadata = {
                'title': root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}title').text if root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}title') is not None else 'N/A',
                'creator': root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}individualName').text if root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}individualName') is not None else 'N/A',
                'organization': root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}organizationName').text if root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}organizationName') is not None else 'N/A',
                'country': root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}country').text if root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}country') is not None else 'N/A',
                'city': root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}city').text if root.find('.//{https://eml.ecoinformatics.org/eml-2.2.0}city') is not None else 'N/A'
            }
            return jsonify(metadata)
        else:
            return jsonify({'error': 'EML metadata not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/biodiversity/species-diversity')
def api_species_diversity():
    """Calculate species diversity metrics"""
    try:
        # Load occurrence data if available
        occurrence_path = 'data/cmlre-platform/occurrence.txt'
        if os.path.exists(occurrence_path):
            occurrence_df = pd.read_csv(occurrence_path, sep='\t')
            
            # Calculate diversity metrics
            total_species = occurrence_df['scientificName'].nunique()
            total_records = len(occurrence_df)
            
            # Geographic distribution
            unique_locations = occurrence_df[['decimalLatitude', 'decimalLongitude']].dropna().drop_duplicates()
            
            # Temporal distribution
            occurrence_df['eventDate'] = pd.to_datetime(occurrence_df['eventDate'], errors='coerce')
            year_range = f"{occurrence_df['eventDate'].dt.year.min()}-{occurrence_df['eventDate'].dt.year.max()}"
            
            return jsonify({
                'total_species': int(total_species),
                'total_records': int(total_records),
                'unique_locations': len(unique_locations),
                'year_range': year_range,
                'data_source': 'CMLRE Occurrence Data'
            })
        else:
            # Fallback to fisheries data
            fish_cols = [col for col in df.columns if col not in ['Year', 'total_catch', 'sst_avg', 'chlorophyll_a', 'Other']]
            active_species = [col for col in fish_cols if df[col].sum() > 0]
            
            return jsonify({
                'total_species': len(active_species),
                'total_records': len(df),
                'year_range': f"{df['Year'].min()}-{df['Year'].max()}",
                'data_source': 'Fisheries Catch Data'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecosystem/health-assessment')
def api_ecosystem_health():
    """Assess ecosystem health based on multiple indicators"""
    try:
        # Calculate ecosystem health indicators
        recent_data = df[df['Year'] >= df['Year'].max() - 5]  # Last 5 years
        
        # Biodiversity indicator (number of active species)
        active_species = [col for col in df.columns if col not in ['Year', 'total_catch', 'sst_avg', 'chlorophyll_a', 'Other'] and recent_data[col].sum() > 0]
        biodiversity_score = len(active_species) / len([col for col in df.columns if col not in ['Year', 'total_catch', 'sst_avg', 'chlorophyll_a', 'Other']]) * 100
        
        # Catch stability (coefficient of variation)
        catch_cv = (recent_data['total_catch'].std() / recent_data['total_catch'].mean()) * 100
        stability_score = max(0, 100 - catch_cv)
        
        # Ocean parameter trends
        sst_trend = recent_data['sst_avg'].iloc[-1] - recent_data['sst_avg'].iloc[0]
        chl_trend = recent_data['chlorophyll_a'].iloc[-1] - recent_data['chlorophyll_a'].iloc[0]
        
        # Overall health score
        health_score = (biodiversity_score + stability_score) / 2
        
        return jsonify({
            'overall_health_score': round(health_score, 1),
            'biodiversity_score': round(biodiversity_score, 1),
            'stability_score': round(stability_score, 1),
            'sst_trend': round(sst_trend, 3),
            'chlorophyll_trend': round(chl_trend, 3),
            'active_species_count': len(active_species),
            'assessment_period': f"{recent_data['Year'].min()}-{recent_data['Year'].max()}",
            'health_status': 'Good' if health_score > 70 else 'Moderate' if health_score > 50 else 'Poor'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --------------------------
# Main
# --------------------------
if __name__ == '__main__':
    # Avoid Windows console Unicode issues with emojis
    print("Starting CMLRE Marine Fisheries Prototype...")
    app.run(debug=True, port=5000)
