
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import inventario
from usuario import USUARIOS
from ventas import realizar_venta, obtener_estadisticas


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    if os.environ.get("RENDER"):
        raise RuntimeError(
            "Debes configurar la variable SECRET_KEY en Render."
        )

    app.secret_key = "clave-local-solo-para-pruebas"


# ==========================================
# CONTROL DE SESIÓN Y PERMISOS
# ==========================================

def requiere_sesion():
    return "usuario" in session


def requiere_rol(*roles):
    return session.get("rol") in roles


# ==========================================
# INICIO DE SESIÓN
# ==========================================

@app.route("/", methods=["GET", "POST"])
def login():

    if requiere_sesion():
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        nombre_usuario = request.form.get(
            "usuario", ""
        ).strip()

        contrasena = request.form.get(
            "contrasena", ""
        )

        usuario = USUARIOS.get(nombre_usuario)

        if usuario and usuario.get("contrasena") == contrasena:
            session.clear()
            session["usuario"] = nombre_usuario
            session["rol"] = usuario["rol"]

            return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.")

    return render_template("login.html")


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if not requiere_sesion():
        return redirect(url_for("login"))

    try:
        inventario.cargar_productos()
        productos = inventario.listar_productos()

        total_productos = len(productos)

        unidades = sum(
            int(producto["stock"]) for producto in productos
        )

        valor_inventario = sum(
            float(producto["precio"]) * int(producto["stock"])
            for producto in productos
        )

    except (OSError, ValueError, KeyError, TypeError) as error:
        flash("No se pudo cargar el inventario: " + str(error))
        total_productos = 0
        unidades = 0
        valor_inventario = 0

    estadisticas = obtener_estadisticas()

    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"],
        total_productos=total_productos,
        unidades=unidades,
        valor_inventario=valor_inventario,
        estadisticas=estadisticas
    )


# ==========================================
# INVENTARIO
# ==========================================

@app.route("/inventario", methods=["GET", "POST"])
def ver_inventario():

    if not requiere_sesion():
        return redirect(url_for("login"))

    try:
        inventario.cargar_productos()

        if request.method == "POST":

            if not requiere_rol(
                "Administrador",
                "Encargado de Inventario"
            ):
                flash("No tenés permiso para agregar productos.")
                return redirect(url_for("ver_inventario"))

            codigo = request.form.get("codigo", "").strip()
            nombre = request.form.get("nombre", "").strip()
            precio = request.form.get("precio", "").strip()
            stock = request.form.get("stock", "").strip()

            try:
                inventario.agregar_producto(
                    codigo,
                    nombre,
                    precio,
                    stock
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

    except (OSError, ValueError, KeyError, TypeError) as error:
        flash("Error al cargar el inventario: " + str(error))

        return render_template(
            "inventario.html",
            productos=[],
            usuario=session["usuario"],
            rol=session["rol"]
        )


# ==========================================
# ELIMINAR PRODUCTOS
# ==========================================

@app.route("/eliminar/<codigo>", methods=["POST"])
def eliminar(codigo):

    if not requiere_sesion():
        return redirect(url_for("login"))

    if not requiere_rol(
        "Administrador",
        "Encargado de Inventario"
    ):
        flash("No tenés permiso para eliminar productos.")
        return redirect(url_for("ver_inventario"))

    try:
        inventario.cargar_productos()
        inventario.eliminar_producto(codigo)

        flash("Producto eliminado correctamente.")

    except (ValueError, OSError, KeyError) as error:
        flash("No se pudo eliminar el producto: " + str(error))

    return redirect(url_for("ver_inventario"))


# ==========================================
# REGISTRO DE VENTAS
# ==========================================

@app.route("/ventas", methods=["GET", "POST"])
def ver_ventas():

    if not requiere_sesion():
        return redirect(url_for("login"))

    try:
        inventario.cargar_productos()

        if request.method == "POST":

            codigo = request.form.get(
                "codigo", ""
            ).strip().upper()

            try:
                cantidad = int(
                    request.form.get("cantidad", "")
                )
            except (ValueError, TypeError):
                flash("Ingresa una cantidad válida.")
                return redirect(url_for("ver_ventas"))

            venta = realizar_venta(
                codigo=codigo,
                cantidad=cantidad,
                usuario=session.get("usuario", "Sistema")
            )

            if venta:
                flash("Venta registrada correctamente.")
            else:
                flash(
                    "No se pudo registrar la venta. "
                    "Verifica el producto y el stock."
                )

            return redirect(url_for("ver_ventas"))

        productos = inventario.listar_productos()

        return render_template(
            "ventas.html",
            productos=productos,
            usuario=session.get("usuario"),
            rol=session.get("rol"),
            mensaje=None
        )

    except (OSError, ValueError, KeyError, TypeError) as error:
        flash("Error al procesar la venta: " + str(error))

        return render_template(
            "ventas.html",
            productos=[],
            usuario=session.get("usuario"),
            rol=session.get("rol"),
            mensaje=None
        )


# ==========================================
# ESTADÍSTICAS
# ==========================================

@app.route("/estadisticas")
def ver_estadisticas():

    if not requiere_sesion():
        return redirect(url_for("login"))

    estadisticas = obtener_estadisticas()

    return render_template(
        "estadisticas.html",
        estadisticas=estadisticas,
        usuario=session.get("usuario"),
        rol=session.get("rol")
    )


# ==========================================
# CERRAR SESIÓN
# ==========================================

@app.route("/cerrar-sesion")
def cerrar_sesion():

    session.clear()

    return redirect(url_for("login"))


# ==========================================
# MANEJO DE ERRORES
# ==========================================

@app.errorhandler(404)
def pagina_no_encontrada(error):

    if requiere_sesion():
        return "La página solicitada no existe.", 404

    return redirect(url_for("login"))


# ==========================================
# EJECUCIÓN LOCAL
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000))
    )
