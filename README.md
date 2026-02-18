# 🆔 Aadhaar Enrollment Analytics Dashboard

An interactive dashboard to analyze and visualize Aadhaar enrollment patterns, demographics, and trends across India. Built with Python and Streamlit, this tool provides actionable insights into enrollment data to help identify gaps and planning opportunities.

![Dashboard Screenshot](https://github.com/user-attachments/assets/9cf284e7-47e8-4d0c-839e-2029f3bc6656)

## 🚀 Features

- **📊 Interactive Dashboard**: A user-friendly interface to explore data dynamically
- **📈 Time Series Analysis**: Visualize daily and monthly enrollment trends with seasonal patterns
- **🗺️ State-wise Analysis**: Compare enrollment performance across different states
- **👥 Demographics Analysis**: Understand enrollment distribution by gender and age groups
- **🏢 Center Type Analysis**: Analyze enrollments by permanent vs temporary centers
- **💡 Actionable Insights**: Automated insights highlighting key trends and patterns
- **🔍 Advanced Filters**: Filter data by date range, states, and center type
- **📥 Data Export**: Download filtered data for further analysis

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/babaleshwarpankaj-collab/uidi_hack.git
cd uidi_hack
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Generate Sample Data

First, generate sample enrollment data:

```bash
python generate_data.py
```

This will create a `sample_data.csv` file with 2 years of synthetic enrollment data across 30 Indian states.

### Run the Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Dashboard Sections

### 1. Key Metrics
- **Total Enrollments**: Aggregate enrollment count
- **Average Daily Enrollments**: Mean enrollments per day
- **States Covered**: Number of states in the dataset
- **Days of Data**: Total days of enrollment records

### 2. Time Series Analysis
- **Daily Trends**: Line chart showing day-by-day enrollment patterns
- **Monthly Trends**: Bar chart displaying monthly aggregated enrollments

### 3. Seasonal Patterns
- Monthly average enrollments to identify seasonal trends
- Helps in resource planning and capacity management

### 4. State-wise Analysis
- Top N states by total enrollments (configurable via slider)
- Horizontal bar chart for easy comparison
- Center type distribution (Permanent vs Temporary)

### 5. Demographics Analysis
- **Gender Distribution**: Pie chart showing male vs female enrollments
- **Age Group Distribution**: Breakdown by Children (0-18), Adults (19-60), and Seniors (60+)

### 6. Actionable Insights
Automated insights including:
- Top performing state
- Gender distribution percentages
- Peak enrollment month
- Center type preference
- Daily average across all states

### 7. Detailed Data View
- Option to view raw data
- Download filtered data as CSV

## 🎛️ Filters

The sidebar provides interactive filters:

- **Date Range**: Select custom date ranges for analysis
- **States**: Multi-select dropdown to filter by specific states
- **Center Type**: Filter by Permanent or Temporary centers

All visualizations and metrics update automatically based on selected filters.

## 📁 Project Structure

```
uidi_hack/
├── dashboard.py          # Main Streamlit application
├── generate_data.py      # Script to generate sample data
├── requirements.txt      # Python dependencies
├── sample_data.csv      # Generated enrollment data (after running generate_data.py)
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## 🔧 Data Schema

The enrollment data includes:

- `date`: Date of enrollment
- `state`: Indian state name
- `total_enrollments`: Total enrollments for the day
- `male_enrollments`: Male enrollments
- `female_enrollments`: Female enrollments
- `child_enrollments`: Enrollments for age 0-18
- `adult_enrollments`: Enrollments for age 19-60
- `senior_enrollments`: Enrollments for age 60+
- `center_type`: Permanent or Temporary

## 🎨 Customization

You can customize the dashboard by:

1. **Adding new visualizations**: Edit `dashboard.py` and add new chart functions
2. **Modifying data generation**: Edit `generate_data.py` to change data patterns
3. **Styling**: Modify the CSS in the `st.markdown()` section of `dashboard.py`
4. **Adding filters**: Extend the sidebar section with additional filter options

## 📝 Notes

- The sample data is generated synthetically for demonstration purposes
- Data patterns include realistic variations like weekend effects and seasonal trends
- The dashboard is optimized for performance with caching enabled

## 🐛 Troubleshooting

**Issue**: Dashboard shows "Data file not found" error  
**Solution**: Run `python generate_data.py` first to create the sample data

**Issue**: Import errors when running the dashboard  
**Solution**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available for educational and demonstration purposes.

## 👤 Author

Built with ❤️ for Aadhaar enrollment analytics

---

**Disclaimer**: This dashboard uses synthetic data for demonstration purposes only. It is not affiliated with UIDAI or any government organization.
