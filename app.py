import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('concesionaria.db')
cursor = conn.cursor()

# Crear tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS vehiculos (
                    id INTEGER PRIMARY KEY,
                    marca TEXT,
                    modelo TEXT,
                    año INTEGER,
                    precio REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    correo TEXT UNIQUE,
                    contrasena TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    contacto TEXT)''')
conn.commit()

# Función para verificar el login
def verificar_login():
    correo = entry_usuario.get()
    contrasena = entry_contrasena.get()
    cursor.execute("SELECT * FROM usuarios WHERE correo=? AND contrasena=?", (correo, contrasena))
    user = cursor.fetchone()
    if user:
        ventana_login.destroy()
        crear_ventana_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para crear un nuevo usuario
def crear_usuario():
    correo = entry_nuevo_usuario.get()
    contrasena = entry_nueva_contrasena.get()
    try:
        cursor.execute("INSERT INTO usuarios (correo, contrasena) VALUES (?, ?)", (correo, contrasena))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario creado correctamente")
        ventana_nuevo_usuario.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El correo ya está en uso")

# Función para crear la ventana principal
def crear_ventana_principal():
    global ventana
    ventana = tk.Tk()
    ventana.title("Sistema de Concesionaria")
    ventana.geometry("800x600")  # Tamaño de la ventana más grande

    # Título
    tk.Label(ventana, text="Sistema de Concesionaria", font=("Arial", 24)).pack(pady=10)

    # Crear un Notebook para pestañas
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill='both', expand=True)

    # Pestaña de agregar vehículos
    pestaña_agregar = ttk.Frame(notebook)
    notebook.add(pestaña_agregar, text='Agregar Vehículo')

    # Campos para agregar vehículo
    tk.Label(pestaña_agregar, text="Marca").grid(row=0, column=0)
    entry_marca = tk.Entry(pestaña_agregar)
    entry_marca.grid(row=0, column=1)

    tk.Label(pestaña_agregar, text="Modelo").grid(row=1, column=0)
    entry_modelo = tk.Entry(pestaña_agregar)
    entry_modelo.grid(row=1, column=1)

    tk.Label(pestaña_agregar, text="Año").grid(row=2, column=0)
    entry_año = tk.Entry(pestaña_agregar)
    entry_año.grid(row=2, column=1)

    tk.Label(pestaña_agregar, text="Precio").grid(row=3, column=0)
    entry_precio = tk.Entry(pestaña_agregar)
    entry_precio.grid(row=3, column=1)

    tk.Button(pestaña_agregar, text="Agregar Vehículo", command=lambda: agregar_vehiculo(entry_marca.get(), entry_modelo.get(), entry_año.get(), entry_precio.get())).grid(row=4, columnspan=2)

    # Pestaña de mostrar vehículos
    pestaña_mostrar = ttk.Frame(notebook)
    notebook.add(pestaña_mostrar, text='Vehículos')

    # Tabla para mostrar vehículos
    global tree
    tree = ttk.Treeview(pestaña_mostrar, columns=("ID", "Marca", "Modelo", "Año", "Precio"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Marca", text="Marca")
    tree.heading("Modelo", text="Modelo")
    tree.heading("Año", text="Año")
    tree.heading("Precio", text="Precio")
    tree.pack(fill='both', expand=True)

    tk.Button(pestaña_mostrar, text="Eliminar Vehículo", command=eliminar_vehiculo).pack(side='left')
    tk.Button(pestaña_mostrar, text="Modificar Vehículo", command=modificar_vehiculo).pack(side='left')
    tk.Button(pestaña_mostrar, text="Vender Vehículo", command=vender_vehiculo).pack(side='left')

    # Botón para cambiar el color de fondo
    tk.Button(ventana, text="Cambiar Color de Fondo", command=cambiar_color_fondo).pack(pady=10)

    actualizar_tabla()

    # Iniciar el bucle de la aplicación
    ventana.mainloop()

# Función para agregar un vehículo
def agregar_vehiculo(marca, modelo, año, precio):
    cursor.execute("INSERT INTO vehiculos (marca, modelo, año, precio) VALUES (?, ?, ?, ?)",
                   (marca, modelo, año, precio))
    conn.commit()
    messagebox.showinfo("Éxito", "El Vehículo fue agregado correctamente")
    actualizar_tabla()

# Función para actualizar la tabla de vehículos
def actualizar_tabla():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM vehiculos")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# Función para eliminar un vehículo
def eliminar_vehiculo():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM vehiculos WHERE id=?", (item_id,))
        conn.commit()
        messagebox.showinfo("Éxito", "Vehículo eliminado correctamente")
        actualizar_tabla()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un vehículo para eliminar")

# Función para modificar un vehículo
def modificar_vehiculo():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)['values'][0]
        cursor.execute("SELECT * FROM vehiculos WHERE id=?", (item_id,))
        vehiculo = cursor.fetchone()
        
        # Ventana para modificar
        ventana_modificar = tk.Toplevel(ventana)
        ventana_modificar.title("Modificar Vehículo")
        
        tk.Label(ventana_modificar, text="Marca").grid(row=0, column=0)
        entry_marca = tk.Entry(ventana_modificar)
        entry_marca.grid(row=0, column=1)
        entry_marca.insert(0, vehiculo[1])

        tk.Label(ventana_modificar, text="Modelo").grid(row=1, column=0)
        entry_modelo = tk.Entry(ventana_modificar)
        entry_modelo.grid(row=1, column=1)
        entry_modelo.insert(0, vehiculo[2])

        tk.Label(ventana_modificar, text="Año").grid(row=2, column=0)
        entry_año = tk.Entry(ventana_modificar)
        entry_año.grid(row=2, column=1)
        entry_año.insert(0, vehiculo[3])

        tk.Label(ventana_modificar, text="Precio").grid(row=3, column=0)
        entry_precio = tk.Entry(ventana_modificar)
        entry_precio.grid(row=3, column=1)
        entry_precio.insert(0, vehiculo[4])

        tk.Button(ventana_modificar, text="Modificar", command=lambda: guardar_modificacion(item_id, entry_marca.get(), entry_modelo.get(), entry_año.get(), entry_precio.get())).grid(row=4, columnspan=2)

    else:
        messagebox.showwarning("Advertencia", "Seleccione un vehículo para modificar")

def guardar_modificacion(item_id, marca, modelo, año, precio):
    cursor.execute("UPDATE vehiculos SET marca=?, modelo=?, año=?, precio=? WHERE id=?",
                   (marca, modelo, año, precio, item_id))
    conn.commit()
    messagebox.showinfo("Éxito", "Vehículo modificado correctamente")
    actualizar_tabla()

# Función para vender un vehículo
def vender_vehiculo():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM vehiculos WHERE id=?", (item_id,))
        conn.commit()
        messagebox.showinfo("Éxito", "Vehículo vendido correctamente")
        actualizar_tabla()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un vehículo para vender")

# Función para cambiar el color de fondo
def cambiar_color_fondo():
    if ventana.option_get('bg', 'white') == 'white':
        ventana.config(bg='black')
        for widget in ventana.winfo_children():
            widget.config(bg='black', fg='white')
    else:
        ventana.config(bg='white')
        for widget in ventana.winfo_children():
            widget.config(bg='white', fg='black')

# Ventana para crear un nuevo usuario
def ventana_crear_usuario():
    global ventana_nuevo_usuario, entry_nuevo_usuario, entry_nueva_contrasena
    ventana_nuevo_usuario = tk.Toplevel(ventana_login)
    ventana_nuevo_usuario.title("Crear Usuario")

    tk.Label(ventana_nuevo_usuario, text="Correo").pack()
    entry_nuevo_usuario = tk.Entry(ventana_nuevo_usuario)
    entry_nuevo_usuario.pack()

    tk.Label(ventana_nuevo_usuario, text="Contraseña").pack()
    entry_nueva_contrasena = tk.Entry(ventana_nuevo_usuario, show="*")
    entry_nueva_contrasena.pack()

    tk.Button(ventana_nuevo_usuario, text="Crear Usuario", command=crear_usuario).pack()

# Ventana de login
ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("300x200")

tk.Label(ventana_login, text="Usuario (Correo)").pack()
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Contraseña").pack()
entry_contrasena = tk.Entry(ventana_login, show="*")
entry_contrasena.pack()

tk.Button(ventana_login, text="Entrar", command=verificar_login).pack()
tk.Button(ventana_login, text="Crear Usuario", command=ventana_crear_usuario).pack()

# Iniciar el bucle de la aplicación
ventana_login.mainloop()

# Cerrar la conexión al salir
conn.close()
