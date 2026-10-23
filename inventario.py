
import csv
import os
import math

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "productos.csv")

CAMPOS = ["codigo", "nombre", "precio", "stock", "imagen"]

productos = []

IMAGENES = {
    "Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80",
    "Computadora": "https://images.unsplash.com/photo-1587831990711-23ca6441447b?auto=format&fit=crop&w=600&q=80",
    "Teclado": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
    "Mouse": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=600&q=80",
    "Audifonos": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
    "Monitor": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
    "Tarjeta grafica": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=600&q=80",
    "Procesador": "https://images.unsplash.com/photo-1555617981-dac3880eac6e?auto=format&fit=crop&w=600&q=80",
    "Consola": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=600&q=80",
    "Accesorio": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?auto=format&fit=crop&w=600&q=80"
}

CATALOGO = [
    ("Laptop", [
        ("Laptop Lenovo IdeaPad", 4299),
        ("Laptop HP Pavilion", 5199),
        ("Laptop ASUS VivoBook", 3899),
        ("Laptop Acer Aspire", 3699),
        ("Laptop Dell Inspiron", 5499),
        ("Laptop MSI Gaming", 8999),
        ("Laptop ASUS TUF Gaming", 8299),
        ("Laptop Lenovo Legion", 10999),
        ("Laptop HP Victus", 7499),
        ("Laptop Acer Nitro", 7999)
    ]),
    ("Computadora", [
        ("PC Gamer Ryzen 5", 6499),
        ("PC Gamer Ryzen 7", 8999),
        ("PC Gamer Intel Core i5", 6999),
        ("PC Gamer Intel Core i7", 9999),
        ("PC Oficina Intel Core i3", 3299),
        ("PC Oficina Ryzen 3", 3499),
        ("PC Gamer RTX 4060", 9499),
        ("PC Gamer RTX 4070", 13999),
        ("PC Gamer RGB Basica", 5799),
        ("PC Profesional", 7599)
    ]),
    ("Teclado", [
        ("Teclado mecanico Redragon", 450),
        ("Teclado Logitech G213", 599),
        ("Teclado Razer Huntsman", 1299),
        ("Teclado HyperX Alloy", 899),
        ("Teclado mecanico RGB", 399),
        ("Teclado compacto 60%", 349),
        ("Teclado inalambrico Logitech", 299),
        ("Teclado gamer T-Dagger", 279),
        ("Teclado Corsair K55", 699),
        ("Teclado USB basico", 125)
    ]),
    ("Mouse", [
        ("Mouse Logitech G203", 249),
        ("Mouse Logitech G502", 699),
        ("Mouse Razer DeathAdder", 599),
        ("Mouse Redragon Cobra", 299),
        ("Mouse gamer RGB", 179),
        ("Mouse inalambrico Logitech", 199),
        ("Mouse HyperX Pulsefire", 499),
        ("Mouse Corsair Harpoon", 399),
        ("Mouse ergonomico USB", 159),
        ("Mouse optico basico", 65)
    ]),
    ("Audifonos", [
        ("Audifonos JBL Quantum 100", 399),
        ("Audifonos HyperX Cloud II", 799),
        ("Audifonos Logitech G435", 699),
        ("Audifonos Razer Kraken", 749),
        ("Audifonos Redragon Zeus", 499),
        ("Audifonos gamer RGB", 299),
        ("Audifonos Bluetooth JBL", 599),
        ("Audifonos Sony WH", 999),
        ("Audifonos Corsair HS55", 649),
        ("Audifonos USB basicos", 149)
    ]),
    ("Monitor", [
        ("Monitor LG 24 pulgadas", 1199),
        ("Monitor Samsung 27 pulgadas", 1799),
        ("Monitor gamer ASUS 144Hz", 2199),
        ("Monitor MSI 165Hz", 2499),
        ("Monitor AOC 24 pulgadas", 1399),
        ("Monitor gamer curvo 27", 2899),
        ("Monitor Acer Nitro", 2299),
        ("Monitor Dell Full HD", 1499),
        ("Monitor LG UltraGear", 2699),
        ("Monitor Samsung 32 pulgadas", 3299)
    ]),
    ("Tarjeta grafica", [
        ("Tarjeta grafica RTX 3050", 1999),
        ("Tarjeta grafica RTX 4060", 2799),
        ("Tarjeta grafica RTX 4060 Ti", 3699),
        ("Tarjeta grafica RTX 4070", 4899),
        ("Tarjeta grafica RTX 4070 Super", 5799),
        ("Tarjeta grafica GTX 1660", 1599),
        ("Tarjeta grafica RX 6600", 1899),
        ("Tarjeta grafica RX 7600", 2699),
        ("Tarjeta grafica RX 7700 XT", 4199),
        ("Tarjeta grafica RTX 4080", 9999)
    ]),
    ("Procesador", [
        ("Procesador Ryzen 5 5600", 999),
        ("Procesador Ryzen 5 7600", 1599),
        ("Procesador Ryzen 7 5700X", 1499),
        ("Procesador Ryzen 7 7800X3D", 3299),
        ("Procesador Ryzen 9 7900X", 3899),
        ("Procesador Intel Core i3", 799),
        ("Procesador Intel Core i5", 1299),
        ("Procesador Intel Core i7", 2299),
        ("Procesador Intel Core i9", 3999),
        ("Procesador Ryzen 3", 699)
    ]),
    ("Consola", [
        ("Consola PlayStation 5", 4999),
        ("Consola Xbox Series X", 4799),
        ("Consola Xbox Series S", 2499),
        ("Nintendo Switch OLED", 2399),
        ("Nintendo Switch Lite", 1399),
        ("Control PlayStation 5", 499),
        ("Control Xbox inalambrico", 449),
        ("Control Nintendo Switch", 399),
        ("Consola retro portatil", 499),
        ("Base de carga para controles", 199)
    ]),
    ("Accesorio", [
        ("SSD 500 GB", 399),
        ("SSD 1 TB", 649),
        ("Disco duro 1 TB", 449),
        ("Memoria RAM 16 GB", 399),
        ("Memoria RAM 32 GB", 749),
        ("Fuente de poder 650W", 699),
        ("Fuente de poder 750W", 899),
        ("Gabinete gamer RGB", 799),
        ("Ventiladores RGB", 249),
        ("UPS para computadora", 599)
    ])
]


def crear_catalogo_inicial():
    iniciales = []
    numero = 1

    for categoria, articulos in CATALOGO:
        for nombre, precio in articulos:
            iniciales.append({
                "codigo": "NX" + str(numero).zfill(3),
                "nombre": nombre,
                "precio": float(precio),
                "stock": 10,
                "imagen": IMAGENES[categoria]
            })
            numero += 1

    return iniciales


def guardar_productos():
    temporal = ARCHIVO + ".tmp"

    with open(temporal, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=CAMPOS
        )
        escritor.writeheader()
        escritor.writerows(productos)

    os.replace(temporal, ARCHIVO)


def cargar_productos():
    productos.clear()

    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                codigo = (fila.get("codigo") or "").strip().upper()
                nombre = (fila.get("nombre") or "").strip()

                if not codigo or not nombre:
                    continue

                try:
                    precio = float(fila.get("precio") or 0)
                    stock = int(fila.get("stock") or 0)
                except (ValueError, TypeError):
                    continue

                if not math.isfinite(precio) or stock < 0:
                    continue

                imagen = (fila.get("imagen") or "").strip()

                productos.append({
                    "codigo": codigo,
                    "nombre": nombre,
                    "precio": precio,
                    "stock": stock,
                    "imagen": imagen or IMAGENES["Accesorio"]
                })

    # Crear el catálogo inicial solamente si el inventario está vacío.
    if not productos:
        productos.extend(crear_catalogo_inicial())
        guardar_productos()

    # Actualizar el formato del CSV antiguo para incluir la columna imagen.
    else:
        guardar_productos()


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

    return [
        producto for producto in productos
        if termino in producto["codigo"].casefold()
        or termino in producto["nombre"].casefold()
    ]


def agregar_producto(codigo, nombre, precio, stock, imagen=""):
    codigo = str(codigo).strip().upper()
    nombre = str(nombre).strip()

    if not codigo or not nombre:
        raise ValueError("El código y el nombre son obligatorios.")

    if buscar_producto(codigo):
        raise ValueError("El código ya está registrado.")

    try:
        precio = float(precio)
    except (ValueError, TypeError):
        raise ValueError("El precio debe ser un número válido.")

    if not math.isfinite(precio) or precio <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    try:
        texto_stock = str(stock).strip()

        if not texto_stock or not texto_stock.isdecimal():
            raise ValueError

        stock = int(texto_stock)

    except (ValueError, TypeError):
        raise ValueError(
            "El stock debe ser un entero igual o mayor que cero."
        )

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "imagen": str(imagen).strip() or IMAGENES["Accesorio"]
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


cargar_productos()
