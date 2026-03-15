# Transfer Friction & Temporal Inequity in Chennai's Multimodal Public Transport Network

**Bachelor's Thesis | B.Plan Final Year (2022–26)**
**SPA Vijayawada**
**Author: Bharat Oraon (Roll No. 2220200359)**

---

## 📌 Project Overview

This research focuses on measuring, mapping, and explaining the extent of **transfer friction** and **temporal inequity** within Chennai's multimodal public transport network. While conventional planning often focuses on spatial network expansion, this thesis shifts the lens to the **temporal experience of passengers** during intermodal transfers (switching between Metro, Bus, and Suburban Rail).

Transfer nodes are often the weakest links in the transit chain. Schedule misalignment between independently operated agencies (CMRL, MTC, Southern Railway) creates invisible time penalties that disproportionately affect transit-dependent commuters, especially in the city's periphery.

## 🚀 Key Objectives

1.  **Transfer Friction Index (TFI)**: Develop a computation-ready metric integrating walk time, wait time, and missed connection probability.
2.  **Time-Expanded Multimodal Network**: Build a network model incorporating exact gate-to-gate walk impedance for Chennai.
3.  **Spatial & Temporal Analysis**: Evaluate how transfer friction varies geographically and between Peak vs. Off-Peak periods.
4.  **Equity Assessment**: Link transfer friction distribution to demographic vulnerability across Chennai's 200 wards.
5.  **Policy Simulation**: Model potential TFI reductions through operational interventions like timetable synchronization and physical infrastructure improvements.

## 📊 Core Findings

-   **Operational vs. Infrastructural**: Transfer inefficiencies are primarily operational. Timetable synchronization alone can reduce average TFI by up to **40%**, significantly more than the gains from physical construction.
-   **Structural Inequity**: Peripheral suburban nodes (e.g., VOC Nagar, Veppampattu) carry a transfer burden nearly **3x** that of central core nodes.
-   **Rail-Bus Mode Gap**: Suburban Rail transfers exhibit the highest friction due to infrequent off-peak headways (45–90 min).

## 📂 Repository Structure

-   `Chennai/`: GIS data and spatial layers for the study area.
-   `Data/`: Processed datasets and computational outputs.
-   `Literature-Study/`: Background research and literature review synthesis.
-   `methodology.html`: Detailed breakdown of the six-stage computational pipeline.
-   `Results.html`: Visualization of key findings and spatial mapping.
-   `TFI_formula_logic.html`: Mathematical derivation and calculation logic for the Transfer Friction Index.
-   `Full_thesis_content.html`: Single-sheet reference for all thesis sections.
-   `Research_design_framework.html`: Overview of the research framework and methodology.
-   `Thesis Topic & Abstract.pdf`: Summary and scope of the research.
-   `fix_enrichment.py`: Automation script for KML attributes injection.

## 📊 Demographic Data Integration

The Chennai Ward Map has been enriched with 2011 Census demographic data for Wards 1–155.

### Data Sources
1.  **2011 District Census Handbook (Part B)**: SC/ST population, Literacy, and Worker statistics.
2.  **Demographic Profile Chennai (CSV)**: Age-wise population cohorts and gender split.

### Enriched KML Attributes
The `chennai_wards_enriched.kml` file now includes:
-   `Total_Pop`, `Male_Pop`, `Female_Pop`
-   `SC_Pop`, `ST_Pop`
-   `Literates`, `Total_Workers`
-   `Area_sqkm`
-   Age Cohorts: `Pop_0_14`, `Pop_15_24`, `Pop_25_60`, `Pop_60_plus`

## 🛠 Methodology

The research utilizes a six-stage computational pipeline:
1.  **Data Ingestion**: Standardizing GTFS feeds from CMRL, MTC, and Southern Railway.
2.  **Network Builder**: Using GeoJSON gate polygons for accurate gate-to-gate walk impedance.
3.  **Graph Analysis**: Identifying critical backbone interchange hubs via Betweenness Centrality.
4.  **TFI Calculator**: Computing the Transfer Friction Index across the network.
5.  **Inequity Analysis**: Calculating Gini coefficients for TFI distribution.
6.  **Policy Simulation**: Modeling impact projections for various intervention scenarios.

---

### 🎓 Academic Context
This project was completed as part of the B.Plan (Bachelor of Planning) final year thesis at the **School of Planning and Architecture (SPA), Vijayawada**.
