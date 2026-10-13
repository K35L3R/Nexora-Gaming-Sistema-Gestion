
# ==========================================
# NEXORA GAMING & TECHNOLOGY
# Sistema de Gestión de Inventario y Ventas
# ==========================================

from usuario import iniciar_sesion
from ventas import realizar_venta, mostrar_estadisticas


# ==========================================
# LISTA DE PRODUCTOS
# ==========================================

productos = []


# ==========================================
# AGREGAR PRODUCTO
# ==========================================

def agregar_producto():
    print("\n========== AGREGAR PRODUCTO ==========")

    id_producto = input("ID del producto: ").strip().upper()

    if id_producto == "":
        print("El ID no puede estar vacío.")
        return

    for producto in productos:
        if producto[0] == id_producto:
            print("Ya existe un producto con ese ID.")
            return

    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoría: ").strip()

    if nombre == "" or categoria == "":
        print("El nombre y la categoría son obligatorios.")
        return

    while True:
        try:
            precio = float(input("Precio de venta (Q): "))

            if precio <= 0:
                print("El precio debe ser mayor que cero.")
            else:
                break

        except ValueError:
            print("Ingrese un precio válido.")

    while True:
        try:
            cantidad = int(input("Cantidad disponible: "))

            if cantidad < 0:
                print("La cantidad no puede ser negativa.")
            else:
                break

        except ValueError:
            print("Ingrese una cantidad válida.")

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
# LISTAR PRODUCTOS
# ==========================================

def listar_productos():
    print("\n========== INVENTARIO ==========")

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    print(
        f"{'ID':<12}"
        f"{'PRODUCTO':<25}"
        f"{'CATEGORÍA':<20}"
        f"{'PRECIO':<14}"
        f"{'STOCK':<8}"
    )

    print("-" * 79)

    for producto in productos:
        print(
            f"{producto[0]:<12}"
            f"{producto[1][:24]:<25}"
            f"{producto[2][:19]:<20}"
            f"Q{producto[3]:<13.2f}"
            f"{producto[4]:<8}"
        )


# ==========================================
# BUSCAR PRODUCTO
# ==========================================

def buscar_producto():
    print("\n========== BUSCAR PRODUCTO ==========")

    id_buscar = input("Ingrese el ID del producto: ").strip().upper()

    for producto in productos:
        if producto[0] == id_buscar:
            print("\nProducto encontrado.")
            print("ID:", producto[0])
            print("Nombre:", producto[1])
            print("Categoría:", producto[2])
            print("Precio: Q", format(producto[3], ".2f"))
            print("Stock:", producto[4])
            return

    print("No se encontró un producto con ese ID.")


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

def eliminar_producto():
    print("\n========== ELIMINAR PRODUCTO ==========")

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    id_eliminar = input(
        "Ingrese el ID del producto que desea eliminar: "
    ).strip().upper()

    for producto in productos:
        if producto[0] == id_eliminar:
            print("\nProducto:", producto[1])
            print("Categoría:", producto[2])
            print("Precio: Q", format(producto[3], ".2f"))
            print("Stock:", producto[4])

            confirmacion = input(
                "¿Desea eliminarlo? (s/n): "
            ).strip().lower()

            if confirmacion == "s":
                productos.remove(producto)
                print("Producto eliminado correctamente.")
            else:
                print("Eliminación cancelada.")

            return

    print("No se encontró un producto con ese ID.")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

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

        elif rol == "Vendedor":
            print("1. Listar productos")
            print("2. Buscar producto")
            print("3. Realizar venta")
            print("4. Estadísticas")
            print("5. Cerrar sesión")

        elif rol == "Encargado de Inventario":
            print("1. Agregar producto")
            print("2. Listar productos")
            print("3. Buscar producto")
            print("4. Eliminar producto")
            print("5. Estadísticas")
            print("6. Cerrar sesión")

        else:
            print("Rol no reconocido.")
            return

        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        # OPCIONES DEL ADMINISTRADOR
        if rol == "Administrador":

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
                print("Sesión cerrada correctamente.")
                break

            else:
                print("Opción inválida.")

        # OPCIONES DEL VENDEDOR
        elif rol == "Vendedor":

            if opcion == "1":
                listar_productos()

            elif opcion == "2":
                buscar_producto()

            elif opcion == "3":
                realizar_venta(productos)

            elif opcion == "4":
                mostrar_estadisticas(productos)

            elif opcion == "5":
                print("Sesión cerrada correctamente.")
                break

            else:
                print("Opción inválida.")

        # OPCIONES DEL ENCARGADO DE INVENTARIO
        elif rol == "Encargado de Inventario":

            if opcion == "1":
                agregar_producto()

            elif opcion == "2":
                listar_productos()

            elif opcion == "3":
                buscar_producto()

            elif opcion == "4":
                eliminar_producto()

            elif opcion == "5":
                mostrar_estadisticas(productos)

            elif opcion == "6":
                print("Sesión cerrada correctamente.")
                break

            else:
                print("Opción inválida.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    usuario, rol = iniciar_sesion()

    if usuario is not None:
        mostrar_menu(rol)
    else:
        print("Acceso bloqueado. El programa finalizará.")


if __name__ == "__main__":
    main()
