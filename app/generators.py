from openai import AsyncOpenAI
import httpx

# Импорт конфигурационных переменных
from app.config import OpenAI, proxy

# Создание клиента для взаимодействия с OpenAI
client = AsyncOpenAI(
    api_key=OpenAI,  # API ключ OpenAI
    http_client=httpx.AsyncClient(  # HTTP клиент для отправки запросов
        proxies=proxy,  # Прокси сервер для обхода ограничений
        transport=httpx.HTTPTransport(local_address='0.0.0.0')  # Транспорт для отправки запросов
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
