
import csv
import os
from datetime import datetime

import inventario

ARCHIVO_VENTAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ventas.csv"
)


def registrar_venta(codigo, cantidad, usuario):
    inventario.cargar_productos()

    producto = inventario.buscar_producto(codigo)

    if producto is None:
        raise ValueError("El producto no existe.")

    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        raise ValueError("La cantidad debe ser un número entero.")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    if cantidad > producto["stock"]:
        raise ValueError("No hay suficiente stock disponible.")

    subtotal = producto["precio"] * cantidad
    stock_anterior = producto["stock"]

    producto["stock"] -= cantidad

    try:
        inventario.guardar_productos()
    except OSError:
        producto["stock"] = stock_anterior
        raise

    archivo_existe = os.path.exists(ARCHIVO_VENTAS)

    try:
        with open(
            ARCHIVO_VENTAS,
            "a",
            newline="",
            encoding="utf-8"
        ) as archivo:
            campos = [
                "fecha",
                "usuario",
                "codigo",
                "producto",
                "cantidad",
                "precio_unitario",
                "total"
            ]

            escritor = csv.DictWriter(
                archivo,
                fieldnames=campos
            )

            if not archivo_existe:
                escritor.writeheader()

            escritor.writerow({
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": usuario,
                "codigo": producto["codigo"],
                "producto": producto["nombre"],
                "cantidad": cantidad,
                "precio_unitario": producto["precio"],
                "total": subtotal
            })

    except OSError:
        producto["stock"] = stock_anterior
        inventario.guardar_productos()
        raise

    return subtotal


def obtener_estadisticas():
    ventas = []

    if not os.path.exists(ARCHIVO_VENTAS):
        return {
            "cantidad_ventas": 0,
            "unidades_vendidas": 0,
            "ingresos": 0.0,
            "ventas": []
        }

    with open(
        ARCHIVO_VENTAS,
        "r",
        newline="",
        encoding="utf-8"
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            ventas.append(fila)

    unidades = sum(int(v["cantidad"]) for v in ventas)
    ingresos = sum(float(v["total"]) for v in ventas)

    return {
        "cantidad_ventas": len(ventas),
        "unidades_vendidas": unidades,
        "ingresos": ingresos,
        "ventas": ventas
    }
