# Heavy Metal Anomaly Detection

## Objective
Detecting anomalies in geochemical data.

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
├── README.md
└── .ipynb_checkpoints/
    ├── preprocessing-checkpoint.ipynb
    └── preprocessingFinal-checkpoint.ipynb
```