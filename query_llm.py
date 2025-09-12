import requests
import time

# API végpont – igazítsd a saját LLM konténeredhez
URL = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"

payload = {
    "model": "ai/smollm2",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Please write 500 words about the Hungarian history"}
    ],
    "stream": False
}

def query_model():

    response = requests.post(URL, json=payload)
    response.raise_for_status()

    print(response.json()["choices"][0]["message"]["content"])

def main():
    query_model()

if __name__ == "__main__":
    main()