import requests

API_BASE_URL = "http://localhost:8000/api/v1"


# --- ALUNOS ---
def get_alunos():
  try:
    response = requests.get(f"{API_BASE_URL}/alunos/")
    if response.status_code == 200:
      return response.json()
    return []
  except Exception as e:
    print(f"Erro ao conectar com a API: {e}")
    return []

def criar_aluno(dados_aluno):
  try:
    response = requests.post(f"{API_BASE_URL}/alunos/", json=dados_aluno)
    return response
  except Exception as e:
    return None


# --- EXERCÍCIOS ---
def get_exercicios():
  try:
    res = requests.get(f"{API_BASE_URL}/treinos/exercicios/")
    return res.json() if res.status_code == 200 else []
  except:
    return []

def criar_exercicio(payload):
  try:
    return requests.post(f"{API_BASE_URL}/treinos/exercicios/", json=payload)
  except:
    return None


# --- FICHAS ---
def get_fichas_aluno(aluno_id: int):
  try:
    res = requests.get(f"{API_BASE_URL}/treinos/fichas/aluno/{aluno_id}")
    return res.json() if res.status_code == 200 else []
  except:
    return []

def criar_ficha_treino(payload):
  try:
    return requests.post(f"{API_BASE_URL}/treinos/fichas/", json=payload)
  except:
    return None


# --- AVALIAÇÕES ---
def get_avaliacoes_aluno(aluno_id: int):
  try:
    response = requests.get(f"{API_BASE_URL}/avaliacoes/aluno/{aluno_id}")
    return response.json() if response.status_code == 200 else []
  except:
    return []


def criar_avaliacao(dados_avaliacao):
  try:
    return requests.post(f"{API_BASE_URL}/avaliacoes/", json=dados_avaliacao)
  except:
    return None
  

def get_mensalidades_aluno(aluno_id: int):
  try:
    response = requests.get(f"{API_BASE_URL}/mensalidades/aluno/{aluno_id}")
    return response.json() if response.status_code == 200 else []
  except:
    return []


def criar_mensalidade(dados):
  try:
    return requests.post(f"{API_BASE_URL}/mensalidades/", json=dados)
  except:
    return None


def atualizar_mensalidade(mensalidade_id: int, dados):
  try:
    return requests.patch(
        f"{API_BASE_URL}/mensalidades/{mensalidade_id}", json=dados
    )
  except:
    return None