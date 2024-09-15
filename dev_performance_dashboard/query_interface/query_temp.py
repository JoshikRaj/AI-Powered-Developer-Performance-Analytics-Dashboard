import cohere
import os
import streamlit as st
import pandas as pd

#Setting 
cohere_api_key = 'ngcsi3x9Yf5delGbRpFwhYrLsR1A2FN7SeQEsYkK'
cohere_client = cohere.Client(cohere_api_key)

# Define the function to interact with the Cohere API
def query_cohere_api(user_query):
    try:
        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=f"You are a helpful assistant. The user asked: {user_query}",
            max_tokens=150,
            temperature=0.7,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error querying the Cohere API: {str(e)}"

# Define the natural language query function
def natural_language_query_module(metrics):
    st.write("### Natural Language Query")

    # Get user input
    user_query = st.text_input("Ask a question about developer performance:")
    
    if user_query:
        # Query Cohere API
        response = query_cohere_api(user_query)
        st.write(f"**Cohere Response:** {response}")

        # Extract the metric name and value from the response
        relevant_metric = None
        for metric_key in metrics.keys():
            if metric_key.lower() in response.lower():
                relevant_metric = metric_key
                break

        if relevant_metric:
            st.write(f"**Metric:** {relevant_metric}")
            metric_value = metrics.get(relevant_metric)
            if isinstance(metric_value, (int, float)):
                st.write(f"**Value:** {metric_value:.2f}")
            elif isinstance(metric_value, pd.Series):
                st.write(f"**Values:**")
                st.write(metric_value)
            else:
                st.write(f"**Value:** {metric_value}")
        
