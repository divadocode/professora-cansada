from flask import Flask, render_template, request, redirect, url_for
import os
import hashlib
from automation.dryrun import enviar_nota_dryrun

app = Flask(__name__)

# Função para gerar hash da senha
def gerar_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

# Página inicial
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Página de login/cadastro
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_digitado = request.form["login"]
        senha_digitada = request.form["senha"]

        # Se já existir login.txt -> validar
        if os.path.exists("login.txt"):
            with open("login.txt", "r") as arquivo:
                login_salvo, hash_senha_salva = [x.strip() for x in arquivo.read().split(",")]

            if login_digitado == login_salvo and gerar_hash(senha_digitada) == hash_senha_salva:
                return redirect(url_for("notas"))
            else:
                return "Acesso negado! <a href='/login'>Tentar de novo</a>"

        # Se não existir -> cadastrar esse login e senha
        else:
            with open("login.txt", "w") as arquivo:
                arquivo.write(login_digitado + "," + gerar_hash(senha_digitada))
            return redirect(url_for("notas"))

    return render_template("login.html")

# Página para lançar notas
@app.route("/notas", methods=["GET", "POST"])
def notas():
    if request.method == "POST":
        turma = request.form["turma"]
        nome = request.form["nome"]
        nota = request.form["nota"]

        # DRYRUN CHAMADO AQUI!!!
        enviar_nota_dryrun(turma, nome, nota)

        return redirect(url_for("loop"))

    return render_template("notas.html")

# Página de loop (pergunta se quer lançar outra nota)
@app.route("/loop", methods=["GET", "POST"])
def loop():
    if request.method == "POST":
        escolha = request.form["escolha"]
        if escolha == "sim":
            return redirect(url_for("notas"))
        else:
            return redirect(url_for("grata"))
    return render_template("loop.html")

# Página final de agradecimento
@app.route("/grata")
def grata():
    return render_template("grata.html")

if __name__ == "__main__":
    app.run(debug=True)

