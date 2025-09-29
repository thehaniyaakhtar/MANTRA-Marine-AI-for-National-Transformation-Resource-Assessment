# MANTRA User Manual
## AI-Driven Unified Data Platform for Oceanographic, Fisheries, and Molecular Biodiversity Insights

### Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Platform Overview](#platform-overview)
4. [Core Features](#core-features)
5. [User Interface Guide](#user-interface-guide)
6. [Data Analysis Modules](#data-analysis-modules)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Introduction

MANTRA (Marine AI for National Transformation & Resource Assessment) is an AI-enabled, intelligent digital platform designed to integrate heterogeneous marine datasets from oceanography, taxonomy, morphology, and molecular biology into a unified system. This platform serves as a national marine data backbone, empowering India's scientific community with next-generation tools for holistic marine ecosystem assessment.

### Key Benefits
- **Unified Data Integration**: Seamlessly combine data from multiple marine science disciplines
- **AI-Powered Analysis**: Advanced machine learning for species identification and ecosystem modeling
- **Real-time Visualization**: Interactive dashboards for data exploration and analysis
- **Standardized Metadata**: International format compliance (EML, DwC-A)
- **Scalable Architecture**: Cloud-ready platform for future expansion

---

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for data visualization
- JavaScript enabled
- Minimum 4GB RAM for optimal performance

### Accessing the Platform
1. Navigate to the MANTRA platform URL
2. The main dashboard will load automatically
3. No login required for the prototype version

### First Steps
1. **Explore the Dashboard**: Familiarize yourself with the main interface
2. **View Data Overview**: Check the metrics grid for dataset summary
3. **Try Basic Analysis**: Use the species analysis tool
4. **Explore Visualizations**: Switch between different chart types

---

## Platform Overview

### Main Dashboard Components

#### 1. Header Section
- **Platform Title**: MANTRA branding
- **Subtitle**: Marine AI for National Transformation & Resource Assessment
- **Data Range**: Shows the temporal coverage of available data

#### 2. Metrics Grid
- **Years Covered**: Total time span of data
- **Fish Categories**: Number of species/groups tracked
- **Total Records**: Number of data points
- **Total Catch**: Cumulative catch in tonnes

#### 3. Visualization Controls
- **Catch Trends**: Time series analysis
- **EEZ Map**: Geographic visualization
- **Correlations**: Cross-parameter analysis
- **Molecular Analysis**: eDNA and species identification
- **Otolith Analysis**: Morphometric analysis
- **Ecosystem Health**: Overall system assessment

---

## Core Features

### 1. Data Integration
MANTRA integrates multiple data sources:
- **Fisheries Data**: Catch statistics and species abundance
- **Oceanographic Data**: Sea surface temperature, chlorophyll-a
- **Biodiversity Data**: Species occurrence records
- **Molecular Data**: eDNA sequences and genetic information
- **Morphological Data**: Otolith shape and size measurements

### 2. AI-Powered Analysis
- **Species Identification**: Automated classification using molecular markers
- **Trend Analysis**: Machine learning-based prediction models
- **Pattern Recognition**: Cross-disciplinary correlation analysis
- **Ecosystem Modeling**: Health assessment and forecasting

### 3. Interactive Visualizations
- **Time Series Charts**: Dynamic plotting with Plotly.js
- **Geographic Maps**: Interactive EEZ mapping with Folium
- **Correlation Heatmaps**: Multi-parameter relationship analysis
- **3D Visualizations**: Advanced spatial and temporal displays

---

## User Interface Guide

### Navigation
The platform uses a tabbed interface for different analysis modules:

#### Main Navigation Tabs
1. **📈 Catch Trends**: Time series analysis of fish catch data
2. **🗺️ EEZ Map**: Geographic visualization of Indian Exclusive Economic Zone
3. **🔗 Correlations**: Cross-parameter correlation analysis
4. **🧬 Molecular Analysis**: eDNA sequence analysis and species identification
5. **🐟 Otolith Analysis**: Fish otolith shape and morphometric analysis
6. **🌊 Ecosystem Health**: Overall ecosystem health assessment

### Interactive Elements

#### Control Panels
- **Species Selector**: Dropdown menu for species-specific analysis
- **Analysis Buttons**: Trigger specific analytical processes
- **Parameter Controls**: Adjust visualization parameters

#### Results Display
- **Metrics Cards**: Key statistics and indicators
- **Chart Containers**: Interactive visualizations
- **Analysis Results**: Detailed findings and interpretations

---

## Data Analysis Modules

### 1. Catch Trends Analysis

#### Purpose
Analyze temporal patterns in fish catch data to identify trends, peaks, and seasonal variations.

#### How to Use
1. Select the "📈 Catch Trends" tab
2. The system automatically loads the top 3 most active species
3. Charts display time series data with interactive features
4. Hover over data points for detailed information

#### Key Metrics
- **Trend Percentage**: Overall change over time period
- **Peak Year**: Year with highest recorded catch
- **Latest Catch**: Most recent catch data
- **Trend Direction**: Increasing, decreasing, or stable

### 2. Geographic Analysis (EEZ Map)

#### Purpose
Visualize marine data within the Indian Exclusive Economic Zone boundaries.

#### How to Use
1. Select the "🗺️ EEZ Map" tab
2. Interactive map loads with fishing zones marked
3. Click on markers for detailed information
4. Zoom and pan for detailed exploration

#### Features
- **EEZ Boundary**: Clearly marked exclusive economic zone
- **Fishing Zones**: Arabian Sea, Bay of Bengal, Lakshadweep Sea
- **Catch Estimates**: Approximate catch data for each zone
- **Interactive Markers**: Click for detailed information

### 3. Correlation Analysis

#### Purpose
Identify relationships between oceanographic parameters and fish catch data.

#### How to Use
1. Select the "🔗 Correlations" tab
2. Heatmap displays correlation matrix
3. Color coding indicates strength of relationships
4. Red indicates positive correlation, blue indicates negative

#### Interpretation
- **Strong Positive (Red)**: Parameters increase together
- **Strong Negative (Blue)**: Parameters have inverse relationship
- **Neutral (White)**: No significant relationship

### 4. Molecular Biology Analysis

#### Purpose
Analyze environmental DNA (eDNA) sequences for species identification and biodiversity assessment.

#### How to Use
1. Select the "🧬 Molecular Analysis" tab
2. Enter DNA sequence in ATCG format
3. Click "🔬 Analyze Sequence"
4. View results including species prediction and confidence

#### Features
- **Sequence Analysis**: GC content, length, composition
- **Species Prediction**: AI-powered species identification
- **Confidence Scoring**: Reliability assessment of predictions
- **Biodiversity Metrics**: Species diversity and distribution

#### Example Sequence
```
ATCGATCGATCGATCGATCGATCGATCGATCG
```

### 5. Otolith Analysis

#### Purpose
Analyze fish otolith (ear bone) images for morphometric features and age determination.

#### How to Use
1. Select the "🐟 Otolith Analysis" tab
2. Upload an otolith image (JPG, PNG format)
3. Click "🔍 Analyze Shape"
4. View morphometric measurements and analysis

#### Supported Features
- **Shape Analysis**: Area, perimeter, aspect ratio
- **Morphometric Features**: Circularity, ellipticity, axis measurements
- **Image Processing**: Automated contour detection
- **Quality Assessment**: Analysis confidence indicators

#### Image Requirements
- **Format**: JPG, PNG
- **Size**: Maximum 10MB
- **Quality**: Clear, well-lit otolith images
- **Background**: Contrasting background recommended

### 6. Ecosystem Health Assessment

#### Purpose
Evaluate overall ecosystem health based on multiple biological and environmental indicators.

#### How to Use
1. Select the "🌊 Ecosystem Health" tab
2. System automatically calculates health metrics
3. View comprehensive health dashboard
4. Monitor trends and indicators

#### Health Indicators
- **Overall Health Score**: Composite health assessment (0-100%)
- **Biodiversity Score**: Species richness and diversity
- **Stability Score**: Catch variability and consistency
- **Environmental Trends**: SST and chlorophyll changes
- **Active Species Count**: Number of species with recent data

#### Health Status Levels
- **Good (70-100%)**: Healthy ecosystem with stable indicators
- **Moderate (50-69%)**: Some concerns, monitoring recommended
- **Poor (<50%)**: Significant issues, intervention needed

---

## Advanced Features

### Machine Learning Integration

#### Predictive Modeling
- **Fish Abundance Prediction**: Forecast future catch based on environmental parameters
- **Species Distribution Modeling**: Predict species presence in different areas
- **Ecosystem Forecasting**: Long-term ecosystem health projections

#### Principal Component Analysis (PCA)
- **Dimensionality Reduction**: Identify key factors driving ecosystem changes
- **Pattern Recognition**: Discover hidden relationships in complex datasets
- **Feature Importance**: Rank parameters by their influence on outcomes

### Data Export and Integration

#### Export Options
- **CSV Export**: Download processed data for external analysis
- **JSON API**: Programmatic access to all platform features
- **Visualization Export**: Save charts and graphs as images
- **Report Generation**: Automated analysis reports

#### API Integration
- **RESTful APIs**: Standard HTTP endpoints for data access
- **Real-time Updates**: Live data streaming capabilities
- **Batch Processing**: Handle large datasets efficiently
- **Custom Queries**: Flexible data filtering and aggregation

---

## Troubleshooting

### Common Issues

#### 1. Charts Not Loading
**Problem**: Visualization containers show "Loading..." indefinitely
**Solution**: 
- Check internet connection
- Refresh the page
- Clear browser cache
- Ensure JavaScript is enabled

#### 2. File Upload Issues
**Problem**: Otolith image upload fails
**Solution**:
- Check file format (JPG, PNG only)
- Ensure file size < 10MB
- Use clear, well-lit images
- Try different browser

#### 3. Analysis Errors
**Problem**: Analysis returns error messages
**Solution**:
- Check input data format
- Ensure all required fields are filled
- Try with sample data first
- Contact support if persistent

#### 4. Performance Issues
**Problem**: Platform runs slowly
**Solution**:
- Close other browser tabs
- Check available RAM
- Use modern browser
- Clear browser cache

### Error Messages

#### "No data found"
- Check data availability for selected parameters
- Verify date ranges and filters
- Contact administrator for data access

#### "Analysis failed"
- Verify input data format
- Check for missing required fields
- Try with different parameters
- Contact technical support

#### "File too large"
- Reduce image file size
- Use image compression
- Try different file format
- Contact support for large file handling

---

## Best Practices

### Data Quality
1. **Use High-Quality Images**: Clear, well-lit otolith images for best analysis results
2. **Complete Sequences**: Provide full DNA sequences for accurate species identification
3. **Regular Updates**: Keep data current for accurate trend analysis
4. **Standardized Formats**: Follow international data standards

### Analysis Workflow
1. **Start with Overview**: Begin with dashboard metrics and trends
2. **Drill Down**: Use specific analysis modules for detailed investigation
3. **Cross-Reference**: Compare results across different analysis types
4. **Document Findings**: Save and export important results

### Performance Optimization
1. **Batch Processing**: Group similar analyses together
2. **Selective Loading**: Load only necessary data for current analysis
3. **Cache Results**: Save intermediate results for repeated analysis
4. **Regular Maintenance**: Clear temporary files and cache regularly

### Collaboration
1. **Share Results**: Export and share analysis findings with colleagues
2. **Document Methods**: Record analysis parameters and assumptions
3. **Version Control**: Keep track of different analysis iterations
4. **Feedback Loop**: Provide feedback for platform improvements

---

## Support and Resources

### Technical Support
- **Email**: support@mantra-marine.ai
- **Documentation**: Complete API and user documentation
- **Community Forum**: User community for questions and sharing
- **Training Materials**: Video tutorials and step-by-step guides

### Additional Resources
- **Scientific Literature**: References and citations for methods
- **Data Standards**: International marine data standards
- **Best Practices**: Guidelines for marine data analysis
- **Case Studies**: Real-world application examples

### Updates and Maintenance
- **Regular Updates**: Platform improvements and new features
- **Security Patches**: Regular security updates
- **Performance Optimization**: Continuous performance improvements
- **User Feedback**: Incorporation of user suggestions

---

*This user manual is regularly updated to reflect platform improvements and new features. For the latest version, please visit the official documentation portal.*

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Platform**: MANTRA Marine AI Platform
