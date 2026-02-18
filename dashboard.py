"""
Aadhaar Enrollment Analytics Dashboard
Interactive dashboard to analyze and visualize Aadhaar enrollment patterns, demographics, and trends across India.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Aadhaar Enrollment Analytics",
    page_icon="🆔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the enrollment data"""
    try:
        df = pd.read_csv('sample_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run generate_data.py first.")
        st.stop()

def calculate_metrics(df):
    """Calculate key metrics from the data"""
    total_enrollments = df['total_enrollments'].sum()
    avg_daily = df.groupby('date')['total_enrollments'].sum().mean()
    total_states = df['state'].nunique()
    total_days = df['date'].nunique()
    
    return {
        'total_enrollments': total_enrollments,
        'avg_daily': avg_daily,
        'total_states': total_states,
        'total_days': total_days
    }

def plot_time_series(df, freq='D'):
    """Plot time series of enrollments"""
    if freq == 'D':
        daily = df.groupby('date')['total_enrollments'].sum().reset_index()
        fig = px.line(daily, x='date', y='total_enrollments',
                     title='Daily Enrollment Trends',
                     labels={'date': 'Date', 'total_enrollments': 'Total Enrollments'})
    else:  # Monthly
        df['month'] = df['date'].dt.to_period('M').astype(str)
        monthly = df.groupby('month')['total_enrollments'].sum().reset_index()
        fig = px.bar(monthly, x='month', y='total_enrollments',
                    title='Monthly Enrollment Trends',
                    labels={'month': 'Month', 'total_enrollments': 'Total Enrollments'})
    
    fig.update_layout(height=400, hovermode='x unified')
    return fig

def plot_state_comparison(df, top_n=10):
    """Plot top states by enrollment"""
    state_totals = df.groupby('state')['total_enrollments'].sum().sort_values(ascending=False).head(top_n)
    fig = px.bar(state_totals, x=state_totals.values, y=state_totals.index,
                orientation='h',
                title=f'Top {top_n} States by Total Enrollments',
                labels={'x': 'Total Enrollments', 'y': 'State'})
    fig.update_layout(height=500)
    return fig

def plot_demographics(df):
    """Plot demographic breakdown"""
    gender_data = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Enrollments': [df['male_enrollments'].sum(), df['female_enrollments'].sum()]
    })
    
    age_data = pd.DataFrame({
        'Age Group': ['Children (0-18)', 'Adults (19-60)', 'Seniors (60+)'],
        'Enrollments': [
            df['child_enrollments'].sum(),
            df['adult_enrollments'].sum(),
            df['senior_enrollments'].sum()
        ]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.pie(gender_data, values='Enrollments', names='Gender',
                     title='Gender Distribution',
                     color_discrete_sequence=['#1f77b4', '#ff7f0e'])
        fig1.update_layout(height=350)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.pie(age_data, values='Enrollments', names='Age Group',
                     title='Age Group Distribution',
                     color_discrete_sequence=['#2ca02c', '#d62728', '#9467bd'])
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)

def plot_seasonal_patterns(df):
    """Plot seasonal enrollment patterns"""
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    monthly_avg = df.groupby(['month', 'month_name'])['total_enrollments'].mean().reset_index()
    monthly_avg = monthly_avg.sort_values('month')
    
    fig = px.line(monthly_avg, x='month_name', y='total_enrollments',
                 title='Average Enrollments by Month (Seasonal Patterns)',
                 labels={'month_name': 'Month', 'total_enrollments': 'Average Daily Enrollments'},
                 markers=True)
    fig.update_layout(height=400, xaxis_tickangle=-45)
    return fig

def plot_center_type_distribution(df):
    """Plot distribution by center type"""
    center_data = df.groupby('center_type')['total_enrollments'].sum().reset_index()
    fig = px.pie(center_data, values='total_enrollments', names='center_type',
                title='Enrollments by Center Type',
                color_discrete_sequence=['#17a2b8', '#ffc107'])
    fig.update_layout(height=350)
    return fig

def generate_insights(df, metrics):
    """Generate actionable insights"""
    insights = []
    
    # Top performing state
    top_state = df.groupby('state')['total_enrollments'].sum().idxmax()
    top_state_count = df.groupby('state')['total_enrollments'].sum().max()
    insights.append(f"🏆 **Top Performing State**: {top_state} with {top_state_count:,} enrollments")
    
    # Gender ratio
    male_pct = (df['male_enrollments'].sum() / df['total_enrollments'].sum()) * 100
    female_pct = 100 - male_pct
    insights.append(f"👥 **Gender Distribution**: Male {male_pct:.1f}% | Female {female_pct:.1f}%")
    
    # Peak month
    df['month_name'] = df['date'].dt.strftime('%B %Y')
    peak_month = df.groupby('month_name')['total_enrollments'].sum().idxmax()
    insights.append(f"📈 **Peak Enrollment Month**: {peak_month}")
    
    # Center type preference
    center_perm = df[df['center_type'] == 'Permanent']['total_enrollments'].sum()
    center_temp = df[df['center_type'] == 'Temporary']['total_enrollments'].sum()
    perm_pct = (center_perm / (center_perm + center_temp)) * 100
    insights.append(f"🏢 **Center Type**: {perm_pct:.1f}% enrollments at Permanent centers")
    
    # Daily average
    insights.append(f"📊 **Average Daily Enrollments**: {metrics['avg_daily']:,.0f} across all states")
    
    return insights

# Main Application
def main():
    # Header
    st.markdown('<div class="main-header">🆔 Aadhaar Enrollment Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # Sidebar - Filters
    st.sidebar.header("📊 Filters")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # State filter
    all_states = sorted(df['state'].unique())
    selected_states = st.sidebar.multiselect(
        "Select States",
        options=all_states,
        default=all_states
    )
    
    # Center type filter
    center_types = st.sidebar.multiselect(
        "Select Center Type",
        options=['Permanent', 'Temporary'],
        default=['Permanent', 'Temporary']
    )
    
    # Apply filters
    if len(date_range) == 2:
        filtered_df = df[
            (df['date'].dt.date >= date_range[0]) &
            (df['date'].dt.date <= date_range[1]) &
            (df['state'].isin(selected_states)) &
            (df['center_type'].isin(center_types))
        ]
    else:
        filtered_df = df[
            (df['state'].isin(selected_states)) &
            (df['center_type'].isin(center_types))
        ]
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_df)
    
    # Display key metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Enrollments", f"{metrics['total_enrollments']:,}")
    with col2:
        st.metric("Average Daily Enrollments", f"{metrics['avg_daily']:,.0f}")
    with col3:
        st.metric("States Covered", metrics['total_states'])
    with col4:
        st.metric("Days of Data", metrics['total_days'])
    
    st.markdown("---")
    
    # Time Series Analysis
    st.subheader("📈 Time Series Analysis")
    
    tab1, tab2 = st.tabs(["Daily Trends", "Monthly Trends"])
    
    with tab1:
        st.plotly_chart(plot_time_series(filtered_df, freq='D'), use_container_width=True)
    
    with tab2:
        st.plotly_chart(plot_time_series(filtered_df, freq='M'), use_container_width=True)
    
    # Seasonal Patterns
    st.markdown("---")
    st.subheader("🌦️ Seasonal Patterns")
    st.plotly_chart(plot_seasonal_patterns(filtered_df), use_container_width=True)
    
    # State-wise Analysis
    st.markdown("---")
    st.subheader("🗺️ State-wise Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        top_n = st.slider("Number of top states to display", 5, 20, 10)
        st.plotly_chart(plot_state_comparison(filtered_df, top_n), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_center_type_distribution(filtered_df), use_container_width=True)
    
    # Demographics
    st.markdown("---")
    st.subheader("👥 Demographics Analysis")
    plot_demographics(filtered_df)
    
    # Insights
    st.markdown("---")
    st.subheader("💡 Actionable Insights")
    insights = generate_insights(filtered_df, metrics)
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    # Data Table
    st.markdown("---")
    st.subheader("📋 Detailed Data View")
    
    if st.checkbox("Show raw data"):
        st.dataframe(
            filtered_df.head(100),
            use_container_width=True,
            height=400
        )
        
        st.download_button(
            label="📥 Download Filtered Data",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='aadhaar_enrollment_filtered.csv',
            mime='text/csv',
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>🆔 Aadhaar Enrollment Analytics Dashboard</p>
        <p>Built with Python and Streamlit | Data is for demonstration purposes only</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
