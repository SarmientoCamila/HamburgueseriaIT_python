import tkinter as tk 
from tkinter import messagebox
import sqlite3
import requests

# La API Key de Open Exchange Rates
API_KEY = "722bde358fcc4b09880a054f0128077b"

# URL de la API de Open Exchange Rates para obtener las tasas de cambio
url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"

def obtener_tasa_dolar():
    try:
        # Realizamos la solicitud a la API
        response = requests.get(url)
        
        # Verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            datos = response.json()
            # Obtenemos la tasa de USD a ARS
            tasa_usd_ars = datos['rates']['ARS']
            return tasa_usd_ars
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return None
    except Exception as e:
        print(f"Se produjo un error al obtener la tasa de cambio: {e}")
        return None

# Conexión a la base de datos
def conectar_bd():
    conn = sqlite3.connect('comercio.sqlite')
    return conn

# Función para hacer un pedido
def hacer_pedido():
    cliente = entry_cliente.get()
    combo_s = int(entry_combo_s.get() or 0)
    combo_d = int(entry_combo_d.get() or 0)
    combo_t = int(entry_combo_t.get() or 0)
    flurby = int(entry_flurby.get() or 0)
    total_dolares = combo_s * 5 + combo_d * 6 + combo_t * 7 + flurby * 2
    
    tasa_dolar = obtener_tasa_dolar()
    if tasa_dolar:
        total_pesos = total_dolares * tasa_dolar

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ventas (cliente, fecha, combo_s, combo_d, combo_t, flurby, total)
            VALUES (?, datetime('now'), ?, ?, ?, ?, ?)
        ''', (cliente, combo_s, combo_d, combo_t, flurby, total_pesos))
        conn.commit()
        conn.close()

        messagebox.showinfo("Pedido", f"Total en pesos: ${total_pesos:.2f}")
        limpiar_campos()
    else:
        messagebox.showerror("Error", "No se pudo obtener la tasa de cambio")

# Función para cancelar el pedido
def cancelar_pedido():
    entry_cliente.delete(0, tk.END)
    entry_combo_s.delete(0, tk.END)
    entry_combo_d.delete(0, tk.END)
    entry_combo_t.delete(0, tk.END)
    entry_flurby.delete(0, tk.END)

# Función para salir del sistema
def salir_seguro():
    nombre_encargado = entry_encargado.get()
    
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registro (encargado, fecha, evento, caja)
        VALUES (?, datetime('now'), 'OUT', 0) 
    ''', (nombre_encargado,))
    conn.commit()
    conn.close()

    root.quit()

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_cliente.delete(0, tk.END)
    entry_combo_s.delete(0, tk.END)
    entry_combo_d.delete(0, tk.END)
    entry_combo_t.delete(0, tk.END)
    entry_flurby.delete(0, tk.END)

# Crear ventana principal
root = tk.Tk()
root.title("Hamburguesas IT")

# Campo para el encargado
tk.Label(root, text="Encargado:").grid(row=0, column=0)
entry_encargado = tk.Entry(root)
entry_encargado.grid(row=0, column=1)

# Campos para el pedido
tk.Label(root, text="Cliente:").grid(row=1, column=0)
entry_cliente = tk.Entry(root)
entry_cliente.grid(row=1, column=1)

tk.Label(root, text="Combo S:").grid(row=2, column=0)
entry_combo_s = tk.Entry(root)
entry_combo_s.grid(row=2, column=1)

tk.Label(root, text="Combo D:").grid(row=3, column=0)
entry_combo_d = tk.Entry(root)
entry_combo_d.grid(row=3, column=1)

tk.Label(root, text="Combo T:").grid(row=4, column=0)
entry_combo_t = tk.Entry(root)
entry_combo_t.grid(row=4, column=1)

tk.Label(root, text="Flurby:").grid(row=5, column=0)
entry_flurby = tk.Entry(root)
entry_flurby.grid(row=5, column=1)

# Botones
tk.Button(root, text="Hacer Pedido", command=hacer_pedido).grid(row=6, column=0)
tk.Button(root, text="Cancelar Pedido", command=cancelar_pedido).grid(row=6, column=1)
tk.Button(root, text="Salir Seguro", command=salir_seguro).grid(row=7, column=0, columnspan=2)

# Iniciar la aplicación
root.mainloop()
