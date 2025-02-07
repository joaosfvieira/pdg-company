from flask import Flask, render_template, jsonify
import json
import unicodedata

app = Flask(__name__)

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

# Carregar os dados do JSON gerado pelo Selenium
def carregar_jogadores():
    with open("jogadores.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def index():
    jogadores = carregar_jogadores()

    # Converter "lvl" para inteiro
    for jogador in jogadores:
        jogador["lvl"] = int(jogador["lvl"])

    # Ordenar do maior para o menor nível
    sorted_players = sorted(jogadores, key=lambda x: x["lvl"], reverse=True)

    # Top 3 jogadores
    top_3 = sorted_players[:3]

    # Dicionário para armazenar os jogadores por classe
    classes = {
        "Assassina": [],
        "Guerreira": [],
        "Lutador": [],
        "Cavaleiro": [],
        "Mecanico": [],
        "Pike": [],
        "Arqueira": [],
        "Atalanta": [],
        "Mago": [],
        "Xama": [],
        "Sacerdotisa": []
    }

    # Distribuir jogadores em suas respectivas classes
    for jogador in sorted_players:
        classe = remover_acentos(jogador["classe"])
        if classe in classes:
            classes[classe].append(jogador)

    # Estatísticas gerais
    total_membros = len(jogadores)
    nivel_medio = sum(jogador["lvl"] for jogador in jogadores) / total_membros if total_membros > 0 else 0
    numero_por_classe = {classe: len(jogadores) for classe, jogadores in classes.items()}

    return render_template(
        "index.html",
        top_3=top_3,
        classes=classes,
        total_membros=total_membros,
        nivel_medio=nivel_medio,
        numero_por_classe=numero_por_classe
    )

@app.route("/api/jogadores")
def api_jogadores():
    return jsonify(carregar_jogadores())

@app.route("/teste")
def teste():
    return("Teste")

import subprocess

@app.route("/run-scraper")
def run_scraper():
    try:
        subprocess.run(["python", "webscrapper.py"], check=True)
        return jsonify({"status": "success", "message": "Script executado com sucesso"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run()
