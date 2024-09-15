import pickle
import streamlit as st
from dev_performance_dashboard.data_collection.github_api import fetch_and_display_data
from dev_performance_dashboard.metrics.calculations import calculate_and_save_metrics
from dev_performance_dashboard.visualization.charts import visu
from dev_performance_dashboard.query_interface.query_temp import natural_language_query_module




st.title("AI-Powered Developer Performance Analytics Dashboard")

# Navigation menu
st.sidebar.title("Navigation")
options = ["Home", "GitHub Data Fetcher", "Metrics Calculation", "Performance Metrics Visualization", "Natural Language Query"]
selection = st.sidebar.radio("Go to", options)

if selection == "Home":
    st.header("Project Overview")
    st.write("""Welcome to the Developer Performance Analytics Dashboard. This application allows you to:
        - Fetch data from GitHub repositories.
        - Calculate performance metrics based on GitHub data.
        - Visualize performance metrics through interactive charts.
        - Query metrics using natural language processing.""")

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
        
        st.subheader("Commit Frequency")
        st.metric(label='Average Commits per Day', value=f"{metrics['Commit Frequency (average commits/day)']:.2f}")
        
        st.subheader("Total Commits")
        st.metric(label='Total Commits', value=f"{metrics['Total Commits']}")

        st.subheader("PR Merge Rate")
        st.metric(label='PR Merge Rate (%)', value=f"{metrics['PR Merge Rate (%)']:.2f}%")

        st.subheader("Issue Resolution Time")
        st.metric(label='Average Issue Resolution Time (days)', value=f"{metrics['Issue Resolution Time (days)'].mean():.2f} days")

        st.subheader("PR Review Time")
        st.metric(label='Average PR Review Time (days)', value=f"{metrics['PR Review Time (days)'].mean():.2f} days")

        st.subheader("Code Churn Rate")
        st.metric(label='Code Churn Rate (%)', value=f"{metrics['Code Churn Rate (%)']:.2f}%")
        
        st.subheader("Average Commit Size")
        st.metric(label='Average Commit Size (message length)', value=f"{metrics['Average Commit Size (message length)']} characters")
        
        st.subheader("Open-to-Closed Issues Ratio")
        st.metric(label='Open-to-Closed Issues Ratio', value=f"{metrics['Open-to-Closed Issues Ratio']:.2f}")

elif selection == "Performance Metrics Visualization":
    st.header("Performance Metrics Visualization")
    pickle_file_path = 'dev_performance_dashboard/metrics/metrics.pkl'
    visu() 
    

elif selection == "Natural Language Query":
    st.header("Natural Language Query")
    metrics_path = 'dev_performance_dashboard/metrics/metrics.pkl'  # Adjust path to your metrics file
    try:
        with open(metrics_path, 'rb') as file:
            metrics = pickle.load(file)
        natural_language_query_module(metrics)
    except FileNotFoundError:
        st.error(f"File not found: {metrics_path}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

