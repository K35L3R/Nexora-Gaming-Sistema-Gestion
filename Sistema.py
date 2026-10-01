# ==========================================
# NEXORA GAMING & TECHNOLOGY
# Sistema de Gestión de Inventario y Ventas
# ==========================================


# ==========================================
# IMPORTAR FUNCIONES
# ==========================================

from usuario import iniciar_sesion
from ventas import realizar_venta, mostrar_estadisticas


# ==========================================
# LISTAS DEL SISTEMA
# ==========================================

productos = []


# ==========================================
# FUNCIÓN PARA AGREGAR PRODUCTOS
# ==========================================

def agregar_producto():

    print("\n========================================")
    print("           AGREGAR PRODUCTO")
    print("========================================")

    id_producto = input("ID del producto: ")

    # Comprobar que el ID no esté repetido
    for producto in productos:

        if producto[0] == id_producto:
            print("\nYa existe un producto con ese ID.")
            return

    nombre = input("Nombre del producto: ")
    categoria = input("Categoría: ")

    # Validación del precio
    while True:

        try:

            precio = float(input("Precio: "))

            if precio <= 0:
                print("El precio debe ser mayor que 0.")
            else:
                break

        except ValueError:
            print("Error: ingrese un precio válido.")

    # Validación de cantidad
    while True:

        try:

            cantidad = int(input("Cantidad disponible: "))

            if cantidad < 0:
                print("La cantidad no puede ser negativa.")
            else:
                break

        except ValueError:
            print("Error: ingrese una cantidad válida.")

    producto = [
        id_producto,
        nombre,
        categoria,
        precio,
        cantidad
    ]

    productos.append(producto)

    print("\nProducto agregado correctamente.")


# ==========================================
# FUNCIÓN PARA LISTAR PRODUCTOS
# ==========================================

def listar_productos():

    print("\n========================================")
    print("              INVENTARIO")
    print("========================================")

    if len(productos) == 0:

        print("No hay productos registrados.")
        return

    print(
        f"{'ID':<8}"
        f"{'PRODUCTO':<25}"
        f"{'CATEGORÍA':<20}"
        f"{'PRECIO':<12}"
        f"{'STOCK':<8}"
    )

    print("-" * 73)

    for producto in productos:

        print(
            f"{producto[0]:<8}"
            f"{producto[1]:<25}"
            f"{producto[2]:<20}"
            f"Q{producto[3]:<11.2f}"
            f"{producto[4]:<8}"
        )


# ==========================================
# FUNCIÓN PARA BUSCAR PRODUCTOS
# ==========================================

def buscar_producto():

    print("\n========================================")
    print("             BUSCAR PRODUCTO")
    print("========================================")

    id_buscar = input("Ingrese el ID del producto: ")

    encontrado = False

    for producto in productos:

        if producto[0] == id_buscar:

            print("\nProducto encontrado.")
            print(f"ID: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Categoría: {producto[2]}")
            print(f"Precio: Q{producto[3]:.2f}")
            print(f"Stock: {producto[4]}")

            encontrado = True
            break

    if encontrado == False:

        print("\nNo se encontró un producto con ese ID.")


# ==========================================
# FUNCIÓN PARA ELIMINAR PRODUCTOS
# ==========================================

def eliminar_producto():

    print("\n========================================")
    print("            ELIMINAR PRODUCTO")
    print("========================================")

    if len(productos) == 0:

        print("No hay productos registrados.")
        return

    id_eliminar = input("Ingrese el ID del producto a eliminar: ")

    for producto in productos:

        if producto[0] == id_eliminar:

            print("\nProducto encontrado:")
            print(f"Nombre: {producto[1]}")
            print(f"Categoría: {producto[2]}")
            print(f"Precio: Q{producto[3]:.2f}")
            print(f"Stock: {producto[4]}")

            confirmacion = input(
                "\n¿Está seguro de eliminarlo? (s/n): "
            ).lower()

            if confirmacion == "s":

                productos.remove(producto)

                print("\nProducto eliminado correctamente.")

            else:

                print("\nLa eliminación fue cancelada.")

            return

    print("\nNo se encontró un producto con ese ID.")


# ==========================================
# FUNCIÓN PARA MOSTRAR MENÚ
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

            agregar_producto()

        elif opcion == "2":

            listar_productos()

        elif opcion == "3":

            buscar_producto()

        elif opcion == "4":

            eliminar_producto()

        elif opcion == "5":

            realizar_venta(productos)

        elif opcion == "6":

            mostrar_estadisticas(productos)

        elif opcion == "7":

            print("\nGracias por utilizar NEXORA Gaming.")
            break

        else:

            print("\nOpción inválida. Seleccione una opción del 1 al 7.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if iniciar_sesion():

    mostrar_menu()

else:

    print("\nAcceso bloqueado. El programa finalizará.")
