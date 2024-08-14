from openai import AsyncOpenAI
import httpx

from app.config import OpenAI, proxy

client = AsyncOpenAI(api_key=OpenAI,
                     http_client=httpx.AsyncClient(proxies=proxy,
                     transport=httpx.HTTPTransport(local_address='0.0.0.0')))


async def gpt_text(reg, model):
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": reg}
        ]
    )
    return completion.choices[0].message.content


