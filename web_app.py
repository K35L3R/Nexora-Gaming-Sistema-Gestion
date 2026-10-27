
import os
import uuid
from datetime import timedelta

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from werkzeug.utils import secure_filename

import inventario
from usuario import USUARIOS
from ventas import realizar_venta, obtener_estadisticas


# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================

app = Flask(__name__)

# En producción, SECRET_KEY debe configurarse como
# variable de entorno en el servicio de alojamiento.
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    if os.environ.get("RENDER"):
        raise RuntimeError(
            "Debes configurar la variable SECRET_KEY en Render."
        )

    # Solo para desarrollo local.
    app.secret_key = "clave-local-solo-para-pruebas"

EN_PRODUCCION = bool(os.environ.get("RENDER"))

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=EN_PRODUCCION,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8)
)


# ==========================================
# CONFIGURACIÓN DE IMÁGENES
# ==========================================

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EXTENSIONES_IMAGEN = {
    "png",
    "jpg",
    "jpeg",
    "webp",
    "gif"
}


def guardar_imagen(archivo):
    """Guarda una imagen y devuelve su ruta pública."""

    if not archivo or not archivo.filename:
        return ""

    nombre_seguro = secure_filename(archivo.filename)

    if not nombre_seguro or "." not in nombre_seguro:
        raise ValueError("El archivo de imagen no es válido.")

    extension = nombre_seguro.rsplit(".", 1)[1].lower()

    if extension not in EXTENSIONES_IMAGEN:
        raise ValueError(
            "Formato no permitido. Usa PNG, JPG, JPEG, WEBP o GIF."
        )

    nombre_archivo = f"{uuid.uuid4().hex}.{extension}"

    ruta_archivo = os.path.join(
        UPLOAD_FOLDER,
        nombre_archivo
    )

    archivo.save(ruta_archivo)

    return url_for(
        "static",
        filename=f"uploads/{nombre_archivo}"
    )


def eliminar_archivo_subido(ruta_publica):
    """Elimina una imagen subida si el registro del producto falla."""

    if not ruta_publica:
        return

    nombre_archivo = os.path.basename(ruta_publica)

    if not nombre_archivo:
        return

    ruta_archivo = os.path.join(
        UPLOAD_FOLDER,
        nombre_archivo
    )

    try:
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
    except OSError:
        app.logger.exception(
            "No se pudo eliminar la imagen: %s",
            nombre_archivo
        )


# ==========================================
# CONTROL DE SESIÓN Y PERMISOS
# ==========================================

def requiere_sesion():
    return bool(session.get("usuario"))


def requiere_rol(*roles):
    return session.get("rol") in roles


def usuario_actual():
    return session.get("usuario")


def rol_actual():
    return session.get("rol")


def cargar_productos_seguro():
    """Carga los productos antes de consultar el inventario."""

    inventario.cargar_productos()
    return inventario.listar_productos()


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

        if (
            usuario
            and usuario.get("contrasena") == contrasena
            and usuario.get("rol")
        ):
            session.clear()
            session.permanent = True
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
        productos = cargar_productos_seguro()

        total_productos = len(productos)

        unidades = sum(
            int(producto["stock"])
            for producto in productos
        )

        valor_inventario = sum(
            float(producto["precio"]) * int(producto["stock"])
            for producto in productos
        )

        estadisticas = obtener_estadisticas()

    except (OSError, ValueError, KeyError, TypeError):
        app.logger.exception("Error al cargar el dashboard.")

        flash("No se pudieron cargar los datos del panel.")

        total_productos = 0
        unidades = 0
        valor_inventario = 0
        estadisticas = {}

    return render_template(
        "dashboard.html",
        usuario=usuario_actual(),
        rol=rol_actual(),
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

            codigo = request.form.get(
                "codigo", ""
            ).strip().upper()

            nombre = request.form.get(
                "nombre", ""
            ).strip()

            precio = request.form.get(
                "precio", ""
            ).strip()

            stock = request.form.get(
                "stock", ""
            ).strip()

            archivo = request.files.get("imagen")
            imagen = ""

            try:
                if not codigo or not nombre:
                    raise ValueError(
                        "El código y el nombre son obligatorios."
                    )

                if not precio or not stock:
                    raise ValueError(
                        "El precio y el stock son obligatorios."
                    )

                imagen = guardar_imagen(archivo)

                inventario.agregar_producto(
                    codigo,
                    nombre,
                    precio,
                    stock,
                    imagen
                )

                flash("Producto agregado correctamente.")

            except (ValueError, OSError) as error:
                # Evita dejar imágenes huérfanas si el producto
                # no pudo guardarse.
                eliminar_archivo_subido(imagen)
                flash(str(error))

            except Exception:
                eliminar_archivo_subido(imagen)

                app.logger.exception(
                    "Error inesperado al agregar un producto."
                )

                flash(
                    "No se pudo agregar el producto. "
                    "Revisa los datos e inténtalo de nuevo."
                )

            return redirect(url_for("ver_inventario"))

        productos = inventario.listar_productos()

        return render_template(
            "inventario.html",
            productos=productos,
            usuario=usuario_actual(),
            rol=rol_actual()
        )

    except (OSError, ValueError, KeyError, TypeError):
        app.logger.exception("Error al cargar el inventario.")

        flash("No se pudo cargar el inventario.")

        return render_template(
            "inventario.html",
            productos=[],
            usuario=usuario_actual(),
            rol=rol_actual()
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

    except (ValueError, OSError, KeyError, TypeError):
        app.logger.exception(
            "Error al eliminar el producto %s.",
            codigo
        )

        flash(
            "No se pudo eliminar el producto. "
            "Comprueba que exista e inténtalo de nuevo."
        )

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

            cantidad_texto = request.form.get(
                "cantidad", ""
            ).strip()

            try:
                cantidad = int(cantidad_texto)

                if cantidad <= 0:
                    raise ValueError

            except (ValueError, TypeError):
                flash("Ingresa una cantidad entera mayor que cero.")
                return redirect(url_for("ver_ventas"))

            try:
                venta = realizar_venta(
                    codigo=codigo,
                    cantidad=cantidad,
                    usuario=usuario_actual() or "Sistema"
                )

                if venta:
                    flash("Venta registrada correctamente.")
                else:
                    flash(
                        "No se pudo registrar la venta. "
                        "Verifica el producto y el stock."
                    )

            except (ValueError, OSError, KeyError, TypeError):
                app.logger.exception(
                    "Error al registrar una venta."
                )

                flash(
                    "Ocurrió un error al registrar la venta."
                )

            return redirect(url_for("ver_ventas"))

        productos = inventario.listar_productos()

        return render_template(
            "ventas.html",
            productos=productos,
            usuario=usuario_actual(),
            rol=rol_actual(),
            mensaje=None
        )

    except (OSError, ValueError, KeyError, TypeError):
        app.logger.exception("Error al cargar la página de ventas.")

        flash("No se pudieron cargar los datos de ventas.")

        return render_template(
            "ventas.html",
            productos=[],
            usuario=usuario_actual(),
            rol=rol_actual(),
            mensaje=None
        )


# ==========================================
# ESTADÍSTICAS
# ==========================================

@app.route("/estadisticas")
def ver_estadisticas():

    if not requiere_sesion():
        return redirect(url_for("login"))

    try:
        estadisticas = obtener_estadisticas()

    except (OSError, ValueError, KeyError, TypeError):
        app.logger.exception("Error al obtener estadísticas.")

        flash("No se pudieron cargar las estadísticas.")
        estadisticas = {}

    return render_template(
        "estadisticas.html",
        estadisticas=estadisticas,
        usuario=usuario_actual(),
        rol=rol_actual()
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


@app.errorhandler(413)
def archivo_demasiado_grande(error):

    flash(
        "El archivo supera el límite permitido de 5 MB."
    )

    if requiere_sesion():
        return redirect(url_for("ver_inventario"))

    return redirect(url_for("login"))


# ==========================================
# ENCABEZADOS DE SEGURIDAD
# ==========================================

@app.after_request
def agregar_encabezados_seguridad(respuesta):

    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "SAMEORIGIN"
    respuesta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return respuesta


# ==========================================
# EJECUCIÓN LOCAL
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000))
    )
