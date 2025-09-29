# MANTRA - Marine AI for National Transformation & Resource Assessment

## 🌊 AI-Driven Unified Data Platform for Oceanographic, Fisheries, and Molecular Biodiversity Insights

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)]()

### 🎯 Project Overview

MANTRA is an AI-enabled platform that integrates marine datasets from oceanography, fisheries, taxonomy, morphology, and molecular biology into a unified system. It serves as a national marine data backbone, empowering India’s scientific community with next-generation tools for holistic ecosystem assessment.

---

### 🚀 Key Features

#### 🔬 **Molecular Biology**

* Automated eDNA-based species identification
* Machine learning taxonomic classification
* Biodiversity and genetic marker analysis

#### 🐟 **Otolith Morphometry**

* Shape recognition and morphometric measurements
* Computer vision-based image processing
* Fish age estimation from otolith features

#### 🌊 **Ecosystem Health**

* Multi-parameter environmental and biological assessment
* Comprehensive health scoring and forecasting
* Real-time monitoring with trend analysis

#### 📊 **Data Analytics**

* Predictive modeling for fish abundance/distribution
* PCA, correlation, and time-series analysis
* Cross-disciplinary parameter integration

#### 🗺️ **Interactive Visualizations**

* Indian EEZ mapping with Leaflet/Folium
* Dynamic charts (Plotly.js) and 3D visualization
* Integrated spatial and temporal analysis

---

### 🏗️ Architecture

```
MANTRA Platform
├── Backend (Flask)
│   ├── AI Modules: Molecular, Otolith, Analytics
│   ├── Data Integration: Fisheries, Oceanography, Biodiversity, Molecular
│   └── API Endpoints: Data, AI, Visualization
├── Frontend (HTML/CSS/JS)
│   ├── Dashboard & Visualization Components
│   └── Analysis Modules
└── Data Standards: EML, DwC-A, ISO 19115
```

---

### 🛠️ Technology Stack

**Backend**: Flask, Pandas, NumPy, SciPy, Scikit-learn, OpenCV, BioPython
**Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap, Plotly.js, Leaflet
**Visualization & Mapping**: Plotly, Folium
**Image Processing**: OpenCV, Pillow

---

### 📦 Installation

#### Quick Start

```bash
git clone https://github.com/mantra-marine/platform.git
cd platform
pip install -r requirements.txt
python app.py
```

#### Virtual Environment

```bash
python -m venv mantra_env
source mantra_env/bin/activate   # Windows: mantra_env\Scripts\activate
pip install -r requirements.txt
python app.py
```

Application runs at `http://localhost:5000`.

---

### 🎮 Usage

1. **Dashboard** – Dataset metrics & interactive exploration
2. **Catch Trends** – Temporal fish catch patterns
3. **Geographic Analysis** – Marine data within Indian EEZ
4. **Molecular Biology** – Upload eDNA sequences for automated analysis
5. **Otolith Analysis** – Morphometric feature extraction & fish aging
6. **Ecosystem Health** – Comprehensive health scoring and forecasting

---

### 📊 API Endpoints

**Core**

* `GET /api/data` – Dataset overview
* `GET /api/trends/{species}` – Trend analysis

**AI-Enhanced**

* `POST /api/molecular/analyze-edna` – eDNA sequence analysis
* `POST /api/otolith/analyze-shape` – Otolith morphometrics
* `POST /api/analytics/predict-abundance` – Abundance prediction

**Visualization**

* `GET /api/visualize/timeseries` – Time series charts
* `GET /api/visualize/map` – Interactive EEZ map

**Ecosystem**

* `GET /api/biodiversity/species-diversity` – Diversity metrics
* `GET /api/ecosystem/health-assessment` – Health evaluation

---

### 📁 Project Structure

```
MANTRA/
├── app.py
├── requirements.txt
├── README.md
├── API_DOCUMENTATION.md
├── USER_MANUAL.md
├── data/
│   ├── final.csv
│   └── cmlre-platform/
│       ├── eml.xml
│       ├── meta.xml
│       └── occurrence.txt
├── static/js/main.js
├── templates/
│   ├── index.html
│   └── map.html
└── merging_data/
    ├── merge_datasets.py
    └── debug_sau.py
```

---

### 🔬 Applications

**Marine Biology**: Species identification, biodiversity metrics, population dynamics
**Fisheries Management**: Catch prediction, stock assessment, sustainable fishing strategies
**Oceanography**: Environmental monitoring, climate impact assessment, conservation planning

---

### 🌟 Innovations

1. **Unified Data Integration** with standardized metadata
2. **AI-Powered Analysis** for classification, prediction, and forecasting
3. **Interactive Visualization** via maps, charts, and 3D interfaces
4. **Scalable Architecture** with modular APIs and cloud readiness

---

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes and add tests
4. Submit a pull request

---

### 🏛️ Institutional Support

**Centre for Marine Living Resources & Ecology (CMLRE)**
Ministry of Earth Sciences, Government of India – Kochi, Kerala

---

### 🔮 Roadmap

* **Phase 1**: Core platform, AI basics, visualizations, APIs ✅
* **Phase 2**: Advanced ML models, real-time data streaming, mobile app, cloud deployment 🔄
* **Phase 3**: International integration, advanced forecasting, multi-language support, enterprise features 📋

---

**MANTRA – Empowering Marine Science with AI**

*Transforming marine data into actionable insights for sustainable ocean management*
🌊🤖📊🔬


