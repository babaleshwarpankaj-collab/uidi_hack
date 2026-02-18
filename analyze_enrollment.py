import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os
from datetime import datetime

# Set style for plots
plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12

def load_data():
    """Load all CSV files in the directory and concatenate them."""
    # Get all CSV files in the directory
    csv_files = glob('api_data_aadhar_enrolment_*.csv')
    
    # Read and concatenate all CSV files
    dfs = []
    for file in csv_files:
        print(f"Loading {file}...")
        df = pd.read_csv(file)
        dfs.append(df)
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def clean_data(df):
    """Clean and preprocess the data."""
    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    
    # Convert numeric columns to appropriate types
    numeric_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows with missing values in key columns
    df = df.dropna(subset=['state', 'district', 'pincode'] + numeric_cols, how='all')
    
    return df

def sort_and_save_data(df):
    """Sort the data by date and save to a new CSV file."""
    # Sort by date
    df_sorted = df.sort_values('date')
    
    # Reset index after sorting
    df_sorted = df_sorted.reset_index(drop=True)
    
    # Format date back to original format for saving
    df_sorted['date'] = df_sorted['date'].dt.strftime('%d-%m-%Y')
    
    # Save to a new CSV file
    output_file = 'sorted_aadhaar_data.csv'
    df_sorted.to_csv(output_file, index=False)
    
    print(f"\n✓ Data has been sorted by date and saved as '{output_file}'")
    print(f"Total records saved: {len(df_sorted):,}")
    
    # Convert date back to datetime for further analysis
    df_sorted['date'] = pd.to_datetime(df_sorted['date'], format='%d-%m-%Y')
    
    return df_sorted

def analyze_enrollment(df):
    """Perform analysis on the enrollment data."""
    print("\n=== Basic Data Overview ===")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Number of states: {df['state'].nunique()}")
    print(f"Number of districts: {df['district'].nunique()}")
    
    # Total enrollments by age group
    print("\n=== Total Enrollments by Age Group ===")
    age_columns = ['age_0_5', 'age_5_17', 'age_18_greater']
    age_totals = df[age_columns].sum()
    print(age_totals)
    
    # Top 10 states by enrollment
    print("\n=== Top 10 States by Total Enrollments ===")
    df['total_enrollments'] = df[age_columns].sum(axis=1)
    state_totals = df.groupby('state')['total_enrollments'].sum().sort_values(ascending=False).head(10)
    print(state_totals)
    
    return df

def plot_enrollment_trends(df):
    """Create visualizations of enrollment trends."""
    # Create output directory if it doesn't exist
    os.makedirs('visualizations', exist_ok=True)
    
    # 1. Daily Enrollment Trends
    plt.figure(figsize=(14, 6))
    daily_enrollments = df.groupby('date')['total_enrollments'].sum()
    plt.plot(daily_enrollments.index, daily_enrollments.values, marker='o', linestyle='-', linewidth=1, markersize=3)
    plt.title('Daily Aadhaar Enrollments Over Time', pad=20)
    plt.xlabel('Date')
    plt.ylabel('Number of Enrollments')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('visualizations/daily_enrollments.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Age Group Distribution
    plt.figure(figsize=(10, 6))
    age_columns = ['age_0_5', 'age_5_17', 'age_18_greater']
    age_totals = df[age_columns].sum()
    age_labels = ['0-5 years', '5-17 years', '18+ years']
    
    colors = ['#66b3ff', '#ff9999', '#99ff99']
    explode = (0.05, 0.05, 0.05)
    
    plt.pie(age_totals, labels=age_labels, autopct='%1.1f%%', 
            colors=colors, explode=explode, startangle=90,
            wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': 'solid', 'antialiased': True})
    
    plt.title('Age Group Distribution of Aadhaar Enrollments', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('visualizations/age_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Top 10 States by Enrollment
    plt.figure(figsize=(12, 8))
    state_enrollments = df.groupby('state')['total_enrollments'].sum().nlargest(10).sort_values()
    
    ax = state_enrollments.plot(kind='barh', color='#20b2aa')
    plt.title('Top 10 States by Total Aadhaar Enrollments', pad=20)
    plt.xlabel('Number of Enrollments')
    
    # Add value labels on the bars
    for i, v in enumerate(state_enrollments):
        ax.text(v + 1000, i, f'{v:,}', color='black', va='center')
    
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('visualizations/top_states.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Monthly Enrollment Trends by Age Group
    plt.figure(figsize=(14, 6))
    df['month_year'] = df['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df.groupby('month_year')[age_columns].sum()
    
    for col in age_columns:
        plt.plot(monthly.index, monthly[col], marker='o', label=col.replace('_', ' ').title())
    
    plt.title('Monthly Aadhaar Enrollments by Age Group', pad=20)
    plt.xlabel('Month')
    plt.ylabel('Number of Enrollments')
    plt.legend(title='Age Group')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualizations/monthly_age_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nVisualizations have been saved in the 'visualizations' directory.")

def main():
    print("Starting Aadhaar Enrollment Data Analysis...")
    print("=" * 50)
    
    try:
        # Load and clean the data
        print("\n[1/4] Loading data...")
        df = load_data()
        print(f"✓ Loaded {len(df):,} records")
        
        print("\n[2/4] Cleaning and preparing data...")
        df = clean_data(df)
        
        # Sort and save the data
        print("\n[2.5/4] Sorting data by date...")
        df = sort_and_save_data(df)
        
        # Add total enrollments column
        age_columns = ['age_0_5', 'age_5_17', 'age_18_greater']
        df['total_enrollments'] = df[age_columns].sum(axis=1)
        
        # Perform analysis
        print("\n[3/4] Analyzing data...")
        analyze_enrollment(df)
        
        # Generate visualizations
        print("\n[4/4] Generating visualizations...")
        plot_enrollment_trends(df)
        
        print("\n" + "=" * 50)
        print("Analysis complete! Here's what we've done:")
        print("1. Created 'sorted_aadhaar_data.csv' with data sorted by date")
        print("2. Generated visualizations in the 'visualizations' directory:")
        print("   - daily_enrollments.png: Shows enrollment trends over time")
        print("   - age_distribution.png: Pie chart of age group distribution")
        print("   - top_states.png: Horizontal bar chart of top 10 states by enrollment")
        print("   - monthly_age_trends.png: Monthly trends by age group")
        print("\nYou can find all output files in the project directory and 'visualizations' folder.")
        
    except Exception as e:
        print("\n" + "!" * 50)
        print(f"An error occurred: {str(e)}")
        print("Please check if all required data files are present in the directory.")
        print("!" * 50)

if __name__ == "__main__":
    main()
