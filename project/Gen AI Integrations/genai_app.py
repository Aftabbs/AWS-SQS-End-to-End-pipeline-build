from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer 
from transformers import TrainingArguments 
from unsloth import is_bfloat16_supported
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os 
from dot_env import load_dot_env
load_dot_env()
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="API-KEY"
)

def validate_and_transform_order(order_data):
    """
    Validate and transform order data using the GenAI model.
    Args:
        order_data (dict): The order data to validate and transform.
    Returns:
        dict: The parsed response content from the GenAI model.
    """
    prompt = f"""
    You are a data validation assistant. Validate the following order data:
    {json.dumps(order_data, indent=2)}

    Tasks:
    1. Ensure 'user_id', 'order_id', and 'order_value' are present and correctly typed.
    2. Verify 'order_value' equals the sum of (quantity * price_per_unit) for all items. If not, suggest corrections.
    3. Extract the fields 'user_id', 'order_value', and 'order_timestamp'.
    4. Highlight any errors or inconsistencies and propose fixes.
    Provide your response in JSON format.
    """
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024
    )

    response_content = completion.choices[0].message.content
    return response_content

input_file_path = "synthetic_order_data.json"
output_file_path = "validated_order_data.json"

with open(input_file_path, "r") as infile:
    orders = json.load(infile)

output_data = []
for order in orders:
    raw_response = validate_and_transform_order(order)
    output_data.append({
        "original_order": order,
        "genai_response": raw_response
    })

with open(output_file_path, "w") as outfile:
    json.dump(output_data, outfile, indent=2)

print(f"Validated data has been saved to {output_file_path}")
