import pickle
import streamlit as st
from dev_performance_dashboard.data_collection.github_api import fetch_and_display_data
from dev_performance_dashboard.metrics.calculations import calculate_and_save_metrics
from dev_performance_dashboard.visualization.charts import visu
from dev_performance_dashboard.query_interface.query_temp import natural_language_query_module
import os

# Set up the page title and navigation menu
st.set_page_config(page_title="AI-Powered Developer Performance Analytics Dashboard")
st.title("AI-Powered Developer Performance Analytics Dashboard")

st.sidebar.title("Navigation")
options = ["Home", "GitHub Data Fetcher", "Metrics Calculation", "Performance Metrics Visualization", "Natural Language Query"]
selection = st.sidebar.radio("Go to", options)

# Define behavior for each navigation option
if selection == "Home":
    st.header("Project Overview")
    st.write("""
        Welcome to the Developer Performance Analytics Dashboard. This application allows you to:
        - Fetch data from GitHub repositories.
        - Calculate performance metrics based on GitHub data.
        - Visualize performance metrics through interactive charts.
        - Query metrics using natural language processing.
    """)

elif selection == "GitHub Data Fetcher":
    st.header("GitHub Data Fetcher")
    repo_url = st.text_input("Enter GitHub Repository URL:")
    if repo_url:
        fetch_and_display_data(repo_url)

elif selection == "Metrics Calculation":
    st.header("Metrics Calculation")
    if st.button("Calculate Metrics"):
        metrics = calculate_and_save_metrics()
        st.write("Metrics have been calculated and saved.")

        # Display key metrics in a structured manner
        for metric, value in metrics.items():
            st.metric(label=metric, value=f"{value:.2f}")

elif selection == "Performance Metrics Visualization":
    st.header("Performance Metrics Visualization")
    metrics_pkl_path = 'dev_performance_dashboard/metrics/metrics.pkl'
    if os.path.exists(metrics_pkl_path):
        with open(metrics_pkl_path, 'rb') as f:
            metrics = pickle.load(f)
        visu()
    else:
        st.error("Metrics file not found. Please ensure the file exists at the specified path.")

elif selection == "Natural Language Query":
    st.header("Natural Language Query")
    metrics_path = 'dev_performance_dashboard/metrics/metrics.pkl'
    try:
        with open(metrics_path, 'rb') as file:
            metrics = pickle.load(file)
        natural_language_query_module(metrics)
    except FileNotFoundError:
        st.error(f"File not found: {metrics_path}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
