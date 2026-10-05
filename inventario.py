import csv
import os
import math

ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "productos.csv"
)

CAMPOS = ["codigo", "nombre", "precio", "cantidad"]
productos = []


def cargar_productos():
    productos.clear()

    if not os.path.exists(ARCHIVO):
        return

    with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            producto = {
                "codigo": fila["codigo"],
                "nombre": fila["nombre"],
                "precio": float(fila["precio"]),
                "cantidad": int(fila["cantidad"])
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
    codigo = codigo.strip().upper()

    for producto in productos:
        if producto["codigo"] == codigo:
            return producto

    return None


def agregar_producto(codigo, nombre, precio, cantidad):
    codigo = codigo.strip().upper()
    nombre = nombre.strip()

    if codigo == "" or nombre == "":
        raise ValueError("El código y el nombre son obligatorios.")

    if buscar_producto(codigo):
        raise ValueError("El código ya está registrado.")

    try:
        precio = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        raise ValueError("El precio o la cantidad no son válidos.")

    if not math.isfinite(precio) or precio <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa.")

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
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
        raise ValueError("El producto no existe.")

    posicion = productos.index(producto)
    productos.remove(producto)

    try:
        guardar_productos()
    except OSError:
        productos.insert(posicion, producto)
        raise
