import sqlite3
import time

# Definir combos y precios
combos = {
    "Combo Simple": 5,
    "Combo Doble": 6,
    "Combo Triple": 7,
    "McFlurby": 2
}

# Función para conectar a la base de datos y crear tablas si no existen
def inicializar_db():
    conn = sqlite3.connect('comercio.sqlite')
    cursor = conn.cursor()
    
    # Crear tabla ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        fecha TEXT,
        combo_s INTEGER,
        combo_d INTEGER,
        combo_t INTEGER,
        flurby INTEGER,
        total REAL
    )
    ''')

    # Crear tabla registro
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        encargado TEXT,
        fecha TEXT,
        evento TEXT,
        caja REAL
    )
    ''')

    conn.commit()
    return conn

# Función para registrar ventas en la base de datos
def registrar_venta(conn, cliente, cant_simple, cant_doble, cant_triple, cant_flurby, total):
    fecha = time.strftime("%a %b %d %H:%M:%S %Y")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO ventas (cliente, fecha, combo_s, combo_d, combo_t, flurby, total)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (cliente, fecha, cant_simple, cant_doble, cant_triple, cant_flurby, total))
    conn.commit()
    
# #Ejemplo de clientes para migrar ventas.txt a la base de datos

# def migrar_datos_a_bd():
#     # Conectar a la base de datos
#     conn = sqlite3.connect('comercio.sqlite')
    
#     with open('ventas.txt', 'r') as file:
#         for line in file:
#             # Saltar la línea de encabezado si existe
#             if "Cliente" in line:
#                 continue
            
#             # Limpiar la línea y dividirla en partes
#             datos = line.strip().split(' ; ')
            
#             # Asignar los valores a variables
#             cliente = datos[0]
#             fecha = datos[1]
#             combo_s = int(datos[2])
#             combo_d = int(datos[3])
#             combo_t = int(datos[4])
#             flurby = int(datos[5])
#             total = float(datos[6])
            
#             # Insertar en la base de datos
#             registrar_venta(conn, cliente, fecha, combo_s, combo_d, combo_t, flurby, total)

#     # Cerrar la conexión a la base de datos
#     conn.close()

# # Ejecutar la migración
# migrar_datos_a_bd()



# #
    
    

# Función para registrar accesos y salidas en la base de datos
def registrar_acceso(conn, encargado, evento, monto_final=None):
    fecha = time.strftime("%a %b %d %H:%M:%S %Y")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO registro (encargado, fecha, evento, caja)
    VALUES (?, ?, ?, ?)
    ''', (encargado, fecha, evento, monto_final))
    conn.commit()

# Función para mostrar el menú principal
def mostrar_menu(encargado):
    print(f"\nHamburguesas IT\nEncargad@ -> {encargado}")
    print("1 – Ingreso nuevo pedido")
    print("2 – Cambio de turno")
    print("3 – Apagar sistema")

# Función para ingresar un nuevo pedido
def nuevo_pedido(conn):
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
        registrar_venta(conn, cliente, cant_simple, cant_doble, cant_triple, cant_flurby, total)
        print("Pedido confirmado.")
    else:
        print("Pedido cancelado.")

# Función para cambio de turno
def cambiar_turno(conn, encargado):
    total_caja = float(input("Ingrese el monto total en caja: "))
    registrar_acceso(conn, encargado, 'OUT', total_caja)
    
    nuevo_encargado = input("Ingrese nombre del nuevo encargad@: ")
    registrar_acceso(conn, nuevo_encargado, 'IN')
    
    return nuevo_encargado

# Función principal
def main():
    conn = inicializar_db()
    
    encargado = input("Bienvenido a Hamburguesas IT\nIngrese su nombre encargad@: ")
    registrar_acceso(conn, encargado, 'IN')

    while True:
        mostrar_menu(encargado)
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nuevo_pedido(conn)
        elif opcion == '2':
            encargado = cambiar_turno(conn, encargado)
        elif opcion == '3':
            total_caja = float(input("Ingrese el monto total en caja: "))
            registrar_acceso(conn, encargado, 'OUT', total_caja)
            print("Apagando sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    conn.close()

if __name__ == "__main__":
    main()
