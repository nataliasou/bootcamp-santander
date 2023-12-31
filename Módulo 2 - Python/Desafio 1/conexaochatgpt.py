# -*- coding: utf-8 -*-
"""conexaoChatgpt.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/118BWmNEocBd_-c0iEiCzxkGGiFtjNX_d

# **Aplicação de ETL com Python**
## **Etapa: Extract**

---


Nas linhas abaixo serão extraídos os IDs de usuário no arquivo CSV fornecido. </br> Cada ID terá um GET para obter dados do usuário especificado pelo ID.
"""

import pandas as pd

df = pd.read_csv("dados.csv")
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

url_api = 'https://sdw-2023-prd.up.railway.app' # url para requisição

def get_user(id):
  response = requests.get(f'{url_api}/users/{id}')
  return response.json() if response.status_code == 200 else None

user = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(user, indent=2))

"""## Etapa: Transform
Usando a API do OPenAI para gerar uma mensagem de marketing.
"""

!pip install openai

openai_api_key = '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'

import openai

openai.api_key = openai_api_key


def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "Você é um especialista de Marketing."
        },
        {
          "role": "user",
          "content": f"Mensagem personalizada para o usuário {user['name']} (máximo de 100 caracteres)"
        }
      ]
  )
  return completion.choice[0].message.content.strip("\"")


for u in user:
  news = generate_ai_news(u)
  print(news)
  u['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

"""## Etapa: Load
Atualização da lista de news de cada usuário
"""

def update_user(user):
  response = requests.put(f"{url_api}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for u in user:
  success = update_user(u)
  print(f"User {u['name']} updated? {success}!")