import openai
import pandas as pd
import pickle
import os

# Set up OpenAI API key (use environment variables in practice)
openai.api_key = 'YOUR_API_KEY'  # Replace this with your actual API key

def load_metrics(pickle_file_path):
    try:
        with open(pickle_file_path, 'rb') as file:
            metrics = pickle.load(file)
    except FileNotFoundError:
        return None
    except Exception as e:
        return str(e)
    return metrics

def query_llm(question, metrics):
    # Prepare the prompt for LLM
    prompt = f"Given the following metrics data:\n\n{metrics}\n\nAnswer the following question: {question}"
    
    # Make API call to OpenAI's GPT
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use appropriate engine
        prompt=prompt,
        max_tokens=150
    )
    
    answer = response.choices[0].text.strip()
    return answer

def main():
    pickle_file_path = 'C:\Users\JOSHIK RAJ\AI-Powered Developer Performance\dev_performance_dashboard\metrics\metrics.pkl'  # Update this path to your metrics file
    metrics = load_metrics(pickle_file_path)
    
    if metrics is None:
        print("Metrics data not found.")
        return
    
    # Streamlit input for user's question
    user_question = input("Enter your question about the metrics: ")
    
    # Query the LLM
    answer = query_llm(user_question, metrics)
    
    print("Answer:", answer)
