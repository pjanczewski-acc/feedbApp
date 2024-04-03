import pandas as pd
from datetime import datetime, timedelta
import openai
import json

# Load configuration from JSON file
with open("C:/Users/piotr.janczewski/Desktop/genAI/Test/config.json", mode="r") as f:
    config = json.load(f)

# Function to filter feedback based on time
def filter_feedback(feedback_table, months_back):
    delta = timedelta(days=months_back * 30)
    threshold_date = datetime.now() - delta
    filtered_feedback = feedback_table[feedback_table['Date'] >= threshold_date]
    return filtered_feedback

# Function to generate feedback scenario using Language Model
def generate_feedback_scenario(filtered_feedback, word_limit=None):
    scenario = []

    for _, entry in filtered_feedback.iterrows():
        feedback = entry['Feedback']
        # Use OpenAI's GPT model to generate context-aware feedback
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Generate feedback scenario for employee based on received feedback: \"{feedback}\"",
            temperature=0.7,
            max_tokens=100
        )
        scenario.append(response.choices[0].text.strip())

    # Truncate feedback scenario if word limit is specified
    if word_limit is not None:
        word_count = sum(len(item.split()) for item in scenario)
        if word_count > word_limit:
            scenario = [" ".join(scenario)[:word_limit] + " [Truncated due to word limit]"]

    return scenario

def main():
    openai.api_key = config["AZURE_API_KEY"]

    file_path = "C:/Users/piotr.janczewski/Desktop/genAI/Test/Ramon Puls.xlsx"
    subordinate_name = "Ramon"
    subordinate_surname = "Puls"
    months_back = 12
    word_limit = 2500

    # Read feedback table from Excel file
    feedback_table = pd.read_excel(file_path, parse_dates=['Date'], skiprows=1)

    # Filter feedback
    filtered_feedback = filter_feedback(feedback_table, months_back)

    # Generate feedback scenario
    scenario = generate_feedback_scenario(filtered_feedback, word_limit)

    # Save feedback scenario to a text file
    output_file_name = f"{subordinate_name} {subordinate_surname} - feedback scenario script.txt"
    output_file_path = file_path.rsplit("/", 1)[0] + "/" + output_file_name
    with open(output_file_path, "w") as file:
        for item in scenario:
            file.write(item + "\n")

    print(f"Feedback scenario saved to: {output_file_path}")

if __name__ == "__main__":
    main()
