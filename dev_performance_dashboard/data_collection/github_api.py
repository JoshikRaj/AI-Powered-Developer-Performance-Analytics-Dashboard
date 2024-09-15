import streamlit as st
from github import Github
import pandas as pd
import os

# Initialize GitHub authentication with your personal access token
g = Github("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")

# Function to fetch repository data
def fetch_repo_data(repo_url):
    # Extract repository name from URL
    repo_name = repo_url.split("/")[-2] + "/" + repo_url.split("/")[-1]
    
    # Access the repository
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        st.error(f"Error accessing repository: {e}")
        return None, None, None, None

    # Collect data for commits
    commits = repo.get_commits()
    commit_data = []
    for commit in commits:
        commit_data.append({
            "sha": commit.sha,
            "author": commit.commit.author.name,
            "date": commit.commit.author.date,
            "message": commit.commit.message
        })
    commits_df = pd.DataFrame(commit_data)

    # Collect data for pull requests (PRs)
    pull_requests = repo.get_pulls(state='all')
    pr_data = []
    for pr in pull_requests:
        pr_data.append({
            "id": pr.id,
            "title": pr.title,
            "created_at": pr.created_at,
            "closed_at": pr.closed_at,
            "state": pr.state
        })
    pr_df = pd.DataFrame(pr_data)

    # Collect data for issues
    issues = repo.get_issues(state='all')
    issue_data = []
    for issue in issues:
        if issue.pull_request:  # Skip pull requests (PRs)
            continue
        issue_data.append({
            "id": issue.id,
            "title": issue.title,
            "created_at": issue.created_at,
            "closed_at": issue.closed_at,
            "state": issue.state
        })
    issues_df = pd.DataFrame(issue_data)

    return commits_df, pr_df, issues_df

# Function to save data to CSV
def save_to_csv(commits_df, pr_df, issues_df, repo_name):
    # Create a folder for the repository data if it doesn't exist
    save_path = f"./{repo_name}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Save the dataframes as CSV files
    commits_df.to_csv(f"{save_path}/commits.csv", index=False)
    pr_df.to_csv(f"{save_path}/pull_requests.csv", index=False)
    issues_df.to_csv(f"{save_path}/issues.csv", index=False)

    st.success(f"Data has been saved to folder: {save_path}")

# Streamlit UI
st.title("AI-Powered Developer Performance Analytics Dashboard")

# User input for GitHub repository URL
repo_url = st.text_input("Enter GitHub Repository URL:")

if repo_url:
    st.write(f"Fetching data from: {repo_url}")
    
    # Fetch data from GitHub API
    commits_df, pr_df, issues_df = fetch_repo_data(repo_url)
    
    # Display the fetched data in the UI
    if commits_df is not None:
        st.subheader("Commits Data")
        st.dataframe(commits_df)

        st.subheader("Pull Requests Data")
        st.dataframe(pr_df)

        st.subheader("Issues Data")
        st.dataframe(issues_df)

        # Save the data to CSV
        repo_name = repo_url.split("/")[-2] + "_" + repo_url.split("/")[-1]
        save_to_csv(commits_df, pr_df, issues_df, repo_name)
    else:
        st.error("Failed to fetch data. Please check the repository URL or token.")
