from openai import AsyncOpenAI

import os

#client = AsyncOpenAI(api_key=os.getenv('OpenAI'))
client = AsyncOpenAI(api_key='')


async def gpt_text(reg, model):
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": reg}
        ]
    )
    return completion.choices[0].message.content


