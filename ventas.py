# ==========================================
# VENTAS
# NEXORA GAMING & TECHNOLOGY
# ==========================================

ventas = []


def realizar_venta(productos):
    print("\n========== REALIZAR VENTA ==========")

    id_producto = input("Ingrese el ID del producto: ")

    producto_encontrado = None

    for producto in productos:
        if producto[0] == id_producto:
            producto_encontrado = producto
            break

    if producto_encontrado is None:
        print("El producto no existe.")
        return

    print("\nProducto:", producto_encontrado[1])
    print("Precio: Q", producto_encontrado[3])
    print("Stock disponible:", producto_encontrado[4])

    cantidad = int(input("Ingrese la cantidad a vender: "))

    if cantidad <= 0:
        print("La cantidad debe ser mayor que 0.")
        return

    if cantidad > producto_encontrado[4]:
        print("No hay suficiente stock.")
        return

    subtotal = producto_encontrado[3] * cantidad

    producto_encontrado[4] = producto_encontrado[4] - cantidad

    ventas.append([
        producto_encontrado[0],
        producto_encontrado[1],
        cantidad,
        subtotal
    ])

    print("\nVenta realizada correctamente.")
    print("Producto:", producto_encontrado[1])
    print("Cantidad:", cantidad)
    print("Subtotal: Q", subtotal)
    print("Stock restante:", producto_encontrado[4])
