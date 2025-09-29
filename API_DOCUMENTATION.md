# MANTRA API Documentation
## AI-Driven Unified Data Platform for Oceanographic, Fisheries, and Molecular Biodiversity Insights

### Overview
MANTRA (Marine AI for National Transformation & Resource Assessment) provides a comprehensive API for marine data analysis, molecular biology research, and ecosystem health assessment. This platform integrates heterogeneous datasets from oceanography, taxonomy, morphology, and molecular biology into a unified system.

### Base URL
```
http://localhost:5000
```

---

## Core Data APIs

### 1. Data Overview
**GET** `/api/data`

Returns basic information about available datasets.

**Response:**
```json
{
  "years": [1950, 1951, 1952, ...],
  "species": ["Oil sardine", "Hilsa shad", "Penaeid prawns", ...],
  "ocean_params": ["sst_avg", "chlorophyll_a"],
  "total_records": 75,
  "total_catch": 2500000.0
}
```

### 2. Search Data
**GET** `/api/search`

Search and filter data by species and year.

**Parameters:**
- `query` (string): Species name to search for
- `year` (string): Specific year to filter

**Example:**
```
GET /api/search?query=sardine&year=2020
```

**Response:**
```json
[
  {
    "Year": 2020,
    "Oil sardine": 45000,
    "total_catch": 50000
  }
]
```

### 3. Species Trend Analysis
**GET** `/api/trends/{species}`

Analyze trends for a specific species.

**Example:**
```
GET /api/trends/Oil%20sardine
```

**Response:**
```json
{
  "species": "Oil sardine",
  "data": [...],
  "trend_percent": 15.5,
  "peak_year": 2018,
  "total_catch": 45000.0,
  "trend_direction": "increasing"
}
```

---

## Visualization APIs

### 4. Time Series Visualization
**GET** `/api/visualize/timeseries`

Returns Plotly JSON for time series charts of top species.

**Response:**
```json
{
  "plot": "{Plotly JSON object}"
}
```

### 5. Correlation Heatmap
**GET** `/api/visualize/correlations`

Returns correlation matrix between ocean parameters and fish catch.

**Response:**
```json
{
  "plot": "{Plotly JSON object}"
}
```

### 6. EEZ Map
**GET** `/api/visualize/map`

Returns HTML for interactive map of Indian Exclusive Economic Zone.

---

## AI-Enhanced Analysis APIs

### 7. eDNA Sequence Analysis
**POST** `/api/molecular/analyze-edna`

Analyze environmental DNA sequences for species identification.

**Request Body:**
```json
{
  "sequence": "ATCGATCGATCGATCG"
}
```

**Response:**
```json
{
  "sequence_length": 16,
  "gc_content": 50.0,
  "at_content": 50.0,
  "predicted_species": "Sardinella longiceps",
  "confidence": 85.2,
  "analysis_timestamp": "2024-01-15T10:30:00Z"
}
```

### 8. Otolith Shape Analysis
**POST** `/api/otolith/analyze-shape`

Analyze otolith images for morphometric features.

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**
```json
{
  "area": 1250.5,
  "perimeter": 150.2,
  "aspect_ratio": 1.25,
  "circularity": 0.65,
  "ellipticity": 1.8,
  "major_axis": 45.2,
  "minor_axis": 25.1,
  "analysis_timestamp": "2024-01-15T10:30:00Z"
}
```

### 9. Principal Component Analysis
**POST** `/api/analytics/pca`

Perform PCA on selected features.

**Request Body:**
```json
{
  "features": ["sst_avg", "chlorophyll_a", "Oil sardine", "Hilsa shad"]
}
```

**Response:**
```json
{
  "explained_variance_ratio": [0.45, 0.30, 0.15],
  "cumulative_variance": [0.45, 0.75, 0.90],
  "components": [[0.5, 0.3, 0.2], [0.2, 0.6, 0.2]],
  "feature_names": ["sst_avg", "chlorophyll_a", "Oil sardine", "Hilsa shad"],
  "pca_scores": [[1.2, -0.5], [0.8, 1.1]]
}
```

### 10. Fish Abundance Prediction
**POST** `/api/analytics/predict-abundance`

Predict fish abundance using machine learning.

**Request Body:**
```json
{
  "ocean_params": ["sst_avg", "chlorophyll_a"],
  "species": "Oil sardine"
}
```

**Response:**
```json
{
  "r2_score": 0.85,
  "mse": 1250.5,
  "feature_importance": {
    "sst_avg": 0.6,
    "chlorophyll_a": 0.4
  },
  "predictions": [45000, 48000, 42000],
  "actual_values": [44000, 47000, 41000]
}
```

---

## Biodiversity and Ecosystem APIs

### 11. Species Diversity Metrics
**GET** `/api/biodiversity/species-diversity`

Calculate biodiversity metrics from occurrence data.

**Response:**
```json
{
  "total_species": 150,
  "total_records": 2500,
  "unique_locations": 45,
  "year_range": "2018-2023",
  "data_source": "CMLRE Occurrence Data"
}
```

### 12. Ecosystem Health Assessment
**GET** `/api/ecosystem/health-assessment`

Assess overall ecosystem health based on multiple indicators.

**Response:**
```json
{
  "overall_health_score": 75.5,
  "biodiversity_score": 80.0,
  "stability_score": 71.0,
  "sst_trend": 0.5,
  "chlorophyll_trend": -0.1,
  "active_species_count": 12,
  "assessment_period": "2019-2024",
  "health_status": "Good"
}
```

### 13. EML Metadata
**GET** `/api/metadata/eml`

Retrieve EML (Ecological Metadata Language) metadata for datasets.

**Response:**
```json
{
  "title": "Indian Ocean Marine Fauna Voucher Specimens Collections",
  "creator": "Johnny Konjarla",
  "organization": "Centre for Marine Living Resources & Ecology",
  "country": "IN",
  "city": "Kochi"
}
```

---

## Error Handling

All APIs return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing parameters)
- `404`: Not Found (resource not found)
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message description"
}
```

---

## Usage Examples

### Python Example
```python
import requests
import json

# Analyze eDNA sequence
sequence_data = {"sequence": "ATCGATCGATCGATCG"}
response = requests.post('http://localhost:5000/api/molecular/analyze-edna', 
                        json=sequence_data)
result = response.json()
print(f"Predicted species: {result['predicted_species']}")

# Get ecosystem health
response = requests.get('http://localhost:5000/api/ecosystem/health-assessment')
health = response.json()
print(f"Ecosystem health: {health['health_status']}")
```

### JavaScript Example
```javascript
// Analyze otolith shape
const formData = new FormData();
formData.append('image', imageFile);

fetch('/api/otolith/analyze-shape', {
    method: 'POST',
    body: JSON.stringify({image: base64Image}),
    headers: {'Content-Type': 'application/json'}
})
.then(response => response.json())
.then(data => {
    console.log('Otolith area:', data.area);
});
```

---

## Data Standards

The platform supports international standards:
- **EML**: Ecological Metadata Language for dataset documentation
- **DwC-A**: Darwin Core Archive for biodiversity data
- **ISO 19115**: Geographic information metadata standards

---

## Rate Limiting

- API calls are limited to 100 requests per minute per IP
- Large file uploads (otolith images) are limited to 10MB
- Analysis requests are queued and processed asynchronously

---

## Support

For technical support and questions:
- Email: support@mantra-marine.ai
- Documentation: https://docs.mantra-marine.ai
- GitHub: https://github.com/mantra-marine/platform

---

*Last updated: January 2024*
*Version: 1.0.0*
