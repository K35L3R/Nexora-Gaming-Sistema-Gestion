```python
# ==========================================
# USUARIOS
# NEXORA GAMING & TECHNOLOGY
# ==========================================

USUARIOS = {
    "admin": {
        "contrasena": "1234",
        "rol": "Administrador"
    },

    "vendedor": {
        "contrasena": "1111",
        "rol": "Vendedor"
    },

    "inventario": {
        "contrasena": "2222",
        "rol": "Encargado de Inventario"
    }
}


def iniciar_sesion():

    intentos = 3

    while intentos > 0:

        print("\n========== INICIO DE SESION ==========")

        usuario = input("Ingrese su usuario: ")

        if usuario.lower() == "salir":
            print("\nSaliendo del sistema...")
            return None, None

        contrasena = input("Ingrese su contraseña: ")

        if usuario in USUARIOS:

            if USUARIOS[usuario]["contrasena"] == contrasena:

                rol = USUARIOS[usuario]["rol"]

                print("\nAcceso permitido.")
                print("Usuario:", usuario)
                print("Rol:", rol)

                return usuario, rol

        intentos = intentos - 1

        print("\nUsuario o contraseña incorrectos.")
        print("Intentos restantes:", intentos)

    print("\nSe agotaron los intentos.")
    print("Acceso bloqueado.")

    return None, None
```
