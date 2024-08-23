import aiofiles
import base64
import httpx
from openai import AsyncOpenAI

# Импорт конфигурационных переменных
from app.config import OpenAI, proxy
import aiohttp
# Создание клиента для взаимодействия с OpenAI
client = AsyncOpenAI(
    api_key=OpenAI,  # API ключ OpenAI
    http_client=httpx.AsyncClient(  # HTTP клиент для отправки запросов
        proxies=proxy,  # Прокси сервер для обхода ограничений
        transport=httpx.HTTPTransport(
            local_address='0.0.0.0')  # Транспорт для отправки запросов
    )
)


# Функция для получения ответа от GPT
async def gpt_text(reg, model):
    # Создание запроса для получения ответа от GPT
    completion = await client.chat.completions.create(
        model=model,  # Модель GPT
        messages=[  # Сообщения для отправки GPT
            {"role": "user", "content": reg}  # Сообщение от пользователя
        ]
    )
    # Возвращение ответа от GPT
    return {'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens}


# Функция генерации картинки
async def gpt_image(req, model):
    response = await client.images.generate(
        model='dall-e-3',
        prompt=req,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return {'response': response.data[0].url,
            'usage': 1}


# Function to encode the image
async def encode_image(image_path):
    async with aiofiles.open(image_path, "rb") as image_file:
        return base64.b64encode(await image_file.read()).decode('utf-8')


async def gpt_vision(req, model, file):

    # Getting the base64 string
    base64_image = await encode_image(file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OpenAI}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": req
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    if req is not None:
        payload['messages'][0]['content'].append({'type': 'text', 'text': req})

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/chat/completions",
                                headers=headers, json=payload) as response:
            completion = await response .json()
            print(completion)
    return {'response': completion['choices'][0]['message']['content'],
            'usage': completion['usage']['total_tokens']}
