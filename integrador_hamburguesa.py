import time

# Definir combos y precios
combos = {
    "Combo Simple": 5,
    "Combo Doble": 6,
    "Combo Triple": 7,
    "McFlurby": 2
}

# Función para mostrar el menú principal 
def mostrar_menu(encargado):
    print(f"\nHamburguesas IT\nEncargad@ -> {encargado}")
    print("1 – Ingreso nuevo pedido")
    print("2 – Cambio de turno")
    print("3 – Apagar sistema")

# Función para registrar ventas
def registrar_venta(cliente, cant_simple, cant_doble, cant_triple, cant_flurby, total):
    fecha = time.strftime("%a %b %d %H:%M:%S %Y")
    with open('ventas.txt', 'a') as ventas_file:
        ventas_file.write(f"{cliente}; {fecha}; {cant_simple}; {cant_doble}; {cant_triple}; {cant_flurby}; {total}\n")

# Función para ingresar un nuevo pedido
def nuevo_pedido():
    cliente = input("Ingrese nombre del cliente: ")
    cant_simple = int(input("Ingrese cantidad Combo S: "))
    cant_doble = int(input("Ingrese cantidad Combo D: "))
    cant_triple = int(input("Ingrese cantidad Combo T: "))
    cant_flurby = int(input("Ingrese cantidad Flurby: "))

    total = (cant_simple * combos["Combo Simple"] +
             cant_doble * combos["Combo Doble"] +
             cant_triple * combos["Combo Triple"] +
             cant_flurby * combos["McFlurby"])

    print(f"Total: ${total}")
    abona = float(input("Abona con $: "))
    vuelto = abona - total
    print(f"Vuelto: ${vuelto}")

    confirmar = input("¿Confirma pedido? Y/N: ").lower()
    if confirmar == 'y':
        registrar_venta(cliente, cant_simple, cant_doble, cant_triple, cant_flurby, total)
        print("Pedido confirmado.")
    else:
        print("Pedido cancelado.")

# Función para cambio de turno
def cambiar_turno():
    nuevo_encargado = input("Ingrese nombre del nuevo encargad@: ")
    return nuevo_encargado

# Función principal
def main():
    encargado = input("Bienvenido a Hamburguesas IT\nIngrese su nombre encargad@: ")

    while True:
        mostrar_menu(encargado)
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nuevo_pedido()
        elif opcion == '2':
            encargado = cambiar_turno()
        elif opcion == '3':
            print("Apagando sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
