import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle

def visualize_metrics(metrics):
    st.title("Developer Performance Analytics Dashboard")

    # Create a compact layout with multiple columns and rows
    st.subheader("Performance Metrics Overview")

    # Check if metrics are available
    if not metrics:
        st.write("No metrics available. Please run the Metrics Calculation module first.")
        return

    # Row 1: Commits Per Day & PR Merge Rate
    col1, col2 = st.columns([1, 1])  # Two equally sized columns for the first row

    # Chart 1: Commits Per Day
    with col1:
        st.write("### Commits Per Day")
        commit_counts = metrics.get('Commit Frequency (commits/day)')
        if isinstance(commit_counts, pd.Series):
            commit_chart = px.bar(
                x=commit_counts.index,
                y=commit_counts.values,
                labels={'x': 'Date', 'y': 'Commits'},
                title="Commits Per Day",
                height=300
            )
            commit_chart.update_layout(
                xaxis_title="Date",
                yaxis_title="Commits",
                title_x=0.5
            )
            commit_chart.update_traces(marker_color='#636EFA')
            st.plotly_chart(commit_chart, use_container_width=True)

    # Chart 2: PR Merge Rate
    with col2:
        st.write("### PR Merge Rate")
        pr_merge_rate = metrics.get('PR Merge Rate (%)')
        if pr_merge_rate is not None:
            pr_merge_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pr_merge_rate,
                title={'text': "PR Merge Rate (%)"},
                gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#EF553B"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            pr_merge_gauge.update_layout(height=300, title_x=0.5)
            st.plotly_chart(pr_merge_gauge, use_container_width=True)

    # Row 2: Issue Resolution Time & PR Review Time
    col3, col4 = st.columns([1, 1])  # Two columns for the second row

    # Chart 3: Issue Resolution Time
    with col3:
        st.write("### Issue Resolution Time (days)")
        issue_resolution = metrics.get('Issue Resolution Time (days)')
        if isinstance(issue_resolution, pd.Series):
            issue_resolution_chart = px.bar(
                x=issue_resolution.index,
                y=issue_resolution.values,
                labels={'x': 'Issue', 'y': 'Resolution Time'},
                title="Issue Resolution Time",
                height=300
            )
            issue_resolution_chart.update_layout(
                xaxis_title="Issue",
                yaxis_title="Days",
                title_x=0.5
            )
            issue_resolution_chart.update_traces(marker_color='#00CC96')
            st.plotly_chart(issue_resolution_chart, use_container_width=True)

    # Chart 4: PR Review Time
    with col4:
        st.write("### PR Review Time (days)")
        pr_review_time = metrics.get('PR Review Time (days)')
        if pr_review_time is not None:
            pr_review_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pr_review_time,
                title={'text': "PR Review Time (days)"},
                gauge={'axis': {'range': [None, pr_review_time * 2]}, 'bar': {'color': "#AB63FA"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            pr_review_gauge.update_layout(height=300, title_x=0.5)
            st.plotly_chart(pr_review_gauge, use_container_width=True)

    # Row 3: Additional Metrics
    col5, col6 = st.columns([1, 1])  # Two columns for the third row

    # Chart 5: Code Churn Rate
    with col5:
        st.write("### Code Churn Rate")
        churn_rate = metrics.get('Code Churn Rate (%)')
        if churn_rate is not None:
            churn_pie = px.pie(
                names=["Churn", "No Churn"],
                values=[churn_rate, 100 - churn_rate],
                title="Code Churn Rate (%)",
                height=300
            )
            churn_pie.update_traces(marker=dict(colors=['#FF7F0E', '#2CA02C']))
            churn_pie.update_layout(title_x=0.5)
            st.plotly_chart(churn_pie, use_container_width=True)

    # Chart 6: Average Commit Size
    with col6:
        st.write("### Average Commit Size")
        avg_commit_size = metrics.get('Average Commit Size (message length)')
        if avg_commit_size is not None:
            commit_size_chart = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_commit_size,
                title={'text': "Avg Commit Size (chars)"},
                gauge={'axis': {'range': [None, avg_commit_size * 2]}, 'bar': {'color': "#19D3F3"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            commit_size_chart.update_layout(height=300, title_x=0.5)
            st.plotly_chart(commit_size_chart, use_container_width=True)

    # Footer
    st.write("### Summary")
    st.write("The dashboard provides an overview of various performance metrics for the developer. Use the sections above to explore the data in detail.")

def visu():
    pickle_file_path = 'path/to/metrics.pkl'  # Update this path to the correct location of your pickle file
    
    try:
        with open(pickle_file_path, 'rb') as file:
            metrics = pickle.load(file)
    except FileNotFoundError:
        st.error(f"File not found: {pickle_file_path}")
        return
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return
    
    visualize_metrics(metrics)
