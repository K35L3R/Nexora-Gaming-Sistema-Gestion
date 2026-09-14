# ==========================================
# NEXORA GAMING & TECHNOLOGY
# Sistema de Gestión de Inventario y Ventas
# ==========================================

# Datos de acceso
USUARIO_CORRECTO = "admin"
CONTRASENA_CORRECTA = "1234"


# ==========================================
# FUNCIÓN DE LOGIN
# ==========================================

def iniciar_sesion():
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        print("\n========================================")
        print("       NEXORA GAMING & TECHNOLOGY")
        print("          SISTEMA DE GESTIÓN")
        print("========================================")

        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
            print("\n✓ Acceso concedido.")
            return True
        else:
            intentos += 1
            restantes = max_intentos - intentos

            print("\n✗ Usuario o contraseña incorrectos.")

            if restantes > 0:
                print(f"Intentos restantes: {restantes}")
            else:
                print("Se alcanzó el número máximo de intentos.")

    return False


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def mostrar_menu():
    while True:
        print("\n========================================")
        print("             MENÚ PRINCIPAL")
        print("========================================")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("4. Eliminar producto")
        print("5. Realizar venta")
        print("6. Estadísticas")
        print("7. Salir")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nFunción de agregar producto: próximamente.")
        elif opcion == "2":
            print("\nFunción de listar productos: próximamente.")
        elif opcion == "3":
            print("\nFunción de buscar producto: próximamente.")
        elif opcion == "4":
            print("\nFunción de eliminar producto: próximamente.")
        elif opcion == "5":
            print("\nFunción de realizar venta: próximamente.")
        elif opcion == "6":
            print("\nFunción de estadísticas: próximamente.")
        elif opcion == "7":
            print("\nGracias por utilizar NEXORA Gaming.")
            break
        else:
            print("\n✗ Opción inválida. Seleccione una opción del 1 al 7.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if iniciar_sesion():
    mostrar_menu()
else:
    print("\nAcceso bloqueado. El programa finalizará.")
