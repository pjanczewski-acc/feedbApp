"""
Created on Wed Apr 3 12:12:00 2024

@author: piotr.janczewski
"""

from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import json
import openai

# Load configuration from JSON file
with open("config.json", mode="r") as f:
    config = json.load(f)

client = openai.AzureOpenAI(
        azure_endpoint=config["AZURE_ENDPOINT"],
        api_key= config["AZURE_API_KEY"],
        api_version="2023-12-01-preview")

st.set_page_config(page_title="Feedback App",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

##############
# Functions
##############

# Function to filter feedback based on time
def filter_feedback(feedback_table, months_back_val):
    delta = timedelta(days=months_back_val * 30)
    threshold_date = datetime.now() - delta
    filtered_feedback = feedback_table[feedback_table['Date'] >= threshold_date]
    return filtered_feedback

# Function to generate feedback scenario using Language Model
def generate_feedback_scenario(filtered_feedback, prompt_feed):

    scenario = []
    feedback = ''
    
    prompt = prompt_feed
    
    for _, entry in filtered_feedback.iterrows():
        feedback += entry['Feedback']

    messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": feedback}
            ]

    response= client.chat.completions.create(
            messages=messages,
            model="PiotrJ_feedback",
            temperature=0,
            seed=445566)
    
    scenario= response.choices[0].message.content

    return scenario

def main_page():

    output = ''

    # Display the images in the header next to each other
    st.image("images/feedback.png")

    col1, col2 = st.columns(2)
    with col1:
        st.write('')
        st.write("Input individual feedbacks to produce discussion scenario")
    with col2:
        st.image("images/clifton.png")

    with st.form("Feedback summary", clear_on_submit=False):

        gen_prompt = "You are a thoughtful manager." + \
            "Based on several pieces of individual feedback " + \
            "you want to draft a scenario of feedback summary for your subordinate." + \
            "The scenario should be composed in bullet points, " + \
            "max 2500 characters, and contain three main sections: " + \
            "    1. positive achievements (what went well)" + \
            "    2. area of opportunity (what to improve)" + \
            "    3. key strengths to build on in future (what seems the best in the subordinate)." + \
            "Generate feedback scenario for employee based on received feedback"

        Clj_prompt = "Additionally, incorporate in the final feedback " + \
                    "CliftonStrength profile of the subordinate" + \
                    "Remember to interpret stregnth definition and focus on top 15 ranks " + \
                    "as per Gallup CliftonStrength framework." + \
                    "Consider interactions between different strengths." + \
                    "For positive achievements and key strengths, " + \
                    "indicate (if adequate) relevant talents and their interactions." + \
                    "For example: 'your success here probably results from your Clifton strength in ...'." + \
                    "For area of opportinity, check and report if any of 5-10 Strngths " + \
                    "can be used to overcome the difficulty. " + \
                    "If none of top 10 strengths seems applicable for given problem, " + \
                    "provide recommendation of Strengths to look among colleagues vto be paired with." + \
                    "For example: 'Your Harmony and Consistency would work great if you are paired a person strong in Command." + \
                    "Here are the CliftonStrengths ranks of the subordinate to incorporate in the feedback."

        Cls_prompt = "Also, incorporate in the final feedback " + \
                    "my CliftonStrength profile" + \
                    "so that I know which my strengths to guide my junior with" + \
                    "to help hium/her strengthen his/her strengths " + \
                    "and overcome difficulties (if any)." + \
                    "Consider especially those strenghts of mine which " + \
                    "are described to pair well with subordinate's strengths." + \
                    "Do not list back all my strengths. Just those relevant for the feedback." + \
                    "Here are my CliftonStrengths ranks."
        
        # Add a file uploader widget
        feedback_file = st.file_uploader("Upload Excel file with individual feedbacks from WD", type=["xls", "xlsx"])

        col1, col2 = st.columns(2)
        with col1:
            Clifton_junior_file = st.file_uploader("Upload JUNIOR's Clifton ranks", type=["txt", "csv"])
            subordinate_name_initial = st.text_input("Counselee name", value="")
        with col2:
            Clifton_senior_file = st.file_uploader("Upload YOUR Clifton ranks", type=["txt", "csv"])
            subordinate_surname_initial = st.text_input("Counselee surname", value="")

        with st.expander("Your prompt"):
            gen_prompt_feed = st.text_area("Main part (obligatory), edit if adequate", value = gen_prompt)
            Clj_prompt_feed = st.text_area("Clifton junior part (optional), edit if adequate", value = Clj_prompt)
            Cls_prompt_feed = st.text_area("Clifton senior part (optional), edit if adequate", value = Cls_prompt)

        months_back_val = st.slider("How old feedback to include: 0=latest, 24=Up to 2Y",
                              min_value=0, max_value=24, value=12)
        st.write("")
                
        # Premilinary listing before final export
        
        produce = st.form_submit_button("Produce feedback scenario")

        if produce:
            
            # Read feedback table from Excel file
            if feedback_file is not None:
                # Read the Excel file into a pandas DataFrame
                feedback_table = pd.read_excel(feedback_file, parse_dates=['Date'], skiprows=1)
                prompt_feed = gen_prompt_feed

            # Read Clifton ranks from text file
            if Clifton_junior_file is not None:
                # Read the Excel file into a pandas DataFrame
                Clifton_junior_table = pd.read_csv(Clifton_junior_file, header=None)
                Clj_prompt_feed += Clifton_junior_table.iloc[:,0].to_string(index=False).replace('\n', '')
                prompt_feed += Clj_prompt_feed

            # Read Clifton ranks from text file
            if Clifton_senior_file is not None:
                # Read the Excel file into a pandas DataFrame
                Clifton_senior_table = pd.read_csv(Clifton_senior_file, header=None)
                Cls_prompt_feed += Clifton_senior_table.iloc[:,0].to_string(index=False).replace('\n', '')
                prompt_feed += Cls_prompt_feed

            # Filter feedback
            filtered_feedback = filter_feedback(feedback_table, months_back_val)

            # Generate feedback scenario
            scenario = generate_feedback_scenario(filtered_feedback, prompt_feed)
            st.write("")
            st.write(scenario)
            st.write("")

    with st.expander("Where to get the input files from?"):
        st.write("For the feedback file, log in to Workday," + 
                    "in the 'Feedback Received' section click on" +
                    "'Export to Excel' in top right corner")
        st.image('images/export.png', caption='example')
        st.write("")
        st.write("For CliftonStrengths, create csv, txt or xls file with the list from 1 to 5, 10, 15 or all 34")
        example = open('example_Clifton.txt', 'r').read()
        st.download_button("Download Example Clifton File", data = example, file_name='example_Clifton.txt', mime='text/csv')

    # Save feedback scenario to a text file
    if produce:
        output = str(scenario).replace('\\n', '\n').replace('\\t', '\t')
        output_file_name = f"{subordinate_name_initial} {subordinate_surname_initial} - feedback scenario script.txt"
        st.download_button('Download feedback scenario', data = output, file_name=output_file_name, mime='text/csv')

    st.write("https://www.youtube.com/watch?v=WNnzw90vxrE of this form")

        
##############
# PAGE SET UP
##############

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

main_page()

