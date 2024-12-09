import streamlit as st
import pandas as pd
import plotly.express as px
import pyarrow.parquet as pq
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# Function to load data with caching
@st.cache_data
def load_data(file):
    st.write(f"Loading file: {file.name}")
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.parquet'):
        df = pq.read_table(file).to_pandas()
    else:
        st.error("Unsupported file format. Please upload a CSV or Parquet file.")
        return None
    st.write(f"File loaded successfully with shape: {df.shape}")
    return df

# Function to preprocess data with caching
@st.cache_data
def preprocess_data(df):
    st.write("Preprocessing data...")
    # Fill missing values with a default value (e.g., 0 for numeric columns, empty string for object columns)
    df_filled = df.fillna({col: 0 if df[col].dtype in [int, float] else '' for col in df.columns})
    st.write(f"Data preprocessed successfully with shape: {df_filled.shape}")
    return df_filled

# Function to sample data
@st.cache_data
def sample_data(df, sample_size=10000):
    st.write(f"Sampling data to {sample_size} rows...")
    sampled_df = df.sample(n=sample_size, random_state=42)
    st.write(f"Data sampled successfully with shape: {sampled_df.shape}")
    return sampled_df

# Function to suggest visualizations based on data types
def suggest_visualizations(df):
    suggestions = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            suggestions.append("Histogram")
            suggestions.append("Box")
            suggestions.append("Violin")
        if pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            suggestions.append("Bar")
            suggestions.append("Pie")
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            suggestions.append("Line")
            suggestions.append("Area")
    # Ensure unique suggestions
    suggestions = list(set(suggestions))
    return suggestions

# Streamlit interface
st.title("Interactive Hackathon Data Explorer")
st.markdown("""
    <style>
    .main .block-container{
        max-width: 90%;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("Upload your CSV or Parquet files", accept_multiple_files=True)

if uploaded_files:
    data_frames = []
    for file in uploaded_files:
        df = load_data(file)
        if df is not None:
            df = preprocess_data(df)
            data_frames.append(df)

    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        st.write(f"Combined DataFrame shape: {combined_df.shape}")

        # Sample the data for visualization
        sampled_df = sample_data(combined_df)

        # Display the sampled dataframe using AgGrid for better performance
        st.write("Sampled DataFrame")
        gb = GridOptionsBuilder.from_dataframe(sampled_df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # Enable multi-row selection
        gridOptions = gb.build()
        AgGrid(sampled_df, gridOptions=gridOptions, update_mode=GridUpdateMode.MODEL_CHANGED)

        # Filtering options
        st.sidebar.title("Filter Options")
        columns = sampled_df.columns.tolist()
        selected_columns = st.sidebar.multiselect("Select columns to display", columns, default=columns)  # Default to all columns
        filtered_df = sampled_df[selected_columns]

        # Suggest visualizations based on data types
        suggested_visualizations = suggest_visualizations(filtered_df)

        # Geographic visualization
        if 'state' in filtered_df.columns:
            st.sidebar.title("Geographic Visualization")
            state_column = 'state'
            metric_column = st.sidebar.selectbox("Select metric for geographic visualization", filtered_df.columns)
            fig = px.choropleth(filtered_df,
                                locations=state_column,
                                locationmode="USA-states",
                                color=metric_column,
                                hover_name=state_column,
                                color_continuous_scale="Viridis",
                                scope="usa",
                                labels={metric_column: metric_column})
            st.plotly_chart(fig)

        # Custom visualizations
        st.sidebar.title("Custom Visualizations")
        plot_type = st.sidebar.selectbox("Select plot type", suggested_visualizations)
        x_axis = st.sidebar.selectbox("Select X-axis", filtered_df.columns)
        y_axis = st.sidebar.selectbox("Select Y-axis", filtered_df.columns)

        if plot_type == "Scatter":
            fig = px.scatter(filtered_df, x=x_axis, y=y_axis)
        elif plot_type == "Bar":
            fig = px.bar(filtered_df, x=x_axis, y=y_axis)
        elif plot_type == "Line":
            fig = px.line(filtered_df, x=x_axis, y=y_axis)
        elif plot_type == "Histogram":
            fig = px.histogram(filtered_df, x=x_axis)
        elif plot_type == "Box":
            fig = px.box(filtered_df, x=x_axis, y=y_axis)
        elif plot_type == "Heatmap":
            fig = px.imshow(filtered_df.corr())
        elif plot_type == "Pie":
            fig = px.pie(filtered_df, names=x_axis, values=y_axis)
        elif plot_type == "Area":
            fig = px.area(filtered_df, x=x_axis, y=y_axis)
        elif plot_type == "Violin":
            fig = px.violin(filtered_df, x=x_axis, y=y_axis)

        st.plotly_chart(fig)
    else:
        st.error("No valid data files were uploaded.")
else:
    st.info("Please upload CSV or Parquet files to get started.")
