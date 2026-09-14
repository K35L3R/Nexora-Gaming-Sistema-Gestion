# ==========================================
# NEXORA GAMING & TECHNOLOGY
# Sistema de Gestión de Inventario y Ventas
# ==========================================


# ==========================================
# DATOS DE ACCESO
# ==========================================

USUARIO_CORRECTO = "admin"
CONTRASENA_CORRECTA = "1234"


# ==========================================
# LISTAS DEL SISTEMA
# ==========================================

productos = []

ventas = []


# ==========================================
# FUNCIÓN DE LOGIN
# ==========================================

def iniciar_sesion():

    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:

        print("\n========================================")
        print("       NEXORA GAMING & TECHNOLOGY")
        print("          SISTEMA DE GESTIÓN")
        print("========================================")

        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:

            print("\n✓ Acceso concedido.")
            return True

        else:

            intentos += 1
            restantes = max_intentos - intentos

            print("\n✗ Usuario o contraseña incorrectos.")

            if restantes > 0:
                print(f"Intentos restantes: {restantes}")
            else:
                print("Se alcanzó el número máximo de intentos.")

    return False


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
            print("\n✗ Ya existe un producto con ese ID.")
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

    producto = [id_producto, nombre, categoria, precio, cantidad]

    productos.append(producto)

    print("\n✓ Producto agregado correctamente.")


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

            print("\n✓ Producto encontrado.")
            print(f"ID: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Categoría: {producto[2]}")
            print(f"Precio: Q{producto[3]:.2f}")
            print(f"Stock: {producto[4]}")

            encontrado = True
            break

    if encontrado == False:

        print("\n✗ No se encontró un producto con ese ID.")


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

                print("\n✓ Producto eliminado correctamente.")

            else:

                print("\nLa eliminación fue cancelada.")

            return

    print("\n✗ No se encontró un producto con ese ID.")


# ==========================================
# FUNCIÓN PARA REALIZAR UNA VENTA
# ==========================================

def realizar_venta():

    print("\n========================================")
    print("             REALIZAR VENTA")
    print("========================================")

    if len(productos) == 0:

        print("No hay productos registrados.")
        return

    id_venta = input("Ingrese el ID del producto: ")

    producto_encontrado = None

    for producto in productos:

        if producto[0] == id_venta:

            producto_encontrado = producto
            break

    if producto_encontrado is None:

        print("\n✗ No se encontró un producto con ese ID.")
        return

    print(f"\nProducto: {producto_encontrado[1]}")
    print(f"Precio: Q{producto_encontrado[3]:.2f}")
    print(f"Stock disponible: {producto_encontrado[4]}")

    while True:

        try:

            cantidad_venta = int(
                input("Cantidad a vender: ")
            )

            if cantidad_venta <= 0:

                print("La cantidad debe ser mayor que 0.")

            elif cantidad_venta > producto_encontrado[4]:

                print("No hay suficiente stock.")

            else:

                break

        except ValueError:

            print("Error: ingrese una cantidad válida.")

    subtotal = producto_encontrado[3] * cantidad_venta

    # Actualizar stock
    producto_encontrado[4] -= cantidad_venta

    # Registrar venta
    venta = [
        producto_encontrado[0],
        producto_encontrado[1],
        cantidad_venta,
        subtotal
    ]

    ventas.append(venta)

    print("\n========================================")
    print("           VENTA REALIZADA")
    print("========================================")
    print(f"Producto: {producto_encontrado[1]}")
    print(f"Cantidad: {cantidad_venta}")
    print(f"Precio unitario: Q{producto_encontrado[3]:.2f}")
    print(f"Subtotal: Q{subtotal:.2f}")
    print(f"Stock restante: {producto_encontrado[4]}")


# ==========================================
# FUNCIÓN PARA MOSTRAR ESTADÍSTICAS
# ==========================================

def mostrar_estadisticas():

    print("\n========================================")
    print("              ESTADÍSTICAS")
    print("========================================")

    if len(productos) == 0:

        print("No hay productos registrados.")
        return

    total_productos = len(productos)

    stock_total = 0
    valor_inventario = 0

    precio_mayor = productos[0]
    precio_menor = productos[0]

    for producto in productos:

        stock_total += producto[4]

        valor_inventario += producto[3] * producto[4]

        if producto[3] > precio_mayor[3]:
            precio_mayor = producto

        if producto[3] < precio_menor[3]:
            precio_menor = producto

    # Calcular promedio de precios
    suma_precios = 0

    for producto in productos:

        suma_precios += producto[3]

    promedio_precio = suma_precios / total_productos

    # Calcular ventas
    total_ventas = 0
    cantidad_vendida = 0

    for venta in ventas:

        cantidad_vendida += venta[2]
        total_ventas += venta[3]

    print(f"Cantidad de productos registrados: {total_productos}")
    print(f"Unidades disponibles en inventario: {stock_total}")
    print(f"Valor total del inventario: Q{valor_inventario:.2f}")
    print(f"Precio promedio: Q{promedio_precio:.2f}")

    print("\nProducto con mayor precio:")
    print(f"{precio_mayor[1]} - Q{precio_mayor[3]:.2f}")

    print("\nProducto con menor precio:")
    print(f"{precio_menor[1]} - Q{precio_menor[3]:.2f}")

    print("\nInformación de ventas:")
    print(f"Cantidad de unidades vendidas: {cantidad_vendida}")
    print(f"Total de ventas: Q{total_ventas:.2f}")


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

            realizar_venta()

        elif opcion == "6":

            mostrar_estadisticas()

        elif opcion == "7":

            print("\nGracias por utilizar NEXORA Gaming.")
            break

        else:

            print("\n✗ Opción inválida. Seleccione una opción del 1 al 7.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if iniciar_sesion():

    mostrar_menu()

else:

    print("\nAcceso bloqueado. El programa finalizará.")
