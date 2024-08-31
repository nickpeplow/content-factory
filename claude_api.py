import os
import requests
import time
from dotenv import load_dotenv

print("claude_api.py is being imported")

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL")

# Add these constants after loading the environment variables
REQUESTS_PER_MINUTE = int(os.getenv("CLAUDE_REQUESTS_PER_MINUTE", "50"))
RATE_LIMIT_DELAY = 60 / REQUESTS_PER_MINUTE

last_request_time = 0

def make_rate_limited_request(url, json, headers):
    global last_request_time
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    
    if time_since_last_request < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - time_since_last_request)
    
    response = requests.post(url, json=json, headers=headers)
    last_request_time = time.time()
    return response

def read_prompt_template(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please make sure the file exists in the same directory as this script.")
        return None

OUTLINE_PROMPT_TEMPLATE = read_prompt_template('claude_outline_prompt.txt')
ARTICLE_PROMPT_TEMPLATE = read_prompt_template('claude_article_prompt.txt')

if OUTLINE_PROMPT_TEMPLATE is None or ARTICLE_PROMPT_TEMPLATE is None:
    raise FileNotFoundError("One or both prompt template files are missing. Please check that both 'claude_outline_prompt.txt' and 'claude_article_prompt.txt' exist in the same directory as this script.")

def generate_outline(keyword):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    prompt = OUTLINE_PROMPT_TEMPLATE.format(keyword=keyword)

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = make_rate_limited_request(CLAUDE_API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['content'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}")
        return None

def write_article_section(keyword, outline, current_content, section_to_write):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    prompt = ARTICLE_PROMPT_TEMPLATE.format(
        keyword=keyword,
        outline=outline,
        current_content=current_content,
        section_to_write=section_to_write
    )

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = make_rate_limited_request(CLAUDE_API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['content'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}")
        return None

def generate_meta_description(keyword, article):
    with open('claude_meta_prompt.txt', 'r') as file:
        prompt_template = file.read()

    prompt = prompt_template.format(keyword=keyword, article=article)

    headers = {
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = make_rate_limited_request(CLAUDE_API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['content'][0]['text'].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}")
        return None

print("generate_outline, write_article_section, and generate_meta_description functions are defined in claude_api.py")
