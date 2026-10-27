import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_model_completion(prompt: str, model: str = "openai/gpt-6-luna") -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
    )

    response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])

    return response.choices[0].message.content


async def get_model_completion_async(prompt: str, model: str = "openai/gpt-6-luna") -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
    )

    response = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])

    return response.choices[0].message.content


if __name__ == "__main__":
    user_prompt = "Explain quantum computing in one sentence."
    completion = get_model_completion(user_prompt)
    print(completion)
