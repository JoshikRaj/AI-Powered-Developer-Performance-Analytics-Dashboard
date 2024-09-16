import pandas as pd
import pickle
import os

# Creating Class to calculate and store metrics from a dataframe
class MetricsCalculator:
    def __init__(self,dir_path):
        self.data_dir = dir_path # Path to the data directory which has data
        self.commit_df = None
        self.issue_df = None
        self.pr_df = None
        self.metrics = None

    # Method to load commits data from a pickle file
    def get_commit_df(self,path):
        with open(path,'rb') as f:
            self.commits_df = pickle.load(f)

    # Method to load issues data from a pickle file
    def get_issue_df(self,path):
        with open(path,'rb') as f:
            self.issue_df = pickle.load(f)

    # Method to load pull_requests data from a pickle file
    def get_pr_df(self,path):
        with open(path,'rb') as f:
            self.pr_df = pickle.load(f)

    # Method to calculate performance metrics
    def calculate_performance_metrics(self):
        # Defining Paths 
        commit_data_path = os.path.join(self.data_dir, 'commits.pkl')
        pr_data_path = os.path.join(self.data_dir, 'pr.pkl')
        issue_data_path = os.path.join(self.data_dir, 'issues.pkl')

        # Loading Data
        self.get_commit_df(commit_data_path)
        self.get_pr_df(pr_data_path)
        self.get_issue_df(issue_data_path)

        # Calculate Commit Frequency
        commit_counts = self.commits_df.groupby(self.commits_df['date'].dt.date).size()
        average_commits_per_day = commit_counts.mean()
        total_commits = commit_counts.sum()

        # Defining the metrics dictionary
        self.metrics = {
            'Commit Frequency (average commits/day)': average_commits_per_day,
            'Total Commits': total_commits,
            'PR Merge Rate (%)': (self.pr_df['state'] == 'closed').mean() * 100,
            'Issue Resolution Time (days)': (self.issue_df['closed_at'] - self.issue_df['created_at']).dt.total_seconds() / (60 * 60 * 24),
            'PR Review Time (days)': (self.pr_df['closed_at'] - self.pr_df['created_at']).dt.total_seconds() / (60 * 60 * 24),
            'Code Churn Rate (%)': 30,  # Placeholder
            'Average Commit Size (message length)': 45,  # Placeholder
            'Open-to-Closed Issues Ratio': 0.5  # Placeholder
        }

        # Save metrics to pickle in the metrics folder for further use
        metrics_path = 'dev_performance_dashboard/metrics'
        if not os.path.exists(metrics_path):
            os.makedirs(metrics_path)

        # Save the metrics as a pickle file
        with open(os.path.join(metrics_path, 'metrics.pkl'), 'wb') as f:
            pickle.dump(self.metrics, f)

        return self.metrics 

   

