import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle
import os
import numpy as np

class Visualizer:

    def __init__(self):
        # Defining the required variables
        self.metrics_data_path = None
        self.metrics = None

    # Method to set the path
    def set_path(self, path):
        self.metrics_data_path = path

    # Method that creates the charts
    def visualize_metrics(self):
        if not self.metrics:
            st.error("No metrics available. Please run the Metrics Calculation module first.")
            return

        # Title and description for the dashboard
        st.markdown("## Developer Performance Metrics Dashboard")
        st.markdown("A Streamlit-based dashboard that provides insights into developer performance using data from an open-source GitHub repository")

        # Adding some layout for the dashboard
        layout_settings = {
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
            'plot_bgcolor': 'rgba(0,0,0,0)',   # Transparent background
            'font': {'color': '#517FA4'}       # A soothing blue font color
        }

        # 3D Metrics Relationship Chart
        self.visualize_3d_metrics()  # Call 3D visualization first

        # PR Merge Rate Gauge
        st.markdown("### PR Merge Rate")
        pr_merge_rate = self.metrics.get('PR Merge Rate (%)')
        if pr_merge_rate is not None:
            # Create a gauge chart for PR Merge Rate
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

        # Issue Resolution Time and PR Review Time
        col3, col4 = st.columns([1, 1])  # Two columns for the third row

        # Issue Resolution Time
        with col3:
            st.markdown("### Issue Resolution Time (days)")
            issue_resolution = self.metrics.get('Issue Resolution Time (days)')
            if isinstance(issue_resolution, pd.Series) and not issue_resolution.empty:
                # Create a bar chart for Issue Resolution Time
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

        # PR Review Time
        with col4:
            st.markdown("### PR Review Time (days)")
            pr_review_time = self.metrics.get('PR Review Time (days)')
            if isinstance(pr_review_time, pd.Series) and not pr_review_time.empty:
                avg_pr_review_time = pr_review_time.mean()  # Calculate the average
                # Create a gauge chart for PR Review Time
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

        # Additional Metrics
        col5, col6 = st.columns([1, 1])  # Two columns for the fourth row

        # Code Churn Rate
        with col5:
            st.markdown("### Code Churn Rate")
            churn_rate = self.metrics.get('Code Churn Rate (%)')
            if churn_rate is not None:
                # Create a pie chart for Code Churn Rate
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

        # Average Commit Size
        with col6:
            st.markdown("### Average Commit Size")
            avg_commit_size = self.metrics.get('Average Commit Size (message length)')
            if avg_commit_size is not None:
                # Create a gauge chart for Average Commit Size
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

    def visualize(self):
        if self.metrics_data_path and os.path.exists(self.metrics_data_path):
            # Load the metrics data from the pickle file
            with open(self.metrics_data_path, 'rb') as f:
                self.metrics = pickle.load(f)
            # Pass the loaded metrics data to visualize_metrics
            self.visualize_metrics()
        else:
            st.write("Metrics file not found. Please check the specified path.")

    # Define 3D Metrics Relationship Chart method
    def visualize_3d_metrics(self):
        st.markdown("### 3D Metrics Relationship Chart")

        pr_merge_rate = self.metrics.get('PR Merge Rate (%)')
        churn_rate = self.metrics.get('Code Churn Rate (%)')
        avg_commit_size = self.metrics.get('Average Commit Size (message length)')

        if pr_merge_rate is not None and churn_rate is not None and avg_commit_size is not None:
            # Prepare 3D scatter data
            fig = go.Figure(data=[go.Scatter3d(
                x=[pr_merge_rate],  # PR Merge Rate on the x-axis
                y=[churn_rate],     # Code Churn Rate on the y-axis
                z=[avg_commit_size],  # Avg Commit Size on the z-axis
                mode='markers',
                marker=dict(
                    size=15,
                    color=pr_merge_rate,  # Color based on PR Merge Rate
                    colorscale='Portland',  # Color scale for appeal
                    showscale=True,  # Display color scale
                    colorbar=dict(
                        title="PR Merge Rate (%)",
                        tickvals=[0, 25, 50, 75, 100],
                        ticktext=['Low', 'Moderate', 'Average', 'High', 'Excellent'],
                    ),
                    opacity=0.8
                )
            )])

            # Update layout for 3D plot
            fig.update_layout(
                title="3D Relationship between PR Merge Rate, Code Churn, and Avg Commit Size",
                scene=dict(
                    xaxis_title="PR Merge Rate (%)",
                    yaxis_title="Code Churn Rate (%)",
                    zaxis_title="Avg Commit Size (chars)",
                    xaxis=dict(
                        backgroundcolor="rgb(200, 200, 230)",
                        gridcolor="white",
                        showbackground=True,
                        zerolinecolor="white"
                    ),
                    yaxis=dict(
                        backgroundcolor="rgb(230, 200,230)",
                        gridcolor="white",
                        showbackground=True,
                        zerolinecolor="white"
                    ),
                    zaxis=dict(
                        backgroundcolor="rgb(230, 230,200)",
                        gridcolor="white",
                        showbackground=True,
                        zerolinecolor="white"
                    ),
                ),
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for 3D metrics visualization.")
