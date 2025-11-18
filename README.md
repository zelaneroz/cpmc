# West Side Market Survey Data Pipeline

This repository contains the data processing pipeline developed by Zelan Eroz Espanto (yours truly) as part of the ongoing research effort at the West Side Market. The project builds on a previous 2022 survey and supports the new 2024–2025 survey initiative aimed at understanding customer demographics, visit behavior, sentiment, and engagement opportunities for the Market.

The notebook in this repository (`.ipynb`) is responsible for end-to-end cleaning, preprocessing, and transformation of raw survey data into analysis-ready outputs. This pipeline supports downstream tasks such as segmentation, frequency analysis, sentiment extraction, and the creation of datasets used for visualization and reporting.

## Contents

* **Data Cleaning:** Standardization, missing-value handling, and normalization of categorical and numeric fields.
* **Feature Engineering:** Construction of variables for visit frequency, reasoning of visit, sentiment categories, and notable experience tagging.
* **Aggregation & Outputs:** Summaries used to inform market insights, customer segment profiles, and recommendations for future engagement strategies.
* **Reproducibility:** All steps are contained in the notebook for transparent and repeatable processing.

## Usage

Open the notebook in Jupyter or VS Code and run the cells in order. The pipeline assumes raw survey data is stored in the main directory and is called `survey.csv`, and processed outputs will be generated in `processed/`.

## Project Context

This work contributes to CPMC’s broader initiative to assess public perceptions of the West Side Market. Insights generated with this pipeline help inform operational planning, vendor engagement, customer outreach, and potential programming such as live events, digital engagement strategies, and improvements to cleanliness, parking, and accessibility.

## License
This project is for academic and research purposes through the XLab Program at Case Western Reserve University's Weatherhead School of Management.
