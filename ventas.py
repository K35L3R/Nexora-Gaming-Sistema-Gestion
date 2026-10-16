
# ==========================================
# SISTEMA PRINCIPAL
# NEXORA GAMING & TECHNOLOGY
# ==========================================

import inventario
from usuario import iniciar_sesion
from ventas import realizar_venta, mostrar_estadisticas


def agregar_producto():
    print("\n========== AGREGAR PRODUCTO ==========")

    codigo = input("Ingrese el código del producto: ")
    nombre = input("Ingrese el nombre del producto: ")
    precio = input("Ingrese el precio de venta: Q ")
    stock = input("Ingrese la cantidad disponible: ")

    try:
        inventario.agregar_producto(codigo, nombre, precio, stock)
        print("\nProducto agregado correctamente.")
    except ValueError as error:
        print("\nError:", error)
    except OSError:
        print("\nError al guardar el producto.")


def listar_productos():
    print("\n========== LISTA DE PRODUCTOS ==========")

    productos = inventario.listar_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    print("-" * 75)
    print("{:<15} {:<30} {:>12} {:>10}".format(
        "CODIGO", "NOMBRE", "PRECIO", "STOCK"
    ))
    print("-" * 75)

    for producto in productos:
        print("{:<15} {:<30} Q{:>10.2f} {:>10}".format(
            producto["codigo"],
            producto["nombre"][:30],
            producto["precio"],
            producto["stock"]
        ))

    print("-" * 75)


def buscar_producto():
    print("\n========== BUSCAR PRODUCTO ==========")

    codigo = input("Ingrese el código del producto: ")
    producto = inventario.buscar_producto(codigo)

    if producto is None:
        print("\nEl producto no existe.")
        return

    print("\nProducto encontrado:")
    print("Código:", producto["codigo"])
    print("Nombre:", producto["nombre"])
    print("Precio: Q", format(producto["precio"], ".2f"))
    print("Stock disponible:", producto["stock"])


def eliminar_producto():
    print("\n========== ELIMINAR PRODUCTO ==========")

    codigo = input("Ingrese el código del producto: ")
    producto = inventario.buscar_producto(codigo)

    if producto is None:
        print("\nEl producto no existe.")
        return

    print("\nProducto:", producto["nombre"])
    print("Código:", producto["codigo"])

    confirmar = input(
        "¿Desea eliminarlo? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("\nOperación cancelada.")
        return

    try:
        inventario.eliminar_producto(codigo)
        print("\nProducto eliminado correctamente.")
    except ValueError as error:
        print("\nError:", error)
    except OSError:
        print("\nError al guardar los cambios.")


def registrar_venta():
    print("\n========== REALIZAR VENTA ==========")

    if not inventario.listar_productos():
        print("No hay productos registrados.")
        return

    realizar_venta()


def ver_estadisticas():
    mostrar_estadisticas()


def mostrar_menu(rol):
    while True:
        print("\n========================================")
        print("       NEXORA GAMING & TECHNOLOGY")
        print("========================================")
        print("Usuario con rol:", rol)
        print("----------------------------------------")

        if rol == "Administrador":
            print("1. Agregar producto")
            print("2. Listar productos")
            print("3. Buscar producto")
            print("4. Eliminar producto")
            print("5. Realizar venta")
            print("6. Estadísticas")
            print("7. Cerrar sesión")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                agregar_producto()
            elif opcion == "2":
                listar_productos()
            elif opcion == "3":
                buscar_producto()
            elif opcion == "4":
                eliminar_producto()
            elif opcion == "5":
                registrar_venta()
            elif opcion == "6":
                ver_estadisticas()
            elif opcion == "7":
                print("\nCerrando sesión...")
                break
            else:
                print("\nOpción no válida.")

        elif rol == "Vendedor":
            print("1. Listar productos")
            print("2. Buscar producto")
            print("3. Realizar venta")
            print("4. Estadísticas")
            print("5. Cerrar sesión")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                listar_productos()
            elif opcion == "2":
                buscar_producto()
            elif opcion == "3":
                registrar_venta()
            elif opcion == "4":
                ver_estadisticas()
            elif opcion == "5":
                print("\nCerrando sesión...")
                break
            else:
                print("\nOpción no válida.")

        elif rol == "Encargado de Inventario":
            print("1. Agregar producto")
            print("2. Listar productos")
            print("3. Buscar producto")
            print("4. Eliminar producto")
            print("5. Estadísticas")
            print("6. Cerrar sesión")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                agregar_producto()
            elif opcion == "2":
                listar_productos()
            elif opcion == "3":
                buscar_producto()
            elif opcion == "4":
                eliminar_producto()
            elif opcion == "5":
                ver_estadisticas()
            elif opcion == "6":
                print("\nCerrando sesión...")
                break
            else:
                print("\nOpción no válida.")

        else:
            print("\nRol no reconocido.")
            break


def main():
    try:
        inventario.cargar_productos()
    except (OSError, ValueError, KeyError) as error:
        print("\nError al cargar el inventario:", error)
        return

    print("========================================")
    print("       BIENVENIDO A NEXORA")
    print("========================================")

    while True:
        usuario, rol = iniciar_sesion()

        if usuario is None:
            print("\nSaliendo del sistema...")
            break

        mostrar_menu(rol)


if __name__ == "__main__":
    main()
