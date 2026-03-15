# Measuring Transfer Friction and Temporal Inequity in Chennai’s Multimodal Public Transport Network

This repository contains the data processing pipeline and analytical scripts developed to evaluate the temporal inequity and transfer friction across Chennai's multimodal transit network (Metro, MTC Bus, and Suburban Rail).

## Overview
Urban public transport planning often emphasizes spatial connectivity while overlooking the temporal experience of passengers during intermodal transfers. This project builds a **Time-Expanded Multimodal Network** from raw GTFS schedules to explicitly measure waiting times, accurate gate-to-gate walking penalties, and missed connection probabilities.

The core metric developed is the **Transfer Friction Index (TFI)**, which distinguishes between **Peak and Off-Peak** hours to identify inequitable spatial distributions of transit burden.

## Data Sources
- **GTFS Static Data**: Schedule data filtered explicitly for **Weekday Services** for CMRL, MTC, and Southern Railway.
- **Spatial Data**: Precise **GeoJSON Entry/Exit Station Gates** combined with bus stop coordinates to accurately map physical walk transfer distances.

## Analytical Pipeline & Scripts

### 1. `data_ingestion.py`
**Actions:** Standardizes GTFS feeds. Merges `stops.txt` and parses `calendar.txt` to strictly filter 1.7 million stop-times down to **Weekday-only** schedules to ensure highly accurate frequency approximations.

### 2. `network_builder.py`
**Actions:** Constructs the spatial transfer topology by loading precise **Metro and Suburban Entry/Exit Polygons**. It snaps station geometries to these physical gates, ensuring the ~8,000 walkable transfer edges (≤500m) accurately reflect gate-to-gate impedance rather than center-to-center.

### 3. `graph_analysis.py`
**Actions:** Builds a Directed Topologic Graph and computes **Betweenness Centrality**.
*Finding: Government Estate/Omandurar, Guindy, and Mambalam serve as the most critical backbone hubs.*

### 4. `tfi_calculator.py`
**Actions:** Computes the **Transfer Friction Index (TFI)** by segmenting temporal schedules into **Peak Hours (08:00-10:00 & 17:00-19:00)** and Off-Peak hours. 
*Finding: VOC Nagar, Veppampattu, and Pattaravakkam endure massive peak-time friction penalties climbing up to 90 minutes per transfer.*

### 5. `hotspot_analysis.py` & `inequity_analysis.py`
**Actions:** Merges quantitative TFI scores geographically to identify spatial segregation, calculating the Gini Coefficient. 
*Finding: A network Peak Gini Coefficient of 0.185. Peripheral zones (South and North) suffer disproportionately higher peak transfer frictions compared to the Central Core. Transfers originating from Suburban nodes suffer severe off-peak instability.*

### 6. `policy_simulation.py`
**Actions:** Simulates the reduction of TFI via Scenario A (Timetable Sync / Schedule Capping) vs Scenario B (Physical Walkway FOB Improvements).
*Finding: When walk distances are accurately mapped to gates, infrastructural FOBs show excellent base reductions. However, alleviating the extreme peripheral wait-time penalties discovered still mandates joint timetable integration.*
