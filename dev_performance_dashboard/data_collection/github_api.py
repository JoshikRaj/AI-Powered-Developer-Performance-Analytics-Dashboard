# Importing the necessary libraries
import streamlit as st
import pandas as pd
import pickle
from github import Github

# Creating a class for easy access
class GitRepCollector:
    # Initialize the class instance
    def __init__(self):
        # Github API authentication
        self.g = Github("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")
        self.repo_url = None
        self.commit_df = None
        self.issue_df = None
        self.pr_df = None

    # Method to set the repo URL
    def set_url(self,url):
        self.repo_url = url
    
    # Method to generate a DataFrame for commits
    def gen_commit_df(self,commits):

        commit_data = []
        # Iterating over all commits 
        for commit in commits:
            commit_data.append({
                "sha": commit.sha,
                "author": commit.commit.author.name,
                "date": commit.commit.author.date,
                "message": commit.commit.message
            })
        self.commit_df = pd.DataFrame(commit_data)

    # Method to generate a DataFrame for issues
    def gen_issue_df(self,issues):
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
        self.issue_df = pd.DataFrame(issue_data)

    # Method to generate a DataFrame for Pull Requests
    def gen_pr_df(self,prs):
        pr_data = []
        for pr in prs:
            pr_data.append({
                "id": pr.id,
                "title": pr.title,
                "created_at": pr.created_at,
                "closed_at": pr.closed_at,
                "state": pr.state
            })
        self.pr_df = pd.DataFrame(pr_data)

    # Method to fetch data from the repository
    def fetch_repo_data(self):
        repo_name = self.repo_url.split("/")[-2] + "/" + self.repo_url.split("/")[-1]
        
        # Exception handling
        try:
            repo = self.g.get_repo(repo_name)
        except Exception as e:
            st.error(f"Error accessing repository: {e}")
            return None, None, None, None

        commits = repo.get_commits()
        prs = repo.get_pulls(state='all')
        issues = repo.get_issues(state='all')

        # Generate a df for commits, prs and issues
        self.gen_commit_df(commits)
        self.gen_pr_df(prs)
        self.gen_issue_df(issues)

    # Method to display the data in Streamlit
    def fetch_and_display_data(self):
        self.fetch_repo_data()

        if self.commit_df is not None:
            st.subheader("Commits Data")
            st.dataframe(self.commit_df)

            st.subheader("Pull Requests Data")
            st.dataframe(self.pr_df)

            st.subheader("Issues Data")
            st.dataframe(self.issue_df)

            # Save data to pickle
            with open('dev_performance_dashboard/data_collection/commits.pkl', 'wb') as f:
                pickle.dump(self.commit_df, f)
            with open('dev_performance_dashboard/data_collection/pr.pkl', 'wb') as f:
                pickle.dump(self.pr_df, f)
            with open('dev_performance_dashboard/data_collection/issues.pkl', 'wb') as f:
                pickle.dump(self.issue_df, f)


