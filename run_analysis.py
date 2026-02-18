import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")

try:
    # Load the data
    df = pd.read_csv("Sum of age_0_5, Sum of age_18_greater and Sum of age_5_17 by state.csv")
    
    # Display basic information
    print("\nFirst few rows of the dataset:")
    print(df.head())
    
    # Calculate total enrollments by age group
    total_0_5 = df['Sum of age_0_5'].sum()
    total_5_17 = df['Sum of age_5_17'].sum()
    total_18_plus = df['Sum of age_18_greater'].sum()
    
    # Create a summary DataFrame
    summary = pd.DataFrame({
        'Age Group': ['0-5 years', '5-17 years', '18+ years'],
        'Total Enrollments': [total_0_5, total_5_17, total_18_plus]
    })
    
    print("\nTotal Enrollments by Age Group:")
    print(summary)
    
    # 1. Bar plot of total enrollments by age group
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Age Group', y='Total Enrollments', data=summary)
    plt.title('Total Aadhaar Enrollments by Age Group')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('enrollments_by_age_group.png', dpi=300)
    
    # 2. Top 10 states by 0-5 age group enrollments
    top_states = df.nlargest(10, 'Sum of age_0_5')
    plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='Sum of age_0_5', data=top_states)
    plt.title('Top 10 States by 0-5 Years Enrollments')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('top_states_0_5.png', dpi=300)
    
    # 3. Pie chart of age distribution
    plt.figure(figsize=(8, 8))
    plt.pie(summary['Total Enrollments'], 
            labels=summary['Age Group'], 
            autopct='%1.1f%%',
            startangle=90)
    plt.title('Aadhaar Enrollment Distribution by Age Group')
    plt.tight_layout()
    plt.savefig('age_distribution_pie.png', dpi=300)
    
    print("\nAnalysis complete! The following visualizations have been saved:")
    print("- enrollments_by_age_group.png")
    print("- top_states_0_5.png")
    print("- age_distribution_pie.png")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("\nPlease ensure all required data files are in the current directory.")
    print("The script expects a file named 'Sum of age_0_5, Sum of age_18_greater and Sum of age_5_17 by state.csv' in the same directory.")
