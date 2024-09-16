import streamlit as st
import pandas as pd
import pickle
from github import Github

# Initialize GitHub authentication with your personal access token
g = Github("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")

def fetch_repo_data(repo_url):
    repo_name = repo_url.split("/")[-2] + "/" + repo_url.split("/")[-1]
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        st.error(f"Error accessing repository: {e}")
        return None, None, None

    # Fetch commits
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

    # Fetch pull requests
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

    # Fetch issues
    issues = repo.get_issues(state='all')
    issue_data = []
    for issue in issues:
        if issue.pull_request:
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

def save_to_pickle(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def fetch_and_display_data(repo_urls):
    for repo_url in repo_urls:
        # Extract repository details from the URL
        repo_name = repo_url.split('/')[-1]
        
        # Fetch data from the repository
        commits_df, pr_df, issues_df = fetch_repo_data(repo_url)
        
        if commits_df is not None:
            # Save data to appropriate files (more than 1 files)
            save_to_pickle(commits_df, f'/{repo_name}_commits.pkl')
            save_to_pickle(pr_df, f'/{repo_name}_pr.pkl')
            save_to_pickle(issues_df, f'/{repo_name}_issues.pkl')
