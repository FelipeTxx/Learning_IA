import requests
import time

inicio = time.monotonic()

while True:
    agora = time.monotonic()
    agora -= inicio
    dados = {
        "app_em_uso": "Instagram",
        "tempo": int(agora)
    }

    requests.post("http://localhost:5000/atividade", json=dados)

    time.sleep(3)