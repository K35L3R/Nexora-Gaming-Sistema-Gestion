
# ==========================================
# USUARIOS
# NEXORA GAMING & TECHNOLOGY
# ==========================================

import os
from getpass import getpass

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==========================================
# CONFIGURACIÓN DE USUARIOS
# ==========================================

# Estas contraseñas son valores de demostración.
# Puedes cambiarlas mediante variables de entorno.

CLAVE_ADMIN = os.environ.get("NEXORA_ADMIN_PASSWORD", "1234")
CLAVE_VENDEDOR = os.environ.get("NEXORA_VENDEDOR_PASSWORD", "1111")
CLAVE_INVENTARIO = os.environ.get("NEXORA_INVENTARIO_PASSWORD", "2222")


USUARIOS = {
    "admin": {
        "contrasena_hash": generate_password_hash(CLAVE_ADMIN),
        "rol": "Administrador"
    },

    "vendedor": {
        "contrasena_hash": generate_password_hash(CLAVE_VENDEDOR),
        "rol": "Vendedor"
    },

    "inventario": {
        "contrasena_hash": generate_password_hash(CLAVE_INVENTARIO),
        "rol": "Encargado de Inventario"
    }
}


# ==========================================
# VERIFICACIÓN DE CREDENCIALES
# ==========================================

def verificar_contrasena(usuario, contrasena):
    """Comprueba la contraseña sin almacenarla como texto."""

    datos_usuario = USUARIOS.get(usuario.lower().strip())

    if not datos_usuario:
        return False

    return check_password_hash(
        datos_usuario["contrasena_hash"],
        contrasena
    )


# ==========================================
# INICIO DE SESIÓN POR TERMINAL
# ==========================================

def iniciar_sesion():

    intentos = 3

    while intentos > 0:

        print("\n" + "=" * 42)
        print("       NEXORA GAMING & TECHNOLOGY")
        print("            INICIO DE SESIÓN")
        print("=" * 42)

        usuario = input(
            "Ingrese su usuario (o 'salir'): "
        ).strip().lower()

        if usuario == "salir":
            print("\nSaliendo del sistema...")
            return None, None

        contrasena = getpass(
            "Ingrese su contraseña: "
        )

        if verificar_contrasena(usuario, contrasena):

            rol = USUARIOS[usuario]["rol"]

            print("\nAcceso permitido.")
            print("Usuario:", usuario)
            print("Rol:", rol)

            return usuario, rol

        intentos -= 1

        print("\nUsuario o contraseña incorrectos.")
        print("Intentos restantes:", intentos)

    print("\nSe agotaron los intentos.")
    print("Acceso bloqueado.")

    return None, None
