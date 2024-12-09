# Interactive Hackathon Data Explorer

## Overview

The Interactive Hackathon Data Explorer is a Streamlit-based application designed for Hackathon participants to upload, process, and visualize large datasets efficiently. This tool is particularly useful for analyzing, visualizing results, and exploring metrics to gain insights and make data-driven decisions.

## Key Features

- **Data Loading**: Supports uploading CSV and Parquet files.
- **Data Preprocessing**: Automatically fills missing values and preprocesses data for analysis.
- **Data Sampling**: Samples a subset of the data for efficient visualization.
- **Dynamic Visualization Suggestions**: Suggests suitable visualization types based on data types.
- **Interactive Visualizations**: Allows users to select and customize visualizations using Plotly.
- **Geographic Visualization**: Supports geographic data visualization for datasets containing a 'state' column.

## Best Use Cases

- **Patient Data Analysis**: Analyze patient data to identify trends, patterns, and outliers.
- **Medical Research**: Visualize medical research results to gain insights and support findings.
- **Healthcare Metrics**: Explore healthcare metrics to monitor performance and make data-driven decisions.

## Installation

### Prerequisites

- Python 3.7 or later
- Pip (Python package installer)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mohitkothari-dev/Interactive-Hackathon-Data-Explorer
   cd Interactive-Hackathon-Data-Explorer

2. **Install Requirements file**:
   ```bash
   pip install -r requirements.txt

3. **Run Streamlit app**:
   ```bash
   streamlit run main.py