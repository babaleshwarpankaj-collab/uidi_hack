"""
Script to generate sample Aadhaar enrollment data for the dashboard
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Indian states
states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
    'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
    'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
    'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
    'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi', 'Jammu and Kashmir'
]

# Generate date range (2 years of data)
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

data = []

for date in date_range:
    # More enrollments on weekdays, seasonal variations
    day_of_week = date.weekday()
    month = date.month
    
    # Seasonal factor (more enrollments in certain months)
    seasonal_factor = 1.0
    if month in [1, 2, 12]:  # Winter
        seasonal_factor = 1.2
    elif month in [6, 7, 8]:  # Monsoon
        seasonal_factor = 0.8
    
    # Weekend factor
    weekend_factor = 0.6 if day_of_week >= 5 else 1.0
    
    for state in states:
        # Base enrollment varies by state population
        state_factor = np.random.uniform(0.5, 2.0)
        
        # Daily enrollments
        base_enrollments = np.random.poisson(500) * state_factor * seasonal_factor * weekend_factor
        
        # Gender distribution
        male_ratio = np.random.uniform(0.48, 0.52)
        male_enrollments = int(base_enrollments * male_ratio)
        female_enrollments = int(base_enrollments * (1 - male_ratio))
        
        # Age groups
        child = int(base_enrollments * 0.25)  # 0-18
        adult = int(base_enrollments * 0.55)  # 19-60
        senior = int(base_enrollments * 0.20)  # 60+
        
        data.append({
            'date': date,
            'state': state,
            'total_enrollments': int(base_enrollments),
            'male_enrollments': male_enrollments,
            'female_enrollments': female_enrollments,
            'child_enrollments': child,
            'adult_enrollments': adult,
            'senior_enrollments': senior,
            'center_type': np.random.choice(['Permanent', 'Temporary'], p=[0.7, 0.3])
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('sample_data.csv', index=False)
print(f"Generated {len(df)} rows of sample data")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total enrollments: {df['total_enrollments'].sum():,}")
print("\nSample data:")
print(df.head())
