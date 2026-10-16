
from flask import Flask, render_template, request, redirect, url_for, session, flash
import inventario
from usuario import USUARIOS

app = Flask(__name__)
app.secret_key = "nexora-clave-demo-2026"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        usuario = USUARIOS.get(nombre_usuario)

        if usuario and usuario["contrasena"] == contrasena:
            session["usuario"] = nombre_usuario
            session["rol"] = usuario["rol"]
            return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    inventario.cargar_productos()
    productos = inventario.listar_productos()

    total_productos = len(productos)
    unidades = sum(p["stock"] for p in productos)
    valor_inventario = sum(
        p["precio"] * p["stock"] for p in productos
    )

    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"],
        total_productos=total_productos,
        unidades=unidades,
        valor_inventario=valor_inventario
    )


@app.route("/inventario", methods=["GET", "POST"])
def ver_inventario():
    if "usuario" not in session:
        return redirect(url_for("login"))

    inventario.cargar_productos()

    if request.method == "POST":
        codigo = request.form.get("codigo", "")
        nombre = request.form.get("nombre", "")
        precio = request.form.get("precio", "")
        stock = request.form.get("stock", "")

        try:
            inventario.agregar_producto(
                codigo, nombre, precio, stock
            )
            flash("Producto agregado correctamente.")
        except (ValueError, OSError) as error:
            flash(str(error))

        return redirect(url_for("ver_inventario"))

    productos = inventario.listar_productos()

    return render_template(
        "inventario.html",
        productos=productos,
        usuario=session["usuario"],
        rol=session["rol"]
    )


@app.route("/eliminar/<codigo>", methods=["POST"])
def eliminar(codigo):
    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("rol") not in [
        "Administrador", "Encargado de Inventario"
    ]:
        flash("No tenés permiso para eliminar productos.")
        return redirect(url_for("ver_inventario"))

    inventario.cargar_productos()

    try:
        inventario.eliminar_producto(codigo)
        flash("Producto eliminado correctamente.")
    except (ValueError, OSError) as error:
        flash(str(error))

    return redirect(url_for("ver_inventario"))


@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
