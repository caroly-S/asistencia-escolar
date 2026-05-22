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
    resumen = csv_helper.calcular_resumen(hoy)
    total   = len(csv_helper.obtener_estudiantes())

    return render_template("inicio.html", total=total, resumen=resumen, hoy=hoy)


@app.route("/estudiantes")

def estudiantes():

    if "usuario" not in session:
        return redirect(url_for("login"))
    buscar = request.args.get("buscar", "")
    grado  = request.args.get("grado",  "")
    lista  = csv_helper.filtrar_estudiantes(buscar, grado)


    return render_template("estudiantes.html",
        estudiantes=lista, buscar=buscar,
        grado=grado, total=len(lista))


@app.route("/estudiantes/nuevo", methods=["POST"])

def nuevo_estudiante():

    if "usuario" not in session:
        return redirect(url_for("login"))
    csv_helper.agregar_estudiante(
        request.form["apellidos"],
        request.form["nombres"],
        request.form["dni"],
        request.form["grado"],
        request.form["seccion"],
        request.form["turno"]
    )

    return redirect(url_for("estudiantes"))


@app.route("/estudiantes/editar/<id>", methods=["GET", "POST"])

def editar_estudiante(id):

    if "usuario" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        csv_helper.actualizar_estudiante(
            id,
            request.form["apellidos"],
            request.form["nombres"],
            request.form["dni"],
            request.form["grado"],
            request.form["seccion"],
            request.form["turno"]
        )
        return redirect(url_for("estudiantes"))
    
    e = csv_helper.buscar_estudiante_por_id(id)

    if e is None:
        return redirect(url_for("estudiantes"))
    
    return render_template("editar.html", e=e)


@app.route("/estudiantes/eliminar/<id>")

def eliminar_estudiante(id):

    if "usuario" not in session:
        return redirect(url_for("login"))
    
    csv_helper.eliminar_estudiante(id)

    return redirect(url_for("estudiantes"))


if __name__ == "__main__":
    csv_helper.leer_csv("data/estudiantes.csv", csv_helper.CABECERA_ESTUDIANTES)
    csv_helper.leer_csv("data/asistencia.csv",  csv_helper.CABECERA_ASISTENCIA)
    app.run(host="0.0.0.0", port=8080, debug=True)