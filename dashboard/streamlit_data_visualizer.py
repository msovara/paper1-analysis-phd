#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Data Visualization Dashboard

Interactive dashboard for visualizing climate data inputs including:
- DMI (Dipole Mode Index) data
- NINO34 data
- Drought indices
- Time series analysis

Author: Mthetho Sovara
Date: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

REPO_ROOT = Path(__file__).resolve().parent.parent

# Page configuration
st.set_page_config(
    page_title="Climate Data Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_csv_file(file_path):
    """Load CSV file with caching"""
    try:
        # Try different separators and encodings
        df = pd.read_csv(file_path, index_col=0, parse_dates=True, 
                        infer_datetime_format=True, low_memory=False)
        return df
    except:
        try:
            df = pd.read_csv(file_path, sep=',', index_col=0, parse_dates=True)
            return df
        except:
            df = pd.read_csv(file_path)
            return df

def detect_date_column(df):
    """Detect date column in dataframe"""
    date_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col].iloc[0:5])
                date_cols.append(col)
            except:
                pass
    return date_cols

def clean_data(df):
    """Clean data by removing missing values and handling special cases"""
    # Replace common missing value indicators
    df = df.replace([-99.99, -9999.0, -9999, 'missing', 'NaN', 'nan'], np.nan)
    
    # Remove rows with all NaN
    df = df.dropna(how='all')
    
    # Convert numeric columns
    for col in df.select_dtypes(include=['object']).columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    
    return df

def create_time_series_plot(df, x_col, y_cols, title="Time Series"):
    """Create interactive time series plot"""
    fig = go.Figure()
    
    for col in y_cols:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df[x_col] if x_col else df.index,
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2),
                hovertemplate=f'<b>{col}</b><br>' +
                            'Date: %{x}<br>' +
                            'Value: %{y:.3f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col if x_col else 'Date',
        yaxis_title='Value',
        hovermode='x unified',
        height=500,
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_scatter_plot(df, x_col, y_col, color_col=None, title="Scatter Plot"):
    """Create interactive scatter plot"""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col if color_col else None,
        title=title,
        hover_data=[df.index] if isinstance(df.index, pd.DatetimeIndex) else None,
        labels={x_col: x_col, y_col: y_col}
    )
    
    fig.update_traces(marker=dict(size=8, opacity=0.6))
    fig.update_layout(height=500, template='plotly_white')
    
    return fig

def create_histogram(df, col, title="Distribution"):
    """Create histogram"""
    fig = px.histogram(
        df,
        x=col,
        nbins=50,
        title=title,
        labels={col: col}
    )
    fig.update_layout(height=400, template='plotly_white')
    return fig

def create_correlation_heatmap(df, numeric_cols):
    """Create correlation heatmap"""
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Correlation Matrix",
        height=600,
        template='plotly_white'
    )
    
    return fig

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Climate Data Visualization Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar for file selection
    st.sidebar.header("📁 Data Input")
    
    # Option 1: Upload file
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type=['csv'],
        help="Upload a CSV file to visualize"
    )
    
    # Option 2: Select from existing files
    st.sidebar.subheader("Or Select Existing File")
    existing_files = [
        "nino34.long.anom.csv",
        "dmi_son_top_events.csv",
        "dmi_son_annual_averages.csv"
    ]
    
    selected_file = st.sidebar.selectbox(
        "Select file",
        ["None"] + existing_files
    )
    
    # Load data
    df = None
    file_name = None
    
    if uploaded_file is not None:
        df = load_csv_file(uploaded_file)
        file_name = uploaded_file.name
        st.sidebar.success(f"✅ Loaded: {file_name}")
    elif selected_file != "None":
        file_path = REPO_ROOT / selected_file
        if file_path.exists():
            df = load_csv_file(file_path)
            file_name = selected_file
            st.sidebar.success(f"✅ Loaded: {file_name}")
        else:
            st.sidebar.error(f"❌ File not found: {selected_file}")
    
    if df is not None:
        # Clean data
        df = clean_data(df)
        
        # Main content area
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview", 
            "📊 Time Series", 
            "🔍 Analysis", 
            "📉 Statistics",
            "⚙️ Data Info"
        ])
        
        with tab1:
            st.header("Data Overview")
            
            # Display basic info
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                st.metric("Numeric Columns", len(numeric_cols))
            with col4:
                missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                st.metric("Missing Data", f"{missing_pct:.1f}%")
            
            # Display first few rows
            st.subheader("Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Quick statistics
            if numeric_cols:
                st.subheader("Quick Statistics")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
        with tab2:
            st.header("Time Series Visualization")
            
            # Get date column
            date_cols = detect_date_column(df)
            if isinstance(df.index, pd.DatetimeIndex):
                x_col = None  # Use index
                date_info = "Using index as date"
            elif date_cols:
                x_col = st.selectbox("Select date column", date_cols, key="date_col")
                date_info = f"Using column: {x_col}"
            else:
                x_col = None
                date_info = "No date column detected - using row numbers"
            
            st.info(f"📅 {date_info}")
            
            # Select columns to plot
            if numeric_cols:
                selected_cols = st.multiselect(
                    "Select columns to visualize",
                    numeric_cols,
                    default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
                    key="ts_cols"
                )
                
                if selected_cols:
                    # Time series plot
                    fig = create_time_series_plot(df, x_col, selected_cols, 
                                                  title=f"Time Series: {', '.join(selected_cols)}")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Optional: Add moving average
                    if st.checkbox("Show moving average", key="ma_check"):
                        window = st.slider("Moving average window", 3, 24, 6, key="ma_window")
                        
                        fig_ma = go.Figure()
                        for col in selected_cols:
                            if col in df.columns:
                                # Original data
                                fig_ma.add_trace(go.Scatter(
                                    x=df[x_col] if x_col else df.index,
                                    y=df[col],
                                    mode='lines',
                                    name=f'{col} (Original)',
                                    line=dict(width=1, color='lightblue'),
                                    opacity=0.5
                                ))
                                
                                # Moving average
                                ma = df[col].rolling(window=window).mean()
                                fig_ma.add_trace(go.Scatter(
                                    x=df[x_col] if x_col else df.index,
                                    y=ma,
                                    mode='lines',
                                    name=f'{col} (MA-{window})',
                                    line=dict(width=2)
                                ))
                        
                        fig_ma.update_layout(
                            title=f"Time Series with Moving Average (window={window})",
                            xaxis_title=x_col if x_col else 'Date',
                            yaxis_title='Value',
                            height=500,
                            template='plotly_white',
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_ma, use_container_width=True)
            else:
                st.warning("No numeric columns found for time series visualization")
        
        with tab3:
            st.header("Data Analysis")
            
            if len(numeric_cols) >= 2:
                # Scatter plot
                st.subheader("Scatter Plot")
                col1, col2 = st.columns(2)
                
                with col1:
                    x_var = st.selectbox("X-axis variable", numeric_cols, key="scatter_x")
                with col2:
                    y_var = st.selectbox("Y-axis variable", numeric_cols, 
                                        index=1 if len(numeric_cols) > 1 else 0, key="scatter_y")
                
                if x_var != y_var:
                    color_var = st.selectbox(
                        "Color by (optional)", 
                        ["None"] + numeric_cols,
                        key="scatter_color"
                    )
                    
                    fig_scatter = create_scatter_plot(
                        df, x_var, y_var, 
                        color_var if color_var != "None" else None,
                        f"Scatter: {y_var} vs {x_var}"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    # Calculate correlation
                    if x_var in df.columns and y_var in df.columns:
                        corr = df[[x_var, y_var]].corr().iloc[0, 1]
                        st.info(f"📊 Correlation coefficient: {corr:.3f}")
                
                # Correlation heatmap
                if len(numeric_cols) > 1:
                    st.subheader("Correlation Matrix")
                    selected_numeric = st.multiselect(
                        "Select columns for correlation",
                        numeric_cols,
                        default=numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols,
                        key="corr_cols"
                    )
                    
                    if len(selected_numeric) > 1:
                        fig_corr = create_correlation_heatmap(df, selected_numeric)
                        st.plotly_chart(fig_corr, use_container_width=True)
            
            # Distribution plots
            if numeric_cols:
                st.subheader("Distribution Analysis")
                dist_col = st.selectbox("Select column for distribution", numeric_cols, key="dist_col")
                
                fig_hist = create_histogram(df, dist_col, f"Distribution of {dist_col}")
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with tab4:
            st.header("Statistical Summary")
            
            if numeric_cols:
                # Detailed statistics
                st.subheader("Descriptive Statistics")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                
                # Additional statistics
                st.subheader("Additional Statistics")
                
                stats_data = []
                for col in numeric_cols:
                    stats_data.append({
                        'Column': col,
                        'Mean': df[col].mean(),
                        'Median': df[col].median(),
                        'Std Dev': df[col].std(),
                        'Min': df[col].min(),
                        'Max': df[col].max(),
                        'Skewness': df[col].skew(),
                        'Kurtosis': df[col].kurtosis(),
                        'Missing': df[col].isnull().sum()
                    })
                
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, use_container_width=True)
                
                # Download statistics
                csv_stats = stats_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Statistics",
                    data=csv_stats,
                    file_name=f"{file_name}_statistics.csv",
                    mime="text/csv"
                )
        
        with tab5:
            st.header("Data Information")
            
            # Data types
            st.subheader("Data Types")
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': [str(dtype) for dtype in df.dtypes],
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values
            })
            st.dataframe(dtype_df, use_container_width=True)
            
            # Memory usage
            st.subheader("Memory Usage")
            memory_usage = df.memory_usage(deep=True).sum() / 1024**2  # MB
            st.info(f"Total memory usage: {memory_usage:.2f} MB")
            
            # Data shape
            st.subheader("Data Shape")
            st.write(f"Rows: {df.shape[0]}")
            st.write(f"Columns: {df.shape[1]}")
            
            # Download data
            st.subheader("Download Data")
            csv_data = df.to_csv()
            st.download_button(
                label="📥 Download Full Dataset",
                data=csv_data,
                file_name=f"{file_name}_processed.csv",
                mime="text/csv"
            )
    
    else:
        # Welcome message when no data is loaded
        st.info("👈 Please upload a CSV file or select an existing file from the sidebar to get started.")
        
        # Show example of what the app can do
        st.markdown("""
        ### Features:
        - 📊 **Time Series Visualization**: Interactive plots with multiple variables
        - 🔍 **Data Analysis**: Scatter plots, correlation matrices, and distributions
        - 📉 **Statistical Summary**: Comprehensive statistics and data insights
        - ⚙️ **Data Information**: Data types, memory usage, and metadata
        - 📥 **Export Options**: Download processed data and statistics
        
        ### Supported Data Formats:
        - CSV files with time series data
        - Date columns (auto-detected)
        - Multiple numeric variables
        """)

if __name__ == "__main__":
    main()

