import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


async def get_model_completion_async(prompt: str, model: str = "openai/gpt-6-luna") -> str:
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
    )

    response = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])

    return response.choices[0].message.content


async def main():
    user_prompt = "Explain quantum computing in one sentence."
    completion = await get_model_completion_async(user_prompt)
    print(completion)

if __name__ == "__main__":
    asyncio.run(main())
