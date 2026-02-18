import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn')
sns.set_palette("viridis")

# Load and preprocess data
try:
    df = pd.read_csv("aadhaar_0_5_enrolment.csv")
    print("\nFirst few rows of the dataset:")
    print(df.head())
    
    # Basic data cleaning
    df.dropna(inplace=True)
    
    # Rename columns for clarity
    df.rename(columns={
        'State Name': 'State',
        'Enrolment Count': 'Enrolment'
    }, inplace=True)
    
    # Ensure numeric types
    df['Enrolment'] = pd.to_numeric(df['Enrolment'])
    
    # Calculate expected children (0-5 years) as 8% of population
    df['Expected_Children'] = df['Population'] * 0.08
    
    # Calculate enrollment gap and ratio
    df['Enrolment_Gap'] = df['Expected_Children'] - df['Enrolment']
    df['Gap_Ratio'] = (df['Enrolment_Gap'] / df['Expected_Children']).round(2)
    
    # Calculate enrollment percentage
    df['Enrolment_Percentage'] = (df['Enrolment'] / df['Expected_Children'] * 100).round(1)
    
    # Save processed data
    df.to_csv("cleaned_aadhaar_analysis.csv", index=False)
    
    # 1. Overall Enrollment Status
    plt.figure(figsize=(12, 6))
    total_expected = df['Expected_Children'].sum()
    total_enrolled = df['Enrolment'].sum()
    plt.bar(['Expected', 'Enrolled'], [total_expected, total_enrolled])
    plt.title('Total Expected vs Actual Enrollment (0-5 years)')
    plt.ylabel('Number of Children (in millions)')
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('enrollment_summary.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Top 10 States by Enrollment Gap
    plt.figure(figsize=(14, 8))
    state_gap = df.groupby('State')['Gap_Ratio'].mean().sort_values(ascending=False)
    ax = state_gap.head(10).plot(kind='barh')
    plt.title('Top 10 States with Highest Enrollment Gap Ratio (0-5 years)')
    plt.xlabel('Gap Ratio (Lower is better)')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(state_gap.head(10)):
        ax.text(v + 0.01, i, f"{v:.2f}", color='black', va='center')
    
    plt.tight_layout()
    plt.savefig('top_states_gap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Enrollment Distribution by State
    plt.figure(figsize=(14, 8))
    state_enrollment = df.groupby('State')['Enrolment_Percentage'].mean().sort_values(ascending=False)
    ax = sns.barplot(x=state_enrollment.values, y=state_enrollment.index, palette='viridis')
    plt.title('Enrollment Percentage by State (0-5 years)')
    plt.xlabel('Enrollment Percentage (%)')
    plt.ylabel('')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Add percentage labels
    for i, v in enumerate(state_enrollment):
        ax.text(v + 1, i, f"{v}%", color='black', va='center')
    
    plt.tight_layout()
    plt.savefig('enrollment_by_state.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. Enrollment vs Population Scatter Plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='Population', y='Enrolment', hue='State', 
                   size='Enrolment_Percentage', sizes=(50, 300), alpha=0.7)
    plt.title('Enrollment vs Population by State')
    plt.xlabel('Population')
    plt.ylabel('Enrollment Count')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('enrollment_vs_population.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. Enrollment Gap Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Gap_Ratio'], bins=20, kde=True)
    plt.title('Distribution of Enrollment Gap Ratio')
    plt.xlabel('Gap Ratio')
    plt.ylabel('Number of Districts')
    plt.axvline(df['Gap_Ratio'].mean(), color='r', linestyle='--', 
                label=f'Mean: {df["Gap_Ratio"].mean():.2f}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('gap_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nAnalysis complete! Generated the following visualizations:")
    print("1. enrollment_summary.png - Overall enrollment status")
    print("2. top_states_gap.png - Top 10 states with highest enrollment gap")
    print("3. enrollment_by_state.png - Enrollment percentage by state")
    print("4. enrollment_vs_population.png - Scatter plot of enrollment vs population")
    print("5. gap_distribution.png - Distribution of enrollment gap ratio")
    print("\nSaved processed data to: cleaned_aadhaar_analysis.csv")
    
except FileNotFoundError:
    print("Error: Input file 'aadhaar_0_5_enrolment.csv' not found.")
    print("Please ensure the file exists in the current directory.")
except Exception as e:
    print(f"An error occurred: {str(e)}")