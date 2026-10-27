import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

def get_model_completion(prompt: str, model: str = "anthropic/claude-3.5-sonnet") -> str:
    """
    Sends a text prompt to OpenRouter and returns the model's text response.
    """
    # Initialize the OpenAI client configured for OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        default_headers={
            "HTTP-Referer": "https://your-site.com",  # Optional: For OpenRouter rankings
            "X-Title": "Your App Name",               # Optional: Shows up in your dashboard
        }
    )

    # Create the chat completion request
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Return the content of the response message
    return response.choices[0].message.content

# --- Example Usage ---
if __name__ == "__main__":
    user_prompt = "Explain quantum computing in one sentence."
    completion = get_model_completion(user_prompt)
    print(completion)