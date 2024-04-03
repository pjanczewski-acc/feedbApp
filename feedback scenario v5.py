import pandas as pd
from datetime import datetime, timedelta
import openai
import json

# Load configuration from JSON file
with open("C:/Users/piotr.janczewski/Desktop/genAI/Test/config.json", mode="r") as f:
    config = json.load(f)

client = openai.AzureOpenAI(
        azure_endpoint=config["AZURE_ENDPOINT"],
        api_key= config["AZURE_API_KEY"],
        api_version="2023-12-01-preview")

# Function to filter feedback based on time
def filter_feedback(feedback_table, months_back):
    delta = timedelta(days=months_back * 30)
    threshold_date = datetime.now() - delta
    filtered_feedback = feedback_table[feedback_table['Date'] >= threshold_date]
    return filtered_feedback

# Function to generate feedback scenario using Language Model
def generate_feedback_scenario(filtered_feedback):
    scenario = []
    feedback = []

    prompt = "You are a thoughtful manager. Based on several pieces of individual feedback, \
                you want to draft a scenario of feedback summary for your subordinate. \
                The scenario should be composed in bullet points, max 2500 characters, \
                and contain three main sections: \
                    1. positive achievements (what went well), \
                    2. area of oppurtunity (what to improve) \
                    3. key strengths to build on in future (what seems the best in the subordinate) \
                Generate feedback scenario for employee based on received feedback:"
    
    for _, entry in filtered_feedback.iterrows():
        feedback.append(entry['Feedback'])

    messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": feedback}
            ]

    response= client.chat.completions.create(
            messages=messages,
            model="PiotrJ_feedback",
            temperature=0,
            seed=445566)
    
    scenario = response.choices[0].message.content

    return scenario

def main():

    file_path = "C:/Users/piotr.janczewski/Desktop/genAI/Test/Ramon Puls.xlsx"
    subordinate_name = "Ramon"
    subordinate_surname = "Puls"
    months_back = 12

    # Read feedback table from Excel file
    feedback_table = pd.read_excel(file_path, parse_dates=['Date'], skiprows=1)

    # Filter feedback
    filtered_feedback = filter_feedback(feedback_table, months_back)

    # Generate feedback scenario
    scenario = generate_feedback_scenario(filtered_feedback)

    # Save feedback scenario to a text file
    output_file_name = f"{subordinate_name} {subordinate_surname} - feedback scenario script.txt"
    output_file_path = file_path.rsplit("/", 1)[0] + "/" + output_file_name
    with open(output_file_path, "w") as file:
        for item in scenario:
            file.write(item + "\n")

    print(f"Feedback scenario saved to: {output_file_path}")

if __name__ == "__main__":
    main()
