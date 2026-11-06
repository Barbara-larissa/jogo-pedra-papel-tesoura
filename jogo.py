from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "pedra-papel-tesoura-2026"

opcoes = ["pedra", "papel", "tesoura"]

vencedoras = {
    "pedra": "papel",
    "papel": "tesoura",
    "tesoura": "pedra"
}


@app.route("/", methods=["GET", "POST"])
def index():

    if "vitorias" not in session:
        session["vitorias"] = 0
        session["derrotas"] = 0
        session["empates"] = 0
        session["historico"] = []

    resultado = ""
    computador = ""
    jogador = ""

    if request.method == "POST":

        jogador = request.form.get("escolha")

        if jogador in opcoes:

            historico = session.get("historico", [])

            # Modo difícil
            if len(historico) >= 2 and random.random() < 0.65:

                mais_escolhida = max(
                    set(historico),
                    key=historico.count
                )

                computador = vencedoras[mais_escolhida]

            else:
                computador = random.choice(opcoes)

            historico.append(jogador)
            session["historico"] = historico[-10:]

            # Resultado
            if jogador == computador:
                resultado = "Empate! 🤝"
                session["empates"] += 1

            elif vencedoras[computador] == jogador:
                resultado = "Você ganhou! 🎉"
                session["vitorias"] += 1

            else:
                resultado = "O computador ganhou! 😢"
                session["derrotas"] += 1

    return render_template(
        "index.html",
        resultado=resultado,
        computador=computador,
        jogador=jogador,
        vitorias=session["vitorias"],
        derrotas=session["derrotas"],
        empates=session["empates"]
    )




@app.route("/reset", methods=["POST"])
def reset():

    session.clear()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)