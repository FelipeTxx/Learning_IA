from flask import Flask, request
from AppRules import bloquearApps
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor rodando!"

@app.route("/atividade", methods=["POST"])
def atividade():
    dados = request.json

    if not dados: return jsonify({"erro": "Sem dados disponiveis"})

    nome_app = dados["app_em_uso"]
    tempo = dados["tempo"]
    
    if not dados: return jsonify({"erro": "Sem dados sobre tempo e/ou apps em uso"})    
    
    print(bloquearApps(nome_app, tempo))
    return jsonify({
        "acao": bloquearApps(nome_app, tempo)
    })


app.run(host="0.0.0.0", port=5000)