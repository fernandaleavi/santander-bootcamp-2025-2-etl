### Extract

# Importar bibliotecas
import pandas as pd
import requests
import json


# Ler arquivo
df = pd.read_csv('SDW2026.csv')

# Definir coluna userID
user_ids = df['UserID'].tolist()

# print(user_ids)

# Obter os dados de cada ID usando a API
url = 'http://127.0.0.1:8000/'

# Definir função para obter user
def get_user(id):
    response = requests.get(f'{url}/users/{id}')
    return response.json() if response.status_code == 200 else None

# Atribui usuário se for não nulo
users = [user for id in user_ids if (user := get_user(id)) is not None]
# Mostra lista de usuários
# print(json.dumps(users, indent=2))


### Transform

from google import genai
from google.genai import types

client = genai.Client()

# Definir função para gerar news com AI

def generate_ai_news(user):
    completion = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="Você é um especialista de marketing que trabalha faz anos para uma agência bancária."
    ),
    contents=f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos. A mensagem deve ser feita levando em consideração o perfil de cliente baseado no seu saldo em conta de {user['account']['balance']} reais e seu limite do cartão de {user['card']['limit']} reais, porém, não fale de forma explícita o valor que o cliente tem ou insinuar que ele tem pouco ou muito dinheiro. A mensagem não deve ter mais de 100 caracteres. "
    )
    return completion.text

# adicionar nova news a cada user
for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })

### Load

# Define função para fazer update de cada user
def update_user(user):
    response = requests.put(f'{url}/users/{user['id']}', json=user)
    return True if response.status_code == 200 else False

# itera cada user para confirmar update
for user in users:
    success = update_user(user)
    print(f'User {user['name']} updated? {success}!')


