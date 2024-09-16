import cohere
import os
import streamlit as st
import pandas as pd
import pickle

class NLPModule:
    def __init__(self):
        
        # API key to access Cohere's advanced API
        self.cohere_api_key = 'ngcsi3x9Yf5delGbRpFwhYrLsR1A2FN7SeQEsYkK'
        self.cohere_client = cohere.Client(self.cohere_api_key)
        self.metrics = None
        self.metrics_data_path = None

    def set_path(self, path):
        self.metrics_data_path = path

    def get_metrics(self):
        try:
            with open(self.metrics_data_path, 'rb') as file:
                self.metrics = pickle.load(file)
        except FileNotFoundError:
            st.error(f"File not found: {self.metrics_data_path}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Method to format metrics ( pandas -> String)
    def format_context(self):
        context = "The following are the performance metrics for developers:\n"
        if self.metrics:
            for key, value in self.metrics.items():
                if isinstance(value, pd.Series):
                    value_str = value.to_string()
                else:
                    value_str = str(value)
                context += f"{key}: {value_str}\n"
        return context

    # Method to query the Cohere API with a user query
    def query_cohere_api(self, user_query):
        context = self.format_context()
        prompt = f"{context}\n\nYou are a helpful assistant. The user asked: {user_query}"
        try:
            response = self.cohere_client.generate(
                model='command-xlarge-nightly', # Model to use for generating text
                prompt=prompt,
                max_tokens=150, # Max No.Of. tokens
                temperature=0.7, # To control the randomness
            )
            return response.generations[0].text.strip()
        except Exception as e:
            return f"Error querying the Cohere API: {str(e)}" # Error handling for API issues

    def natural_language_query_module(self):
        self.get_metrics() # Load the metrics data

         # Display section header
        # Get user input
        user_query = st.text_input("Ask a question about developer performance:")
        
        if user_query:
            # Query Cohere API
            response = self.query_cohere_api(user_query)
            st.write(f"**Cohere Response:** {response}")

            # Attempt to extract metrics from the response 
            relevant_metric = None
            for metric_key in self.metrics.keys():
                if metric_key.lower() in response.lower():
                    relevant_metric = metric_key
                    break
            # Extract relevant metrics from the response
            if relevant_metric:
                st.write(f"**Metric:** {relevant_metric}")
                metric_value = self.metrics.get(relevant_metric)
                if isinstance(metric_value, (int, float)):
                    st.write(f"**Value:** {metric_value:.2f}")
                elif isinstance(metric_value, pd.Series):
                    st.write(f"**Values:**")
                    st.write(metric_value)
                else:
                    st.write(f"**Value:** {metric_value}")
