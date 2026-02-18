# 🆔 Aadhaar Enrollment Analytics Dashboard

An interactive dashboard to analyze and visualize Aadhaar enrollment patterns, demographics, and trends across India. Built with Python and Streamlit, this tool provides actionable insights into enrollment data to help identify gaps and planning opportunities.

## 🚀 Features

-   **📊 Interactive Dashboard**: A user-friendly interface to explore data dynamically.
-   **📈 Time Series Analysis**: Visualize daily and monthly enrollment trends with seasonal decomposition.
-   **👥 Demographic Insights**: Breakdown of enrollments by Age Group (0-5, 5-17, 18+), Gender, and Urban/Rural distribution.
-   **🌍 Geographical Analysis**: Identify top-performing states and regional disparities.
-   **🔮 Forecasting**: 30-day enrollment forecast using moving averages and trend analysis.
-   **📱 Responsive Design**: Optimized for viewing on various devices.

## 🛠️ Tech Stack

-   **Python 3.x**
-   **Streamlit** (Frontend framework)
-   **Pandas & NumPy** (Data manipulation)
-   **Plotly** (Interactive visualizations)
-   **Statsmodels** (Time series analysis)
-   **Matplotlib & Seaborn** (Static plotting)

## ⚙️ Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/babaleshwarpankaj-collab/uidi_hack.git
    cd uidi_hack
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

Run the dashboard locally:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure

-   `app.py`: Main Streamlit application file.
-   `analyze_enrollment.py`: Script for data preprocessing and generating static reports.
-   `requirements.txt`: List of Python dependencies.
-   `data/`: Directory for storing dataset files (if applicable).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
