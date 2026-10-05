```python id="4ohm0m"
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

    for producto in productos:

        if producto[0] == id_producto:
            print("\nYa existe un producto con ese ID.")
            return

    nombre = input("Nombre del producto: ")
    categoria = input("Categoría: ")

    while True:

        try:

            precio = float(input("Precio: "))

            if precio <= 0:
                print("El precio debe ser mayor que 0.")
            else:
                break

        except ValueError:
            print("Error: ingrese un precio válido.")

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
        f"{'STO
```
