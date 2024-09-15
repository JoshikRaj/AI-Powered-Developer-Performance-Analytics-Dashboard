import pandas as pd
import pickle
import os

def calculate_performance_metrics():
    base_path = 'dev_performance_dashboard/data_collection'

    with open(os.path.join(base_path, 'commits.pkl'), 'rb') as f:
        commits_df = pickle.load(f)
    with open(os.path.join(base_path, 'pr.pkl'), 'rb') as f:
        pr_df = pickle.load(f)
    with open(os.path.join(base_path, 'issues.pkl'), 'rb') as f:
        issues_df = pickle.load(f)

    # Calculate Commit Frequency
    commit_counts = commits_df.groupby(commits_df['date'].dt.date).size()
    average_commits_per_day = commit_counts.mean()
    total_commits = commit_counts.sum()

    metrics = {
        'Commit Frequency (average commits/day)': average_commits_per_day,
        'Total Commits': total_commits,
        'PR Merge Rate (%)': (pr_df['state'] == 'closed').mean() * 100,
        'Issue Resolution Time (days)': (issues_df['closed_at'] - issues_df['created_at']).dt.total_seconds() / (60 * 60 * 24),
        'PR Review Time (days)': (pr_df['closed_at'] - pr_df['created_at']).dt.total_seconds() / (60 * 60 * 24),
        'Code Churn Rate (%)': 30,  # Placeholder
        'Average Commit Size (message length)': 45,  # Placeholder
        'Open-to-Closed Issues Ratio': 0.5  # Placeholder
    }

    # Save metrics to pickle in the metrics folder
    metrics_path = 'dev_performance_dashboard/metrics'
    if not os.path.exists(metrics_path):
        os.makedirs(metrics_path)

    with open(os.path.join(metrics_path, 'metrics.pkl'), 'wb') as f:
        pickle.dump(metrics, f)
    
    return metrics

def calculate_and_save_metrics():
    metrics = calculate_performance_metrics()
    print(metrics)
    return metrics