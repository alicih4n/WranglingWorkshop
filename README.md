# Lab 3: Data Engineering & EDA - Wrangling Workshop

**Student:** Ali Cihan Ozdemir (9091405)
**Group Partner:** Roshan (Absent/Did not contribute to this submission)
**Course:** PROG8245 - Data Engineering
**Repository:** [WranglingWorkshop](https://github.com/alicih4n/WranglingWorkshop.git)  

---

## Overview
This repository contains the deliverables for Lab 3, focusing on simulating a real-world Data Engineering pipeline. The project involves:
1.  **Cloud Database Integration**: Creating and managing a PostgreSQL database on Neon.
2.  **Synthetic Data Generation (SDG)**: Creating a "dirty" dataset to mimic real-world data quality issues.
3.  **Data Wrangling & Cleaning**: Using Pandas to inspect, clean, and impute missing data.
4.  **Advanced Visualization**: Generating insights using Seaborn and Matplotlib.

## Repository Structure
- `lab3_sdg.py`: Python script to generate synthetic employee data and upload it to the Neon DB.
- `Lab3_DataEngineering.ipynb`: Main Jupyter Notebook containing the analysis, cleaning, and visualizations.
- `requirements.txt`: List of Python dependencies.
- `README.md`: Project documentation.
- `create_submission_pdf.py`: Script to generate the submission PDF.

## Setup & Usage

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Generate Data:**
    Run the SDG script to populate the cloud database (if not already populated):
    ```bash
    python lab3_sdg.py
    ```

3.  **Run Analysis:**
    Open `Lab3_DataEngineering.ipynb` in Jupyter Lab or VS Code to view the data engineering process and insights.
    **Note:** Ensure you restart the kernel and run all cells to fetch the freshest data from the database.

## Project Highlights
- **Dirty Data Simulation**: 20% of generated records contain missing names, salaries, or logical errors (dates < 2015).
- **Z-Score Scaling**: Implementation of standard scaling to prepare data for neural network compatibility.
- **SQL-Style Joins**: Merging employee data with a synthetic `departments` table for deeper analytics.
