from flask import Flask, render_template, request, redirect, url_for, session
import csv_helper
from datetime import date

app = Flask(__name__)
app.secret_key = "clave2025"

USUARIOS = [
    {"usuario": "caroly",    "password": "123"},
    {"usuario": "christian", "password": "dtyinop1"},
]

def validar_login(usuario, password):
    for u in USUARIOS:
        if u["usuario"] == usuario and u["password"] == password:
            return True
    return False


@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario  = request.form["usuario"]
        password = request.form["password"]
        if validar_login(usuario, password):
            session["usuario"] = usuario
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    hoy     = date.today().isoformat()
    #resumen = csv_helper.calcular_resumen(hoy)
    #total   = len(csv_helper.obtener_estudiantes())
    # TODO: Replace after create helper methods
    return render_template("inicio.html", total=0, resumen=0, hoy=hoy)


if __name__ == "__main__":
    csv_helper.leer_csv("data/estudiantes.csv", csv_helper.CABECERA_ESTUDIANTES)
    csv_helper.leer_csv("data/asistencia.csv",  csv_helper.CABECERA_ASISTENCIA)
    app.run(host="0.0.0.0", port=8080, debug=True)