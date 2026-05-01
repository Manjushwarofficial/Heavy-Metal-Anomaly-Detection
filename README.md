# Heavy Metal Anomaly Detection

## Objective
Detecting anomalies in geochemical data.

## Screenshots
<img width="1280" height="832" alt="Screenshot 2026-04-29 at 4 16 29 PM" src="https://github.com/user-attachments/assets/6b5c50b6-a04a-4f9c-8df9-68f96793f7bf" />
<br>
<img width="1780" height="491" alt="step1_raw_distributions" src="https://github.com/user-attachments/assets/2ca4861c-aadf-41b8-80af-5dddde951be2" />
<br>
<img width="1780" height="943" alt="step2_log_transformation" src="https://github.com/user-attachments/assets/69d6ecbc-93ef-4717-9c09-132af47c2c53" />
<br>
<img width="1540" height="590" alt="step3_boxplot_comparison" src="https://github.com/user-attachments/assets/8fa46f4b-3be7-4c27-9c54-a1c4b315fa92" />


## Geochemical Data Points of Karnataka and Andhra Pradesh (National Geochemical Mapping - NGCM)
Geochemical data points from Karnataka and Andhra Pradesh, collected by Geological Survey of India (GSI) under the National Geochemical Mapping (NGCM) program. The dataset includes multi-element stream sediment analytical data with major oxides (%) and trace elements (ppm and ppb) for 68 elements.

### About Dataset
This dataset contains elemental chemical values of stream sediment samples collected as part of the National Geochemical Mapping (NGCM) program by Geological Survey of India (GSI). Sampling follows a structured grid pattern of 1km × 1km within a toposheet, with composite samples representing a 2km × 2km grid. Additionally, one soil sample is collected from a 5’ × 5’ quadrant of a toposheet. The data includes multi-element analysis, covering major oxides in percentage and trace elements in parts per million (ppm) and parts per billion (ppb), making it a valuable resource for geochemical studies and mineral exploration.

### Dataset Metadata
- **License:** NA
- **Geographical Coverage:** 39,000 Sq Km area in Karnataka and Andhra Pradesh
- **Sector:** Chemical, Mining, and Natural Resources
- **Author:** Geological Survey of India (GSI)
- **Source Organisation:** GSI (Ministry of Mines)
- **Uploaded By:** P K Singh
- **Data Quality Score (Beta):** 3
- **Dataset Type:** Unstructured
- **Frequency:** NA
- **Time Granularity:** NA
- **Year Range:** NA
- **Date & Time:** 11/03/25 20:35:50
- **Visibility:** Open
- **Hosted / Redirected:** Hosted

### Activity Overview
- **Downloads:** 372
- **Views:** 1,491
- **File Size:** 18.55 MB

### Tags
- Geology
- Stream Sediments
- Geochemical

### Data Source
[Geochemical Data Points of Karnataka and Andhra Pradesh (NGCM)](https://aikosh.indiaai.gov.in/home/datasets/details/geochemical_data_points_of_karnataka_and_andhra_pradesh_national_geochemical_mapping_ngcm.html)

## Project Structure
```
Heavy-Metal-Anomaly-Detection/
├── data/
│   ├── Metadata NGCM.docx
│   ├── NGCM-Stream-Sediment-Analysis-Updated.xlsx
│   ├── NGCM_STREAM_SEDIMENTS_bkp.xlsx
│   └── stream_sediments_gcs_ngdr_20250221140319808/
│       ├── stream_sediments_gcs_ngdr.cpg
│       ├── stream_sediments_gcs_ngdr.dbf
│       ├── stream_sediments_gcs_ngdr.prj
│       ├── stream_sediments_gcs_ngdr.sbn
│       ├── stream_sediments_gcs_ngdr.sbx
│       ├── stream_sediments_gcs_ngdr.shp
│       └── stream_sediments_gcs_ngdr.shx
├── preprocessing.ipynb
├── preprocessingFinal.ipynb
├── vizualizer.py
├── README.md
├── .ipynb_checkpoints/
│   ├── preprocessing-checkpoint.ipynb
│   └── preprocessingFinal-checkpoint.ipynb
├── X_scaled_features.csv
├── coords.csv
├── preprocessed_combined.csv
├── anomalous_coordinates.csv
└── outputs/
    ├── step1_raw_distributions.png
    ├── step2_log_transformation.png
    ├── step3_robust_scaling.png
    ├── step3_boxplot_comparison.png
    └── correlation_matrix.png
```

## Features & Workflow

### 1. Data Preprocessing Pipeline
The preprocessing pipeline consists of four main steps:

| Step | Operation | Purpose |
|------|-----------|---------|
| **Step 1** | Data Isolation & Cleaning | Extract As_ppm, Pb_ppm, Hg_ppb; handle missing values |
| **Step 2** | Log Transformation | Apply `log1p()` to correct right-skewed geochemical distributions |
| **Step 3** | Robust Scaling | Normalize features using median & IQR (outlier-resistant) |
| **Step 4** | Coordinate Separation | Keep X/Y coordinates separate; re-attach after prediction for mapping |

**Key Chemical Features:**
- **As_ppm** (Arsenic) - Parts Per Million
- **Pb_ppm** (Lead) - Parts Per Million
- **Hg_ppb** (Mercury) - Parts Per Billion

**Coordinates:**
- **X** - Longitude
- **Y** - Latitude

### 2. Anomaly Detection Models
Two unsupervised learning models are implemented:

#### One-Class SVM
- **Kernel:** Radial Basis Function (RBF)
- **Gamma:** Auto-scaled
- **Nu Parameter:** Controls the expected fraction of anomalies (default 0.05 = 5%)
- **Advantage:** Effective for detecting outliers in high-dimensional feature space

#### Isolation Forest
- **Estimators:** 200 trees
- **Contamination:** Expected anomaly fraction (default 0.05 = 5%)
- **Random State:** 42 (reproducibility)
- **Advantage:** Fast, memory-efficient, works well with multivariate data

### 3. Output Files
The preprocessing pipeline generates:

- **X_scaled_features.csv** - Scaled chemical features (model input)
- **coords.csv** - Geographic coordinates
- **preprocessed_combined.csv** - Combined features + coordinates
- **anomalous_coordinates.csv** - Detected anomaly locations

Visualization outputs:
- **step1_raw_distributions.png** - Histogram of raw chemical distributions
- **step2_log_transformation.png** - Before/after log transformation comparison
- **step3_robust_scaling.png** - Scaling effect on feature ranges
- **step3_boxplot_comparison.png** - Scale dominance analysis
- **correlation_matrix.png** - Feature correlation heatmap

## Installation & Usage

### Prerequisites
```bash
python >= 3.8
pandas
numpy
scikit-learn
folium
PyQt5
PyQtWebEngine
matplotlib
seaborn
openpyxl
```

### Setup
```bash
# Clone or download the repository
cd Heavy-Metal-Anomaly-Detection

# Install dependencies
pip install pandas numpy scikit-learn folium PyQt5 PyQtWebEngine matplotlib seaborn openpyxl
```

### Step 1: Data Preprocessing
Run the preprocessing notebook to prepare the data:
```bash
jupyter notebook preprocessingFinal.ipynb
```

This generates:
- `X_scaled_features.csv` - Scaled features
- `coords.csv` - Coordinates
- `preprocessed_combined.csv` - Combined data
- Visualization plots (PNG files)

### Step 2: Launch Interactive Visualizer
Start the PyQt5 GUI for anomaly detection and visualization:
```bash
python vizualizer.py
```

**GUI Features:**
- Select anomaly detection model (One-Class SVM or Isolation Forest)
- Adjust contamination parameter (0.01 - 0.50)
- Run detection in real-time with progress updates
- View results in interactive table
- Generate interactive map with anomaly locations
- Export detected anomalies to CSV
- Toggle heatmap and clustering visualizations

## Results & Analysis

### Detection Output
The anomaly detection models produce:
- **Label:** -1 (anomaly) or +1 (normal)
- **Anomaly Flag:** Boolean indicating anomalous samples
- **Coordinates:** X (longitude), Y (latitude) for each detection

### Map Visualization
The interactive map displays:
- 🔵 **Light Blue Dots** - All normal samples
- 🔴 **Red Dots** - Detected anomalies
- **Heatmap Layer** (optional) - Anomaly density visualization
- **Cluster Layer** (optional) - Grouped anomaly markers

### Statistical Metrics
- **Total Samples:** Number of data points analyzed
- **Anomalies Detected:** Count of anomalous locations
- **Anomaly Rate:** Percentage of detected anomalies
- **Geographic Distribution:** Latitude/longitude ranges of anomalies

## Methodology

### Why Log Transformation?
Geochemical concentrations follow a **log-normal distribution**:
- Most samples have low concentrations (near-zero)
- Few samples show extreme high values
- Log transformation corrects right-skew, improving model performance

### Why RobustScaler?
- Scales features to comparable ranges
- Uses median & IQR (not affected by extreme outliers)
- Essential for distance-based algorithms like One-Class SVM
- Prevents feature dominance (Mercury would otherwise dominate due to high ppb values)

### Model Selection
- **One-Class SVM:** Better for complex boundary detection
- **Isolation Forest:** Faster, requires less tuning, better for high-dimensional data

## Key Algorithms

### One-Class SVM Training
```python
from sklearn.svm import OneClassSVM
model = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
model.fit(X_scaled)
predictions = model.predict(X_scaled)  # +1 (inlier) or -1 (anomaly)
```

### Isolation Forest Training
```python
from sklearn.ensemble import IsolationForest
model = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
model.fit(X_scaled)
predictions = model.predict(X_scaled)  # +1 (inlier) or -1 (anomaly)
```

## Applications

1. **Environmental Monitoring** - Identify areas with high heavy metal concentration
2. **Mineral Exploration** - Locate geochemical anomalies indicating ore deposits
3. **Pollution Assessment** - Map contaminated regions for remediation
4. **Geochemical Mapping** - Support geological survey and resource exploration
5. **Public Health** - Identify areas of potential health concern from metal contamination

## Parameter Tuning

### Contamination / Nu Parameter
- **Lower values (0.01-0.03):** Stricter anomaly detection
- **Mid values (0.04-0.06):** Balanced detection
- **Higher values (0.07-0.10):** More lenient, detects more anomalies

Recommendation: Start with **0.05** and adjust based on domain knowledge.

## Performance Considerations

- **Data Size:** Handles 1000+ samples efficiently
- **Computation Time:** < 1 second for typical NGCM dataset
- **Memory:** Minimal footprint, suitable for local machines
- **Scalability:** Can be adapted for larger datasets with distributed computing

## Interactive Visualizer (PyQt5 GUI)

### Overview
The **Heavy Metals Anomaly Visualizer** is a desktop application built with PyQt5 that provides an intuitive interface for anomaly detection and geospatial visualization.

### Main Features

#### 1. Model Configuration Panel
- **Model Selection:** Choose between One-Class SVM or Isolation Forest
- **Parameter Adjustment:** Fine-tune contamination/nu values (0.01 - 0.50)
- **Real-time Updates:** Monitor detection progress with visual feedback

#### 2. Detection Execution
- **Threading Support:** Models run in background threads, keeping UI responsive
- **Progress Tracking:** Real-time status updates during model training
- **Result Summary:** Instant display of detection statistics

#### 3. Results Display
- **Results Table:** Browse top 50 anomalies with coordinates
- **Statistical Tab:** Comprehensive analysis of detected anomalies
- **Map Visualization:** Interactive Folium map with anomaly markers

#### 4. Map Features
- **Base Layer:** OpenStreetMap for geographic reference
- **Normal Samples:** Light blue dots representing normal data points
- **Anomalies:** Bright red markers highlighting detected anomalies
- **Heatmap Layer:** Optional density visualization of anomaly concentrations
- **Marker Clustering:** Optional grouping for better visualization at different zoom levels
- **Center Auto-Detection:** Map automatically centers on study region

#### 5. Data Export
- **CSV Export:** Save detected anomalies with coordinates
- **Coordinate Preservation:** All geographic data retained for GIS integration
- **Quality Metadata:** Includes model type and anomaly flags

### Usage Workflow

```
1. Launch Visualizer
   └─> python vizualizer.py

2. Data Loading
   └─> Automatically loads X_scaled_features.csv and coords.csv

3. Select Model & Parameters
   ├─> Choose Model (One-Class SVM or Isolation Forest)
   └─> Adjust Contamination Parameter (default: 0.05)

4. Run Detection
   └─> Click "Run Anomaly Detection"
       ├─> Training executes in background
       ├─> Progress bar updates in real-time
       └─> Results display instantly

5. View Results
   ├─> Results Table: Browse detected anomalies
   ├─> Statistics: Analyze geographic distribution
   └─> Maps: Visualize anomalies on interactive map

6. Generate Map
   ├─> Click "Generate Map"
   ├─> Toggle heatmap and clustering options
   └─> Map opens in browser/viewer

7. Export Data
   └─> Click "Export Anomalies CSV"
       ├─> Select save location
       └─> CSV file with coordinates ready for GIS tools
```

### System Requirements for Visualizer
- **OS:** Windows, macOS, or Linux
- **Python:** 3.8 or higher
- **RAM:** 2 GB minimum (4 GB recommended)
- **Disk Space:** 500 MB for dependencies

### Troubleshooting

**Issue:** Module not found (pandas, PyQt5, etc.)
```bash
# Solution: Install missing dependencies
pip install --upgrade pandas numpy scikit-learn PyQt5 PyQtWebEngine folium matplotlib seaborn
```

**Issue:** Map not displaying
```bash
# Solution: Ensure folium and PyQtWebEngine are properly installed
pip install folium PyQtWebEngine --force-reinstall
```

**Issue:** Application freezes during detection
- This is expected during model training (background threading handles it)
- Wait for progress to complete

## Detailed Workflow

### Complete Analysis Pipeline

```
INPUT DATA (NGCM-Stream-Sediment-Analysis-Updated.xlsx)
    ↓
[PREPROCESSING STAGE]
    ├─ Step 1: Data Cleaning
    │   ├─ Extract As_ppm, Pb_ppm, Hg_ppb
    │   └─ Handle missing values
    ├─ Step 2: Log Transformation
    │   └─ Apply log1p() for distribution normalization
    ├─ Step 3: Robust Scaling
    │   └─ Normalize to [0, 1] using RobustScaler
    └─ Step 4: Coordinate Separation
        ├─ Store X, Y separately
        └─ Generate CSV outputs
    ↓
OUTPUT ARTIFACTS
    ├─ X_scaled_features.csv (model input)
    ├─ coords.csv (coordinates store)
    ├─ preprocessed_combined.csv (inspection data)
    └─ Visualization plots (PNG)
    ↓
[ANOMALY DETECTION STAGE]
    ├─ Load scaled features
    ├─ Load coordinates
    ├─ Select Model
    │   ├─ One-Class SVM (RBF kernel)
    │   └─ Isolation Forest (n_estimators=200)
    ├─ Fit Model
    └─ Generate Predictions
    ↓
PREDICTION LABELS
    ├─ -1 → Anomaly
    └─ +1 → Normal
    ↓
[VISUALIZATION & EXPORT STAGE]
    ├─ Merge coordinates with predictions
    ├─ Create interactive map
    │   ├─ Display normal points (blue)
    │   ├─ Display anomalies (red)
    │   ├─ Add heatmap layer
    │   └─ Add clustering layer
    ├─ Display statistics
    └─ Export anomalies to CSV
    ↓
FINAL OUTPUT
    ├─ anomalous_coordinates.csv
    ├─ Interactive HTML map
    ├─ Statistical report
    └─ GIS-ready coordinate data
```

## Dataset Characteristics

### Sample Statistics
- **Total Samples:** 1000+
- **Study Area:** 39,000 sq km (Karnataka & Andhra Pradesh)
- **Grid Resolution:** 1km × 1km
- **Elements Analyzed:** 68 multi-element components

### Chemical Element Units
- **Major Oxides:** Percentage (%)
- **Trace Elements (ppm):** As, Pb, and others
- **Trace Elements (ppb):** Hg and others

### Data Quality
- **Missing Values:** Handled via dropping or median imputation
- **Outliers:** Managed through RobustScaler
- **Distribution:** Log-normal (corrected via log1p)

## Advanced Configuration

### Modifying Model Parameters

**One-Class SVM Customization:**
```python
# In preprocessingFinal.ipynb or vizualizer.py
oc_svm = OneClassSVM(
    kernel='rbf',      # or 'poly', 'sigmoid', 'linear'
    gamma='scale',     # auto-scale or specify value
    nu=0.05           # tune based on expected anomaly rate
)
```

**Isolation Forest Customization:**
```python
iso_forest = IsolationForest(
    n_estimators=200,     # increase for complex patterns
    contamination=0.05,   # expected anomaly rate
    random_state=42,      # for reproducibility
    n_jobs=-1            # parallel processing
)
```

## Contributing

To extend this project:

1. **Add New Models:** Implement additional anomaly detection algorithms
2. **Enhance Visualization:** Add more map layers or statistical plots
3. **Improve Preprocessing:** Optimize feature engineering or add new transformations
4. **Scale Infrastructure:** Adapt for distributed processing of larger datasets

## References

- Geological Survey of India (GSI) - National Geochemical Mapping Program
- Scikit-learn Documentation: One-Class SVM, Isolation Forest
- Folium Documentation: Interactive maps with Python
- PyQt5 Documentation: Desktop GUI development
- National AI Office (AIKosh): [Data Repository](https://aikosh.indiaai.gov.in)

## License
NA

## Author
Heavy Metal Anomaly Detection Project Team

## Version
1.0.0

## Last Updated
March 2025
