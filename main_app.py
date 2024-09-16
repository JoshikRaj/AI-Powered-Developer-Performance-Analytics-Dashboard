

# Importing  external dependencies
import pickle
import streamlit as st
import os

# Importing classes from different modules
from dev_performance_dashboard.data_collection.github_api import GitRepCollector
from dev_performance_dashboard.metrics.calculations import MetricsCalculator
from dev_performance_dashboard.visualization.charts import Visualizer
from dev_performance_dashboard.query_interface.nlp_processor import NLPModule


def main():
    # Set up the page title and navigation menu
    st.set_page_config(page_title="AI-Powered Developer Performance Analytics Dashboard")
    st.title("AI-Powered Developer Performance Analytics Dashboard")
    st.sidebar.title("Navigation")
    options = ["Home", "GitHub Data Fetcher", "Metrics Calculation", "Performance Metrics Visualization", "Natural Language Query"]
    selection = st.sidebar.radio("Go to", options)

    # Initialize objects for different functionalities
    repo_collector = GitRepCollector() 
    metric_calculator = MetricsCalculator("dev_performance_dashboard/data_collection")
    visualizer = Visualizer()
    nlpmodule = NLPModule()

    # Define behavior for each navigation option
    if selection == "Home":
        st.markdown(
    """
    <div style="display: flex; justify-content: center; padding: 20px;">
        <div style="border: 2px solid #ddd; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); overflow: hidden;">
            <img src="https://media.istockphoto.com/id/1480239160/photo/an-analyst-uses-a-computer-and-dashboard-for-data-business-analysis-and-data-management.jpg?s=612x612&w=0&k=20&c=Zng3q0-BD8rEl0r6ZYZY0fbt2AWO9q_gC8lSrwCIgdk="
            alt="GitHub"
            style="width: 400px; height: auto; display: block;"/>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
        st.header("Project Overview")

        st.write("""
            Welcome to the AI-Powered Developer Performance Analytics Dashboard. 
            This application will allow you to:
            - Fetch data from GitHub repositories.
            - Calculate performance metrics based on GitHub data (Commits, Issues, Pull_Requests).
            - Visualize performance metrics through interactive charts using plotly library.
            - Query metrics using natural language processing using advanced LLM (Cohere).
        """)

    elif selection == "GitHub Data Fetcher":
        st.header("GitHub Data Fetcher")
        repo_url = st.text_input("Enter GitHub Repository URL:")

        if repo_url:
            # Set the repo URL
            repo_collector.set_url(repo_url)
            
            # Fetch the data and check if successful
            success = repo_collector.fetch_and_display_data()  # Assuming this method returns success or failure
            
            if success:  # If data fetching is successful
                st.markdown("<h4 style='color: green;'>The data has been successfully fetched and stored in your local folder.</h4>", unsafe_allow_html=True)
            else:  # If data fetching fails
                st.markdown("<h4 style='color: red;'>Failed to fetch data. Please check the repository URL.</h4>", unsafe_allow_html=True)


    elif selection == "Metrics Calculation":
        st.header("Metrics Calculation")
        if st.button("Calculate Metrics"):

            metrics = metric_calculator.calculate_performance_metrics()

            st.write("Metrics have been calculated and saved.")

            # Display the metrics results
            st.subheader("Commit Frequency")
            st.metric(label='Average Commits per Day', value=f"{metrics['Commit Frequency (average commits/day)']:.2f}")

            st.subheader("Total Commits")
            st.metric(label='Total Commits', value=f"{metrics['Total Commits']}")

            st.subheader("PR Merge Rate")
            st.metric(label='PR Merge Rate (%)', value=f"{metrics['PR Merge Rate (%)']:.2f}%")

            st.subheader("Issue Resolution Time")
            st.metric(label='Average Issue Resolution Time (days)',
                    value=f"{metrics['Issue Resolution Time (days)'].mean():.2f} days")

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
        metrics_pkl_path = 'dev_performance_dashboard/metrics/metrics.pkl'

        visualizer.set_path(metrics_pkl_path)

        if os.path.exists(metrics_pkl_path):
            visualizer.visualize() # Visualize the metrics
        else:
            st.error("Metrics file not found. Please ensure the file exists at the specified path.")

    elif selection == "Natural Language Query":
        st.header("Natural Language Query")
        metrics_path = 'dev_performance_dashboard/metrics/metrics.pkl'
        nlpmodule.set_path(metrics_path)
        nlpmodule.natural_language_query_module()

# Entry point for script execution
if __name__ ==  "__main__":
    main()