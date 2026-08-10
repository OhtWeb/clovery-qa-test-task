import requests


class CloveryApiClient:
    def __init__(self, base_url="https://cerber.ms.raida.work"):
        #Понятия не имею, какой url в действительности, но это легко поправимо
        self.base_url = base_url.rstrip('/')

    def post_create_right(self, project_id: str, text: str, code: str):
        url = f"{self.base_url}/api/rights/{project_id}"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "description": {
                "text": text
            },
            "code": code
        }

        # Отправляем POST запрос с JSON-телом
        response = requests.post(url, json=payload, headers=headers)

        # Пробуем распарсить JSON, если не выходит — берем сырой текст
        try:
            data = response.json()
        except ValueError:
            data = response.text

        return response.status_code, data

    def get_right_new(self, project_id):
        url = f"{self.base_url}/api/rights/{project_id}"

        headers = {
            "Content-Type": "application/json"
        }

        # Отправляем GET запрос с JSON-телом
        response = requests.get(url, headers=headers)

        # Пробуем распарсить JSON, если не выходит — берем сырой текст
        try:
            data = response.json()
        except ValueError:
            data = response.text

        return response.status_code, data