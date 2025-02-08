from datetime import datetime

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
# from dotenv import load_dotenv
import openai
from openai import OpenAIError
import os
import re
import json
import time
import subprocess
import sys
from github import Github


logging.basicConfig(level=logging.INFO)

# Load .env file
# load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key is missing!")
logging.info(f"Loaded OpenAI API key: {api_key[:4]}******")

# GitHub authentication
github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    print("Error: GITHUB_TOKEN environment variable not set")
    sys.exit(1)

# Repository details
repo_name = "ashutosh-mishra/IntelliopsBackend"

# Initialize OpenAI client
openai.api_key = api_key

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class ApiJson(BaseModel):
    json_input: Dict[str, Any]

class ApiJsonSchema(BaseModel):
    schema: Dict[str, Any]

@app.post("/generate-tests")
async def generate_tests(api_json: ApiJson):
    logging.info(f"Received JSON: {api_json.json_input}")
    try:
        # Generate the prompt
        prompt = (
            "You are a test generation assistant. Generate detailed integration tests in Python "
            "for the following API JSON specification. Include all methods and paths. "
            "Also, generate workflow tests where APIs are interdependent:\n\n"
            "Output should be in python format, dont add any explanatory text like here is a Python script or ``` or python, etc"
            f"{api_json.json_input}"
        )

        tests = call_openai_with_retry(prompt)
        print("generated tests: ", tests)
        generated_tests_code = extract_python_code(tests)
        print("generated tests: ", generated_tests_code)


        date_time = get_current_time()
        gen_tests_name = f"gen_tests_{date_time}" + ".py"
        gen_test_file_path = "./artifacts/generated_tests/" + gen_tests_name
        with open(gen_test_file_path, "w+") as f:
            f.write(generated_tests_code)

        commit_github_and_raise_pr_for_tests("generated-tests-" + date_time)

        return {"tests": generated_tests_code}

    except Exception as e:
        logging.error(f"Error generating tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def validate_schema(schema: Dict[str, Any]) -> bool:
    """Validate the input schema."""
    try:
        if "type" not in schema or schema["type"] != "object":
            raise ValueError("Schema must be an object type.")
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            raise ValueError("Properties must be a dictionary.")
        for key, value in properties.items():
            if not isinstance(value, dict) or "type" not in value:
                raise ValueError(f"Invalid property definition for '{key}': {value}")
        return True
    except Exception as e:
        logging.error(f"Schema validation error: {e}")
        return False

def get_current_time():
    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    return date_time

@app.post("/stream-generate-datasets")
async def generate_datasets(api_schema: ApiJsonSchema):

    if not validate_schema(api_schema.schema):
        raise HTTPException(status_code=400, detail="Invalid schema format")

    datasets = []  # Collect all datasets
    try:
        for i in range(10):  # Generate 10 datasets
            dataset = generate_dataset_with_gpt4(api_schema.schema, i)
            datasets.append(dataset)
    except Exception as e:
        logging.error(f"Error generating datasets: {e}")
        raise HTTPException(status_code=500, detail="Error generating datasets")

    print("generated datasets: ", datasets)

    date_time = get_current_time()
    ds_name = f"datasets_{date_time}" + ".json"
    ds_file_path = "./artifacts/datasets/" + ds_name
    with open(ds_file_path, "w+") as f:
      json.dump(datasets, f, indent=4)

    commit_github_and_raise_pr_for_tests("generated-datasets-" + date_time)

    print("Committing changes in branch")
    return JSONResponse(content={"datasets": datasets})

def call_openai_with_retry(prompt: str) -> str:
    max_retries = 5
    retry_delay = 1  # Initial delay in seconds

    for attempt in range(max_retries):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a dataset generation assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()

        except OpenAIError as e:  # Catch all OpenAI-specific exceptions
            logging.warning(f"OpenAI error: {e}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1})")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        except Exception as e:
            logging.error(f"Unexpected error during OpenAI API call: {e}")
            if attempt == max_retries - 1:
                raise e

    raise Exception("Exceeded maximum retries for OpenAI API")

def generate_dataset_with_gpt4(schema: Dict[str, Any], index: int) -> Dict[str, Any]:
    try:
        # Prompt GPT-4 to generate datasets
        prompt = (
            f"You are a dataset generation assistant. Based on the following API schema, "
            f"generate one valid positive example that matches the schema "
            f"and one invalid negative example:\n\nSchema:\n{json.dumps(schema)}\n\n"
            f"Positive Example:\n(Provide a JSON object matching the schema)\n\n"
            f"Negative Example:\n(Provide a JSON object that violates the schema, such as missing required fields or having invalid types)"
        )

        output = call_openai_with_retry(prompt)

        # Function to safely extract JSON from a block
        def extract_json_block(text, key):
            try:
                start_idx = text.find(key) + len(key)
                if start_idx < len(key):  # Key not found
                    return None
                if "```json" in text[start_idx:]:
                    start_idx = text.find("```json", start_idx) + len("```json")
                    end_idx = text.find("```", start_idx)
                    return json.loads(text[start_idx:end_idx].strip())
                elif "```" in text[start_idx:]:
                    start_idx = text.find("```", start_idx) + len("```")
                    end_idx = text.find("```", start_idx)
                    return json.loads(text[start_idx:end_idx].strip())
                else:
                    start_idx = text.find("{", start_idx)
                    end_idx = text.find("}", start_idx) + 1
                    return json.loads(text[start_idx:end_idx].strip())
            except Exception as e:
                logging.error(f"Error extracting JSON block for {key}: {e}")
                return None

        # Extract positive and negative examples
        positive_dataset = extract_json_block(output, "Positive Example:")
        negative_dataset = extract_json_block(output, "Negative Example:")

        if positive_dataset is None or negative_dataset is None:
            raise ValueError("Failed to parse datasets from GPT-4 response")

        return {
            "positive_dataset": positive_dataset,
            "negative_dataset": negative_dataset,
        }

    except Exception as e:
        logging.error(f"Error processing GPT-4 response: {e}")
        return {
            "positive_dataset": {"error": "Failed to generate positive dataset"},
            "negative_dataset": {"error": "Failed to generate negative dataset"},
        }



def extract_python_code(llm_response):
    # Regular expression to match Python code blocks
    pattern = r'```python\s*([\s\S]*?)\s*```'
    
    # Find all matches in the LLM response
    matches = re.findall(pattern, llm_response, re.MULTILINE)
    
    code_str = ""
    for line in matches:
        code_str += line

    # Return the extracted Python code snippets
    return code_str

def commit_github_and_raise_pr_for_tests(branch_name):
    branch_name = branch_name.replace(":", "")

    # Commit the generated files to the repository
    os.system("git checkout -b " + branch_name)
    os.system("git add ./artifacts/generated_tests")
    os.system("git commit -m 'Add generated tests'")

    os.system("git push origin " + branch_name)

    pr_title = "Generated tests artifacts - integration tests"
    pr_body = "This PR contains the generated tests artifacts."

    g = Github(github_token)
    repo = g.get_repo(repo_name)

    repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base="main")

    logging.info("Generated files committed and PR created successfully.")

    logging.info("Switching back to main branch")
    os.system("git checkout main")


def commit_github_and_raise_pr_for_datasets(branch_name):
    branch_name = branch_name.replace(":", "")

    # Commit the generated files to the repository
    os.system("git checkout -b " + branch_name)
    os.system("git add ./artifacts/datasets")
    os.system("git commit -m 'Add generated datasets'")
    os.system("git push origin " + branch_name)

    pr_title = "Generated tests artifacts - datasets"
    pr_body = "This PR contains the generated dataset artifacts."

    g = Github(github_token)
    repo = g.get_repo(repo_name)

    repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base="main")

    logging.info("Generated files committed and PR created successfully.")

    logging.info("Switching back to main branch")
    os.system("git checkout main")