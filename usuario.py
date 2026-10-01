# ==========================================
# USUARIOS
# NEXORA GAMING & TECHNOLOGY
# ==========================================

USUARIO_CORRECTO = "admin"
CONTRASENA_CORRECTA = "1234"


def iniciar_sesion():
    intentos = 3

    while intentos > 0:
        print("\n========== INICIO DE SESION ==========")

        usuario = input("Ingrese su usuario: ")
        contrasena = input("Ingrese su contraseña: ")

        if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
            print("\nAcceso permitido.")
            return True

        intentos = intentos - 1
        print("Usuario o contraseña incorrectos.")
        print("Intentos restantes:", intentos)

    print("\nSe agotaron los intentos.")
    return False
