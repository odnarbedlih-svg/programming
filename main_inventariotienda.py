inventario = {}


def agregar_producto():
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    cantidad = int(input("Cantidad: "))

    if nombre in inventario:
        inventario[nombre]['cantidad'] += cantidad
    else:
        inventario[nombre] = {'precio': precio, 'cantidad': cantidad}

    print(f"Producto '{nombre}' agregado correctamente.\n")


def ver_inventario():
    if not inventario:
        print("Inventario vacío.\n")
        return

    print("\n--- INVENTARIO ---")
    for nombre, datos in inventario.items():
        print(f"Producto: {nombre} | Precio: {datos['precio']} | Cantidad: {datos['cantidad']}")
    print()


def vender_producto():
    nombre = input("Producto a vender: ")

    if nombre not in inventario:
        print("Producto no encontrado.\n")
        return

    cantidad = int(input("Cantidad a vender: "))

    if cantidad > inventario[nombre]['cantidad']:
        print("No hay suficiente stock.\n")
        return

    total = cantidad * inventario[nombre]['precio']
    inventario[nombre]['cantidad'] -= cantidad

    print("\n--- FACTURA ---")
    print(f"Producto: {nombre}")
    print(f"Cantidad: {cantidad}")
    print(f"Total a pagar: {total}")
    print("----------------\n")


def menu():
    while True:
        print("=== TIENDA ===")
menu()