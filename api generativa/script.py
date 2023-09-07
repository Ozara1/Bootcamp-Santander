import pandas as pd
import requests
import json
import openai


# Repósitorio da API: https://github.com/digitalinnovationone/santander-dev-2023-api
sdw_2023_api_url = "https://sdw-2023-prd.up.railway.app"
openai_api_key = "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"

df = pd.read_csv("SDW2023.csv")
user_ids = df["UserID"].tolist()
print(user_ids)


def get_user(id):
    response = requests.get(f"{sdw_2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

openai.api_key = openai_api_key


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em marketing bancário.",
            },
            {
                "role": "users",
                "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)",
            },
        ],
    )
    return completion.choices[0].message.content('"')


for user in users:
    news = generate_ai_news(user)
    print(news)
    user["news"].append(
        {
            "icon": "http//digitalinnovationone.github.io/santander-dev-week-2023-api/icon/credit.svg",
            "description": news,
        }
    )

def update_user(user):
    response = requests.put(f"{sdw_2023_api_url}/users/{user['id']}",json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"User {user['name']} update? {success}!")