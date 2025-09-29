# MANTRA - Marine AI for National Transformation & Resource Assessment

## 🌊 AI-Driven Unified Data Platform for Oceanographic, Fisheries, and Molecular Biodiversity Insights

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)]()

### 🎯 Project Overview

MANTRA is an AI-enabled, intelligent digital platform designed to integrate heterogeneous marine datasets from oceanography, taxonomy, morphology, and molecular biology into a unified system. This platform serves as a national marine data backbone, empowering India's scientific community with next-generation tools for holistic marine ecosystem assessment.

### 🚀 Key Features

#### 🔬 **AI-Powered Molecular Biology Analysis**
- **eDNA Sequence Analysis**: Automated species identification from environmental DNA
- **Taxonomic Classification**: Machine learning-based species classification
- **Biodiversity Assessment**: Comprehensive species diversity metrics
- **Genetic Marker Analysis**: Advanced molecular biology tools

#### 🐟 **Otolith Morphometric Analysis**
- **Shape Analysis**: Automated otolith shape recognition and measurement
- **Morphometric Features**: Area, perimeter, aspect ratio, circularity analysis
- **Image Processing**: Computer vision-based otolith analysis
- **Age Determination**: Fish age estimation from otolith characteristics

#### 🌊 **Ecosystem Health Assessment**
- **Multi-Parameter Analysis**: Integrated assessment of biological and environmental indicators
- **Health Scoring**: Comprehensive ecosystem health metrics (0-100%)
- **Trend Analysis**: Long-term ecosystem monitoring and forecasting
- **Real-time Monitoring**: Live ecosystem health indicators

#### 📊 **Advanced Data Analytics**
- **Machine Learning**: Predictive modeling for fish abundance and distribution
- **Principal Component Analysis**: Dimensionality reduction and pattern recognition
- **Cross-Correlation Analysis**: Multi-parameter relationship analysis
- **Time Series Analysis**: Advanced temporal pattern recognition

#### 🗺️ **Interactive Visualizations**
- **EEZ Mapping**: Interactive Indian Exclusive Economic Zone visualization
- **Dynamic Charts**: Real-time data visualization with Plotly.js
- **Geographic Analysis**: Spatial data analysis and mapping
- **3D Visualizations**: Advanced spatial and temporal displays

### 🏗️ Architecture

```
MANTRA Platform
├── Backend (Flask)
│   ├── AI Modules
│   │   ├── MolecularBiologyAnalyzer
│   │   ├── OtolithAnalyzer
│   │   └── AdvancedAnalytics
│   ├── Data Integration
│   │   ├── Fisheries Data
│   │   ├── Oceanographic Data
│   │   ├── Biodiversity Data
│   │   └── Molecular Data
│   └── API Endpoints
│       ├── Core Data APIs
│       ├── AI-Enhanced APIs
│       └── Visualization APIs
├── Frontend (HTML/CSS/JS)
│   ├── Interactive Dashboard
│   ├── Analysis Modules
│   ├── Visualization Components
│   └── User Interface
└── Data Standards
    ├── EML (Ecological Metadata Language)
    ├── DwC-A (Darwin Core Archive)
    └── ISO 19115 (Geographic Metadata)
```

### 🛠️ Technology Stack

#### Backend Technologies
- **Flask**: Web framework for Python
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms
- **OpenCV**: Computer vision and image processing
- **BioPython**: Bioinformatics tools
- **Plotly**: Interactive visualizations
- **Folium**: Interactive mapping

#### Frontend Technologies
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive functionality
- **Plotly.js**: Advanced data visualization
- **Leaflet**: Interactive mapping
- **Bootstrap**: Responsive design framework

#### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scipy**: Scientific computing
- **OpenCV**: Image processing
- **PIL/Pillow**: Image handling

### 📦 Installation

#### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/mantra-marine/platform.git
cd platform

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

#### Detailed Installation
```bash
# Create virtual environment
python -m venv mantra_env
source mantra_env/bin/activate  # On Windows: mantra_env\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### 🎮 Usage

#### 1. **Dashboard Overview**
- Access the main dashboard to view dataset metrics
- Explore available data through interactive visualizations
- Navigate between different analysis modules

#### 2. **Catch Trends Analysis**
- Analyze temporal patterns in fish catch data
- Identify trends, peaks, and seasonal variations
- Compare multiple species over time

#### 3. **Geographic Analysis**
- Visualize marine data within Indian EEZ boundaries
- Explore fishing zones and catch distributions
- Interactive mapping with detailed information

#### 4. **Molecular Biology Analysis**
- Upload eDNA sequences for species identification
- Analyze genetic markers and biodiversity
- Automated species classification with confidence scoring

#### 5. **Otolith Analysis**
- Upload otolith images for morphometric analysis
- Extract shape features and measurements
- Fish age determination and growth analysis

#### 6. **Ecosystem Health Assessment**
- Comprehensive ecosystem health evaluation
- Multi-parameter health scoring
- Trend analysis and forecasting

### 📊 API Documentation

#### Core Data APIs
- `GET /api/data` - Dataset overview
- `GET /api/search` - Data search and filtering
- `GET /api/trends/{species}` - Species trend analysis

#### AI-Enhanced APIs
- `POST /api/molecular/analyze-edna` - eDNA sequence analysis
- `POST /api/otolith/analyze-shape` - Otolith morphometric analysis
- `POST /api/analytics/pca` - Principal component analysis
- `POST /api/analytics/predict-abundance` - Fish abundance prediction

#### Visualization APIs
- `GET /api/visualize/timeseries` - Time series charts
- `GET /api/visualize/correlations` - Correlation heatmaps
- `GET /api/visualize/map` - Interactive EEZ map

#### Ecosystem APIs
- `GET /api/biodiversity/species-diversity` - Biodiversity metrics
- `GET /api/ecosystem/health-assessment` - Ecosystem health evaluation
- `GET /api/metadata/eml` - EML metadata retrieval

### 📁 Project Structure

```
MANTRA-Marine-AI-for-National-Transformation-Resource-Assessment/
├── app.py                          # Main Flask application
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── API_DOCUMENTATION.md            # API reference
├── USER_MANUAL.md                  # User guide
├── data/                          # Data directory
│   ├── final.csv                  # Main fisheries dataset
│   └── cmlre-platform/            # CMLRE data
│       ├── eml.xml                # EML metadata
│       ├── meta.xml                # Additional metadata
│       └── occurrence.txt          # Species occurrence data
├── static/                        # Static assets
│   └── js/
│       └── main.js                 # JavaScript functionality
├── templates/                      # HTML templates
│   ├── index.html                  # Main dashboard
│   └── map.html                    # Map visualization
└── merging_data/                  # Data processing scripts
    ├── merge_datasets.py           # Dataset merging
    └── debug_sau.py                # Debug utilities
```

### 🔬 Scientific Applications

#### Marine Biology Research
- **Species Identification**: Automated classification using molecular markers
- **Biodiversity Assessment**: Comprehensive species diversity analysis
- **Population Dynamics**: Fish population monitoring and analysis
- **Ecosystem Modeling**: Marine ecosystem health assessment

#### Fisheries Management
- **Catch Prediction**: Machine learning-based abundance forecasting
- **Stock Assessment**: Fish stock evaluation and monitoring
- **Sustainable Fishing**: Data-driven conservation planning
- **Policy Support**: Evidence-based fisheries management

#### Oceanographic Research
- **Environmental Monitoring**: Ocean parameter tracking and analysis
- **Climate Impact Assessment**: Long-term environmental trend analysis
- **Ecosystem Health**: Multi-parameter ecosystem evaluation
- **Conservation Planning**: Data-driven marine conservation strategies

### 🌟 Key Innovations

#### 1. **Unified Data Integration**
- Seamless integration of heterogeneous marine datasets
- Standardized metadata using international formats
- Cross-disciplinary data correlation and analysis

#### 2. **AI-Powered Analysis**
- Machine learning for species identification
- Predictive modeling for ecosystem forecasting
- Automated pattern recognition and analysis

#### 3. **Interactive Visualization**
- Real-time data visualization
- Interactive mapping and charting
- User-friendly interface for scientists and policymakers

#### 4. **Scalable Architecture**
- Cloud-ready platform design
- Modular backend architecture
- RESTful API for external integration

### 🤝 Contributing

We welcome contributions from the marine science community! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Submit a pull request**

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🏛️ Institutional Support

**Centre for Marine Living Resources & Ecology (CMLRE)**
- **Organization**: Ministry of Earth Sciences, Government of India
- **Location**: Kochi, Kerala, India
- **Mission**: Marine living resources research and ecosystem management

### 📞 Support and Contact

- **Technical Support**: support@mantra-marine.ai
- **Documentation**: [API Documentation](API_DOCUMENTATION.md)
- **User Guide**: [User Manual](USER_MANUAL.md)
- **GitHub Issues**: [Report Issues](https://github.com/mantra-marine/platform/issues)

### 🙏 Acknowledgments

- **CMLRE Team**: For providing marine data and scientific expertise
- **Ministry of Earth Sciences**: For institutional support and funding
- **Marine Science Community**: For feedback and collaboration
- **Open Source Community**: For the excellent tools and libraries

### 🔮 Future Roadmap

#### Phase 1 (Current)
- ✅ Core platform development
- ✅ Basic AI integration
- ✅ Interactive visualizations
- ✅ API development

#### Phase 2 (Planned)
- 🔄 Advanced machine learning models
- 🔄 Real-time data streaming
- 🔄 Mobile application
- 🔄 Cloud deployment

#### Phase 3 (Future)
- 📋 International data integration
- 📋 Advanced predictive modeling
- 📋 Multi-language support
- 📋 Enterprise features

---

**MANTRA - Empowering Marine Science with AI**

*Transforming marine data into actionable insights for sustainable ocean management*

🌊🤖📊🔬
