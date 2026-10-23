import csv
import os
import math

ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "productos.csv"
)

CAMPOS = ["codigo", "nombre", "precio", "stock"]

productos = []


def cargar_productos():
    productos.clear()

    if not os.path.exists(ARCHIVO):
        return

    with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            producto = {
                "codigo": fila["codigo"].strip().upper(),
                "nombre": fila["nombre"].strip(),
                "precio": float(fila["precio"]),
                "stock": int(fila["stock"])
            }

            productos.append(producto)


def guardar_productos():
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=CAMPOS
        )

        escritor.writeheader()
        escritor.writerows(productos)


def buscar_producto(codigo):
    codigo = str(codigo).strip().upper()

    for producto in productos:
        if producto["codigo"] == codigo:
            return producto

    return None


def buscar_productos(termino):
    termino = str(termino).strip().casefold()

    if not termino:
        return productos.copy()

    resultados = []

    for producto in productos:
        codigo = producto["codigo"].casefold()
        nombre = producto["nombre"].casefold()

        if termino in codigo or termino in nombre:
            resultados.append(producto)

    return resultados


def agregar_producto(codigo, nombre, precio, stock):
    codigo = str(codigo).strip().upper()
    nombre = str(nombre).strip()

    if not codigo or not nombre:
        raise ValueError(
            "El código y el nombre son obligatorios."
        )

    if buscar_producto(codigo) is not None:
        raise ValueError(
            "El código ya está registrado."
        )

    try:
        precio = float(precio)
    except (ValueError, TypeError):
        raise ValueError(
            "El precio debe ser un número válido."
        )

    if not math.isfinite(precio) or precio <= 0:
        raise ValueError(
            "El precio debe ser mayor que cero."
        )

    try:
        stock_texto = str(stock).strip()

        if not stock_texto or not stock_texto.isdecimal():
            raise ValueError

        stock = int(stock_texto)

    except (ValueError, TypeError):
        raise ValueError(
            "El stock debe ser un número entero igual o mayor que cero."
        )

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock
    }

    productos.append(producto)

    try:
        guardar_productos()
    except OSError:
        productos.remove(producto)
        raise


def listar_productos():
    return productos.copy()


def eliminar_producto(codigo):
    producto = buscar_producto(codigo)

    if producto is None:
        raise ValueError(
            "El producto no existe."
        )

    posicion = productos.index(producto)
    productos.remove(producto)

    try:
        guardar_productos()
    except OSError:
        productos.insert(posicion, producto)
        raise
