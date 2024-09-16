# AI-Powered Developer Performance Analytics Dashboard

## Objective
To develop a Streamlit-based dashboard that provides insights into developer performance using data from an open-source GitHub repository. The system focuses on collecting and analyzing GitHub data, calculating performance metrics, and implementing a natural language interface for querying these metrics.

## Methodology 
- Data such as issues, pull requests, and commits were collected using the GitHub API.
- The data collected from the data collection module was loaded into Pandas DataFrames using helper functions. Based on this data, performance metrics were calculated for the repository.
- An interactive dashboard was created using the Plotly visualization library integrated within a Streamlit application.
- Cohere's advanced API processed user queries, providing relevant results based on the repository's data.

## Project Planning
The Trello project management tool was used to track project progress.  
[Trello link](https://trello.com/b/UvfeIOST/pro-dev-performance-dashboard)

## GitHub Repository 
[GitHub Repository](https://github.com/JoshikRaj/AI-Powered-Developer-Performance-Analytics-Dashboard.git)

## Key Findings
- Performed data collection by fetching URLs from multiple repositories.
- The system effectively fetched all the data about the given repository URL.
- Calculated metrics, such as Commit Frequency, Total Commits, PR Merge Rate, Issue Resolution Time (days), PR Review Time (days), Code Churn Rate, Average Commit Size, and Open-to-Closed Issues Ratio, were visualized clearly and represented in the dashboard.
- The NLP Module successfully responded to user queries, integrating the calculated metrics with LLMs to retrieve details from the requested repositories.
- Cohere’s advanced API was used for fast retrieval of complex queries.
- Data was stored using pickle, offering advantages over CSV files. The pickle file can be converted to CSV using a DataFrame.
- When analyzing successive URLs, data from the previous URLs is overwritten instead of creating multiple files.
- Error handling: Test cases were checked and handled, with unit testing, functionality testing, and exception handling performed.

## Recommendations (TO DO)
1. Expand the data size by accessing high-complexity repositories like **ultralytics**.
2. Implement more secure methods for storing API keys.
3. Enable processing of multiple URLs for the last three modules.

## Conclusion
This AI-powered Developer Performance Dashboard provides project managers and team leads with actionable insights to track and optimize developer productivity. By visualizing key metrics like PR merge rates, issue resolution times, and code churn, it empowers teams to make data-driven decisions. This tool seamlessly integrates with real-world scenarios, fostering continuous improvement and team efficiency.
