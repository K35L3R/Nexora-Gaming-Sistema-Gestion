
import csv
import os
from datetime import datetime

import inventario


ARCHIVO_VENTAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ventas.csv"
)

CAMPOS_VENTA = [
    "fecha",
    "usuario",
    "codigo",
    "producto",
    "cantidad",
    "precio_unitario",
    "total"
]


def obtener_ventas():
    if not os.path.exists(ARCHIVO_VENTAS):
        return []

    with open(ARCHIVO_VENTAS, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        ventas = []

        for fila in lector:
            try:
                ventas.append({
                    "fecha": fila["fecha"],
                    "usuario": fila["usuario"],
                    "codigo": fila["codigo"],
                    "producto": fila["producto"],
                    "cantidad": int(fila["cantidad"]),
                    "precio_unitario": float(fila["precio_unitario"]),
                    "total": float(fila["total"])
                })
            except (KeyError, TypeError, ValueError):
                continue

    return ventas


def guardar_venta(venta):
    archivo_existe = (
        os.path.exists(ARCHIVO_VENTAS)
        and os.path.getsize(ARCHIVO_VENTAS) > 0
    )

    with open(ARCHIVO_VENTAS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_VENTA)

        if not archivo_existe:
            escritor.writeheader()

        escritor.writerow(venta)


def realizar_venta(codigo=None, cantidad=None, usuario=None):
    modo_terminal = codigo is None or cantidad is None

    if modo_terminal:
        codigo = input("Ingrese el código del producto: ").strip().upper()

        try:
            cantidad = int(input("Ingrese la cantidad a vender: "))
        except ValueError:
            print("Error: la cantidad debe ser un número entero.")
            return None

    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
        if modo_terminal:
            print("Error: la cantidad debe ser un entero mayor que cero.")
        return None

    inventario.cargar_productos()
    producto = inventario.buscar_producto(str(codigo).strip().upper())

    if producto is None:
        if modo_terminal:
            print("Error: el producto no existe.")
        return None

    try:
        stock_actual = int(producto["stock"])
        precio = float(producto["precio"])
    except (KeyError, TypeError, ValueError):
        if modo_terminal:
            print("Error: los datos del producto no son válidos.")
        return None

    if cantidad > stock_actual:
        if modo_terminal:
            print("Error: no hay suficientes unidades disponibles.")
        return None

    if precio < 0:
        if modo_terminal:
            print("Error: el precio del producto no es válido.")
        return None

    venta = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": usuario or "Sistema",
        "codigo": producto["codigo"],
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": precio,
        "total": round(precio * cantidad, 2)
    }

    producto["stock"] = stock_actual - cantidad

    try:
        inventario.guardar_productos()
    except (OSError, ValueError, TypeError) as error:
        producto["stock"] = stock_actual

        if modo_terminal:
            print("Error al actualizar el inventario:", error)

        return None

    try:
        guardar_venta(venta)
    except (OSError, ValueError, TypeError, csv.Error) as error:
        producto["stock"] = stock_actual

        try:
            inventario.guardar_productos()
        except (OSError, ValueError, TypeError):
            pass

        if modo_terminal:
            print("Error al guardar la venta:", error)

        return None

    if modo_terminal:
        print("\nVenta registrada correctamente.")
        print("Producto:", venta["producto"])
        print("Cantidad:", venta["cantidad"])
        print("Precio unitario: Q", format(precio, ".2f"))
        print("Total: Q", format(venta["total"], ".2f"))

    return venta


def obtener_estadisticas():
    ventas = obtener_ventas()

    return {
        "cantidad_ventas": len(ventas),
        "unidades_vendidas": sum(v["cantidad"] for v in ventas),
        "ingresos": round(sum(v["total"] for v in ventas), 2),
        "ventas": ventas
    }


def mostrar_estadisticas():
    estadisticas = obtener_estadisticas()

    print("\n========== ESTADÍSTICAS DE VENTAS ==========")
    print("Cantidad de ventas:", estadisticas["cantidad_ventas"])
    print("Unidades vendidas:", estadisticas["unidades_vendidas"])
    print("Ingresos: Q", format(estadisticas["ingresos"], ".2f"))

    if not estadisticas["ventas"]:
        print("Todavía no hay ventas registradas.")
        return

    print("\nHistorial de ventas:")

    for venta in estadisticas["ventas"]:
        print(
            venta["fecha"],
            "|", venta["producto"],
            "| Cantidad:", venta["cantidad"],
            "| Total: Q", format(venta["total"], ".2f")
        )
