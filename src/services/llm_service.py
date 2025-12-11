import json
from src.settings import settings
import logging
import requests


'''Module with business logic'''


class LLM:
    def __init__(self, model='gpt-oss-120b'):
        self.model = model
        self.URL = "https://api.scaleway.ai/4504e593-8265-4652-b056-edcd96fed2d1/v1/chat/completions"
        self.HEADERS = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.LLM_TOKEN}"
        }

    def invoke(self, message):
        PAYLOAD = {
            "model": self.model,
            "messages": [
                    { "role": "system", "content": "You are a helpful assistant"},
                    { "role": "user", "content": message},
                ],
                "max_tokens": 1024,
                "temperature": 0.8,
                "top_p": 0.9,
                "presence_penalty": 0,
                "stream": True,
            }
        response = requests.post(self.URL, headers=self.HEADERS, data=json.dumps(PAYLOAD), stream=True)

        if response.status_code != 200:
            logging.error("LLM не доступна")
            logging.error(response.text)
            return 'Сервер с LLM не доступен'

        text = ''
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line == "data: [DONE]":
                    break
                if decoded_line.startswith("data: "):
                    try:
                        data = json.loads(decoded_line[len("data: "):])
                        if data.get("choices") and data["choices"][0]["delta"].get("content"):
                            text += data["choices"][0]["delta"]["content"]
                    except json.JSONDecodeError:
                        continue
        logging.info(text)
        return text


def get_llm_answer(llm: LLM, query: str):
    PROMPT = f'''У меня есть база данных с двумя таблицами. В первой таблице videos содержаться данные о видео: 
    index - идентификатор видео;
    creator_id - идентификатор креатора;
    video_created_at - дата и время публикации видео;
    views_count - финальное количество просмотров;
    likes_count - финальное количество лайков;
    comments_count - финальное количество комментариев; 
    reports_count - финальное количество жалоб;
    created_at - дата и время загрузки видео
    updated_at - дата и время обновления видео.
    Во второй таблице snapshots содержится информация о видео на каждом часу:
    id - идентификатор снапшота;
    video_id - foreign key на колонку index таблицы videos;
    views_count - количество просмотров на момент замера;
    likes_count - количество лайков на момент замера;
    comments_count - количество комментариев на момент замера;
    reports_count - количество жалоб на момент замера;
    delta_views_count - изменение количества просмотров с предыдущего замера;
    delta_likes_count - изменение количества лайков с предыдущего замера;
    delta_comments_count - изменение количества комментариев с предыдущего замера;
    delta_reports_count - изменение количества жалоб с предыдущего замера;
    created_at - время замера (раз в час);
    updated_at - время изменения.
    
    Напиши SQL запрос для того, чтоб получить следующее:
    {query}
    
    В ответе выведи только SQL запрос.'''

    sql_query = llm.invoke(PROMPT)
    return sql_query
