import httpx
import os

# Load API key from environment variable
API_KEY = "os.getenv("PERPLEXITY_API_KEY")"

# Ensure API key is available
if not API_KEY:
    raise ValueError("Error: PERPLEXITY_API_KEY is not set.")

# Define API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"

# Define request payload
payload = {
    "model": "sonar-pro",  # Use "sonar-small" if you need a lighter model
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "How many stars are in the universe?"}
    ],
}

# Send request to Perplexity API
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

response = httpx.post(API_URL, json=payload, headers=headers)

# Check if request was successful
if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")