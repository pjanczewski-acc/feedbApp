import openai
import json

# Load configuration from JSON file
with open("C:/Users/piotr.janczewski/Desktop/genAI/Test/config.json", mode="r") as f:
    config = json.load(f)

use_azure_active_directory = True  # Set this flag to True if you are using Azure Active Directory

if use_azure_active_directory:
    endpoint = config["AZURE_ENDPOINT"]
    api_key = config["AZURE_API_KEY"]

    from azure.identity import DefaultAzureCredential, get_bearer_token_provider

    client = openai.AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"),
        api_version="2023-09-01-preview"
    )

    deployment = "" # Fill in the deployment name from the portal here

    embeddings = client.embeddings.create(
        model=deployment,
        input="The food was delicious and the waiter..."
    )
                                    
    print(embeddings)
