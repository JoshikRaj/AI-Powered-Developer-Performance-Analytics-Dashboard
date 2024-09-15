import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle
import os

# Visualization function that creates the charts
def visualize_metrics(metrics):
    if not metrics:
        st.error("No metrics available. Please run the Metrics Calculation module first.")
        return

    st.markdown("## Developer Performance Metrics Dashboard")
    st.markdown("This dashboard displays various performance indicators for software developers based on data from GitHub.")
    
    # Use a consistent and appealing background color and text color through layout settings
    layout_settings = {
        'paper_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
        'plot_bgcolor': 'rgba(0,0,0,0)',   # Transparent background
        'font': {'color': '#517FA4'}       # A soothing blue font color
    }

    # Row 2: PR Merge Rate
    col2 = st.columns([1])[0]  # Single column for the second row
    with col2:
        st.markdown("### PR Merge Rate")
        pr_merge_rate = metrics.get('PR Merge Rate (%)')
        if pr_merge_rate is not None:
            pr_merge_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pr_merge_rate,
                title={'text': "PR Merge Rate (%)"},
                gauge={'axis': {'range': [None, 100], 'tickcolor': 'blue'}, 'bar': {'color': "#EF553B"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            pr_merge_gauge.update_layout(height=300, title_x=0.5, **layout_settings)
            st.plotly_chart(pr_merge_gauge, use_container_width=True)
        else:
            st.warning("No data available for 'PR Merge Rate (%)'.")

    # Row 3: Issue Resolution Time & PR Review Time
    col3, col4 = st.columns([1, 1])  # Two columns for the third row

    # Chart 3: Issue Resolution Time
    with col3:
        st.markdown("### Issue Resolution Time (days)")
        issue_resolution = metrics.get('Issue Resolution Time (days)')
        if isinstance(issue_resolution, pd.Series) and not issue_resolution.empty:
            issue_resolution_chart = px.bar(
                x=issue_resolution.index.astype(str),
                y=issue_resolution.values,
                labels={'x': 'Issue', 'y': 'Resolution Time'},
                title="Issue Resolution Time",
                height=300,
                color_discrete_sequence=['#00CC96']
            )
            issue_resolution_chart.update_layout(
                xaxis_title="Issue",
                yaxis_title="Days",
                title_x=0.5,
                **layout_settings
            )
            st.plotly_chart(issue_resolution_chart, use_container_width=True)
        else:
            st.warning("No data available for 'Issue Resolution Time (days)'.")

    # Chart 4: PR Review Time
    with col4:
        st.markdown("### PR Review Time (days)")
        pr_review_time = metrics.get('PR Review Time (days)')
        if isinstance(pr_review_time, pd.Series) and not pr_review_time.empty:
            avg_pr_review_time = pr_review_time.mean()  # Calculate the average
            pr_review_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_pr_review_time,
                title={'text': "PR Review Time (days)"},
                gauge={'axis': {'range': [None, avg_pr_review_time * 2]}, 'bar': {'color': "#AB63FA"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            pr_review_gauge.update_layout(height=300, title_x=0.5, **layout_settings)
            st.plotly_chart(pr_review_gauge, use_container_width=True)
        else:
            st.warning("No data available for 'PR Review Time (days)'.")

    # Row 4: Additional Metrics
    col5, col6 = st.columns([1, 1])  # Two columns for the fourth row

    # Chart 5: Code Churn Rate
    with col5:
        st.markdown("### Code Churn Rate")
        churn_rate = metrics.get('Code Churn Rate (%)')
        if churn_rate is not None:
            churn_pie = px.pie(
                names=["Churn", "No Churn"],
                values=[churn_rate, 100 - churn_rate],
                title="Code Churn Rate (%)",
                height=300,
                color_discrete_sequence=['#FF7F0E', '#2CA02C']
            )
            churn_pie.update_traces(marker=dict(colors=['#FF7F0E', '#2CA02C']))
            churn_pie.update_layout(title_x=0.5, **layout_settings)
            st.plotly_chart(churn_pie, use_container_width=True)
        else:
            st.warning("No data available for 'Code Churn Rate (%)'.")

    # Chart 6: Average Commit Size
    with col6:
        st.markdown("### Average Commit Size")
        avg_commit_size = metrics.get('Average Commit Size (message length)')
        if avg_commit_size is not None:
            commit_size_chart = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_commit_size,
                title={'text': "Avg Commit Size (chars)"},
                gauge={'axis': {'range': [None, avg_commit_size * 2]}, 'bar': {'color': "#19D3F3"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            commit_size_chart.update_layout(height=300, title_x=0.5, **layout_settings)
            st.plotly_chart(commit_size_chart, use_container_width=True)
        else:
            st.warning("No data available for 'Average Commit Size (message length)'.")

    # Footer with a clear and engaging call to action or summary
    st.markdown("### Summary")
    st.info("The dashboard provides an overview of various performance metrics for developers. Explore the sections above for detailed insights and make informed decisions to improve development processes.")

def visu():
    metrics_pkl_path = 'dev_performance_dashboard/metrics/metrics.pkl'
    if os.path.exists(metrics_pkl_path):
        # Load the metrics data from the pickle file
        with open(metrics_pkl_path, 'rb') as f:
            metrics = pickle.load(f)
        # Pass the loaded metrics data to visualize_metrics
        visualize_metrics(metrics)
    else:
        st.write("Metrics file not found. Please make sure the file exists at the specified path.")

# Run the app
if __name__ == '__main__':
    visu()
