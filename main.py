import csv
import os   
import tkinter as tk
from tkinter import ttk, messagebox

import inventario


# Ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Inventario")
ventana.geometry("850x550")
ventana.minsize(750, 450)


# Variables
codigo = tk.StringVar()
nombre = tk.StringVar()
precio = tk.StringVar()
cantidad = tk.StringVar()


# Limpiar campos
def limpiar():
    codigo.set("")
    nombre.set("")
    precio.set("")
    cantidad.set("")


# Mostrar productos en la tabla
def mostrar_productos(lista=None):
    for fila in tabla.get_children():
        tabla.delete(fila)

    if lista is None:
        lista = inventario.listar_productos()

    for producto in lista:
        tabla.insert(
            "",
            tk.END,
            values=(
                producto["codigo"],
                producto["nombre"],
                f"Q{producto['precio']:.2f}",
                producto["cantidad"]
            )
        )


# Agregar producto
def agregar():
    try:
        inventario.agregar_producto(
            codigo.get(),
            nombre.get(),
            precio.get(),
            cantidad.get()
        )

        messagebox.showinfo(
            "Éxito",
            "Producto agregado correctamente."
        )

        limpiar()
        mostrar_productos()

    except (ValueError, OSError) as error:
        messagebox.showerror("Error", str(error))


# Buscar producto
def buscar():
    if codigo.get().strip() == "":
        messagebox.showwarning(
            "Advertencia",
            "Ingresa el código del producto."
        )
        return

    producto = inventario.buscar_producto(codigo.get())

    if producto is None:
        messagebox.showinfo(
            "Resultado",
            "No se encontró el producto."
        )
        return

    nombre.set(producto["nombre"])
    precio.set(str(producto["precio"]))
    cantidad.set(str(producto["cantidad"]))

    mostrar_productos([producto])


# Eliminar producto
def eliminar():
    if codigo.get().strip() == "":
        messagebox.showwarning(
            "Advertencia",
            "Ingresa el código del producto."
        )
        return

    producto = inventario.buscar_producto(codigo.get())

    if producto is None:
        messagebox.showerror(
            "Error",
            "El producto no existe."
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Deseas eliminar {producto['nombre']}?"
    )

    if confirmar:
        try:
            inventario.eliminar_producto(codigo.get())

            messagebox.showinfo(
                "Éxito",
                "Producto eliminado correctamente."
            )

            limpiar()
            mostrar_productos()

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))


# Seleccionar producto desde la tabla
def seleccionar(evento):
    seleccion = tabla.selection()

    if not seleccion:
        return

    valores = tabla.item(seleccion[0], "values")

    codigo.set(valores[0])
    nombre.set(valores[1])
    precio.set(valores[2].replace("Q", ""))
    cantidad.set(valores[3])


# Título
titulo = tk.Label(
    ventana,
    text="SISTEMA DE INVENTARIO",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=15)


# Formulario
formulario = tk.LabelFrame(
    ventana,
    text="Datos del producto",
    padx=15,
    pady=15
)
formulario.pack(fill="x", padx=20, pady=10)


tk.Label(formulario, text="Código:").grid(
    row=0, column=0, padx=5, pady=5
)

tk.Entry(formulario, textvariable=codigo).grid(
    row=0, column=1, padx=5, pady=5
)

tk.Label(formulario, text="Nombre:").grid(
    row=0, column=2, padx=5, pady=5
)

tk.Entry(formulario, textvariable=nombre).grid(
    row=0, column=3, padx=5, pady=5
)

tk.Label(formulario, text="Precio:").grid(
    row=1, column=0, padx=5, pady=5
)

tk.Entry(formulario, textvariable=precio).grid(
    row=1, column=1, padx=5, pady=5
)

tk.Label(formulario, text="Cantidad:").grid(
    row=1, column=2, padx=5, pady=5
)

tk.Entry(formulario, textvariable=cantidad).grid(
    row=1, column=3, padx=5, pady=5
)


# Botones
botones = tk.Frame(ventana)
botones.pack(pady=15)

ttk.Button(
    botones,
    text="Agregar",
    command=agregar
).pack(side="left", padx=5)

ttk.Button(
    botones,
    text="Buscar",
    command=buscar
).pack(side="left", padx=5)

ttk.Button(
    botones,
    text="Eliminar",
    command=eliminar
).pack(side="left", padx=5)

ttk.Button(
    botones,
    text="Listar todos",
    command=mostrar_productos
).pack(side="left", padx=5)

ttk.Button(
    botones,
    text="Limpiar",
    command=limpiar
).pack(side="left", padx=5)


# Tabla
contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True, padx=20, pady=10)

columnas = ("codigo", "nombre", "precio", "cantidad")

tabla = ttk.Treeview(
    contenedor,
    columns=columnas,
    show="headings"
)

tabla.heading("codigo", text="Código")
tabla.heading("nombre", text="Nombre")
tabla.heading("precio", text="Precio")
tabla.heading("cantidad", text="Cantidad")

tabla.column("codigo", width=100)
tabla.column("nombre", width=250)
tabla.column("precio", width=120)
tabla.column("cantidad", width=100)

scroll = ttk.Scrollbar(
    contenedor,
    orient="vertical",
    command=tabla.yview
)

tabla.configure(yscrollcommand=scroll.set)

tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

tabla.bind("<<TreeviewSelect>>", seleccionar)


# Cargar datos y ejecutar
try:
    inventario.cargar_productos()
    mostrar_productos()
except (ValueError, KeyError, OSError, csv.Error) as error:
    messagebox.showerror(
        "Error de carga",
        f"No se pudieron cargar los productos: {error}"
    )

ventana.mainloop()
