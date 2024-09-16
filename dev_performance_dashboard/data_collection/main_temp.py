import streamlit as st
from github_api import fetch_and_display_data

st.title("Developer Performance Analytics Dashboard")

# Navigation menu
st.sidebar.title("Navigation")
options = ["Home", "GitHub Data Fetcher", "Metrics Calculation", "Performance Metrics Visualization", "Natural Language Query"]
selection = st.sidebar.radio("Go to", options)

if selection == "GitHub Data Fetcher":
    st.header("GitHub Data Fetcher")

    # To Get multiple GitHub repositories
    repo_urls_input = st.text_area("Enter GitHub Repository URLs (one per line):")
    repo_urls = [url.strip() for url in repo_urls_input.split('\n') if url.strip()]
    if st.button("Fetch Data"):
        if repo_urls:
            fetch_and_display_data(repo_urls)
            st.write("Data fetching complete.")
        else:
            st.write("Please enter at least one repository URL.")