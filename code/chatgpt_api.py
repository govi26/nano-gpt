import os
import openai
import requests


API_KEY = "<API_KEY>"
API_URL = "https://api.openai.com/v1/chat/completions"
openai.organization = "<ORG_ID>"
openai.api_key = API_KEY

# print(openai.Model.list())

# data = {
#   "model": "gpt-3.5-turbo",
#   "messages": [{"role": "user", "content": "code to number of unique words in a file"}],
#   "temperature": 0.7
# }
# headers = {
#   "Content-Type": "application/json",
#   "Authorization": f"Bearer {API_KEY}"
# }

# response = requests.post(API_URL, headers=headers, json=data)
# response_data = response.json()

# print(response_data['choices'][0]['message']['content'])


# Set the model to use
# model = "gpt-3.5-turbo"

# # Set the programming language to use
# language = "python"

# # Generate code
# code = openai.ChatCompletion.create(
#     model=model,
#     messages=[{"role": "user", "content": "code to reverse a linked list"}]
# )

# # Print the code
# print(code)

# response = openai.ChatCompletion.create(
#     engine="text-davinci-003",  # or another suitable model
#     prompt="Interpret the following command for a genomic data analysis platform and provide the action and parameters in a structured format: 'start analysis on sample 123 with pipeline 5'.",
#     max_tokens=100,
# )

from openai import OpenAI

client = OpenAI(
    api_key=API_KEY,
)

chat_completion = client.completions.create(
    prompt=(
        "Parse the following command for a genomic data analysis platform and list the details. Make sure to identify the 'Action', 'Sample ID', 'Pipeline ID', and 'Project ID': 'start analysis on sample 123 with pipeline 5 in project 14'."
    ),
    model="gpt-3.5-turbo-instruct",
)
print(chat_completion.choices[0])
