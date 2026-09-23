"""
Portal Académico - Aplicación Flask
Examen Práctico - TEM-742 Tecnologías Emergentes II
"""

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash

app = Flask(__name__)
app.secret_key = "clave_secreta_portal_academico_2026"  # Necesaria para usar session y flash

# --- Datos simulados ---

usuarios = {
    "juan": "1234",
    "maria": "abcd",
    "pedro": "2026"
}

cursos = [
    {"nombre": "Programación Web", "docente": "Luis Pérez", "cupos": 15},
    {"nombre": "Bases de Datos", "docente": "Ana López", "cupos": 8},
    {"nombre": "Inteligencia Artificial", "docente": "Carlos Rojas", "cupos": 0}
]


# --- Rutas ---

@app.route("/")
def index():
    usuario_preferido = request.cookies.get("usuario_preferido")
    return render_template("index.html", usuario_preferido=usuario_preferido)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        if usuario in usuarios and usuarios[usuario] == password:
            # 1. Guardar el nombre del usuario en la sesión
            session["usuario"] = usuario
            flash(f"Bienvenido, {usuario}.")

            # 2. Redireccionar a /cursos, guardando la cookie de preferencia
            resp = make_response(redirect(url_for("cursos_view")))
            resp.set_cookie("usuario_preferido", usuario, max_age=60 * 60 * 24 * 30)
            return resp
        else:
            flash("Usuario o contraseña incorrectos.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/cursos")
def cursos_view():
    return render_template("cursos.html", cursos=cursos)


@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        flash("Debe iniciar sesión para acceder a su perfil.")
        return redirect(url_for("login"))
    return render_template("perfil.html", usuario=session["usuario"])


@app.route("/logout")
def logout():
    session.clear()
    flash("La sesión fue cerrada correctamente.")
    return redirect(url_for("index"))


@app.route("/eliminar_cookie")
def eliminar_cookie():
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("usuario_preferido")
    flash("Se eliminó la cookie de usuario preferido.")
    return resp


if __name__ == "__main__":
    app.run(debug=True)
