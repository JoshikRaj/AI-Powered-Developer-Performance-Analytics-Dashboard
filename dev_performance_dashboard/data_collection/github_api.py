from github import Github

# Authenticate using an access token
g = Github("")

# Get a repository by its URL
def get_repo_data(repo_url):
    repo_name = repo_url.split('/')[-2] + "/" + repo_url.split('/')[-1]
    repo = g.get_repo(repo_name)
    return repo

def collect_repo_data(repo):
    # Collect commits
    commits = repo.get_commits()
    commit_data = [{'sha': commit.sha, 'date': commit.commit.author.date} for commit in commits]

    # Collect pull requests
    pull_requests = repo.get_pulls(state='all')
    pr_data = [{'id': pr.id, 'state': pr.state, 'created_at': pr.created_at} for pr in pull_requests]

    # Collect issues
    issues = repo.get_issues(state='all')
    issue_data = [{'id': issue.id, 'state': issue.state, 'created_at': issue.created_at} for issue in issues]

    # Collect code reviews (can be derived from PR comments)
    code_reviews = []
    for pr in pull_requests:
        reviews = pr.get_reviews()
        for review in reviews:
            code_reviews.append({'pr_id': pr.id, 'state': review.state, 'submitted_at': review.submitted_at})

    return {
        'commits': commit_data,
        'pull_requests': pr_data,
        'issues': issue_data,
        'code_reviews': code_reviews
    }

import pandas as pd

def store_data_as_csv(data, file_name):
    # Create a DataFrame and store it
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)

# Example usage
repo_data = collect_repo_data(get_repo_data("https://github.com/surveysparrow/surveysparrow-android-sdk"))
store_data_as_csv(repo_data['commits'], 'commits.csv')
store_data_as_csv(repo_data['pull_requests'], 'pull_requests.csv')
store_data_as_csv(repo_data['issues'], 'issues.csv')
store_data_as_csv(repo_data['code_reviews'], 'code_reviews.csv')



