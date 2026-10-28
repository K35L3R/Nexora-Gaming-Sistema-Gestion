import os
import uuid

from flask import (
    Flask,
@@ -11,6 +12,8 @@
    flash
)

from werkzeug.utils import secure_filename

import inventario
from usuario import USUARIOS
from ventas import realizar_venta, obtener_estadisticas
@@ -29,6 +32,59 @@
    app.secret_key = "clave-local-solo-para-pruebas"


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


# ==========================================
# CONTROL DE SESIÓN Y PERMISOS
# ==========================================
@@ -141,17 +197,33 @@ def ver_inventario():
                flash("No tenés permiso para agregar productos.")
                return redirect(url_for("ver_inventario"))

            codigo = request.form.get("codigo", "").strip()
            nombre = request.form.get("nombre", "").strip()
            precio = request.form.get("precio", "").strip()
            stock = request.form.get("stock", "").strip()
            codigo = request.form.get(
                "codigo", ""
            ).strip()

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

            try:
                imagen = guardar_imagen(archivo)

                inventario.agregar_producto(
                    codigo,
                    nombre,
                    precio,
                    stock
                    stock,
                    imagen
                )

                flash("Producto agregado correctamente.")
