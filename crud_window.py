import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from PIL import Image, ImageTk
from hash_password import hash_existing_passwords
import os
import re
from datetime import datetime
from bst_cliente import ArbolClientes

   
class CRUDWindow:
    def __init__(self, master, tabla):
        self.master = master
        self.tabla = tabla
        self.master.title(f"CRUD - {tabla}")
        self.adjust_window_size() 
        self.conn = sqlite3.connect('empresa.db')
        self.c = self.conn.cursor()
        self.columns = self.get_columns_for_table(tabla)
        self.original_id_cliente = None
        self.tablas_visibles = False  # Inicializar el atributo tablas_visibles
        self.create_widgets()

    def adjust_window_size(self):
        self.master.update_idletasks()  # Asegurarse de que todos los widgets se hayan renderizado
        if self.tabla == "Clientes":
            self.master.state('zoomed')  # Abrir en ventana completa si es la tabla Clientes
        else:
            min_width = 800  # Establecer un ancho mínimo
            min_height = 600  # Establecer una altura mínima
            self.master.minsize(min_width, min_height)  # Aplicar el tamaño mínimo
            self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_height()}")

    def get_columns_for_table(self, tabla):
        self.c.execute(f"PRAGMA table_info({tabla})")
        info = self.c.fetchall()
        columns = [col[1] for col in info]
        return columns

    def create_widgets(self):
        # Main frames
        self.form_frame = ctk.CTkFrame(self.master)
        self.form_frame.pack(pady=20, fill='x')
    
        # Crear un estilo personalizado para DateEntry
        style = ttk.Style(self.master)
        style.theme_use('clam')  # Usar el tema 'clam' como base
        style.configure('my.DateEntry',
                        fieldbackground='#333333',  # Fondo del campo de entrada
                        background='#333333',  # Fondo del calendario
                        foreground='#FFFFFF',  # Color del texto
                        bordercolor='#444444',  # Color del borde
                        arrowcolor='#FFFFFF',  # Color de las flechas
                        selectbackground='#555555',  # Fondo de la selección
                        selectforeground='#FFFFFF')  # Color del texto de la selección
    
        # Identificar los campos de fecha
        date_fields = []
        if self.tabla == 'Clientes':
            date_fields = ['Fecha_Registro']
        elif self.tabla == 'Pago_Cliente':
            date_fields = ['Fecha_Pago']  # Ajusta el nombre del campo si es necesario
    
        self.form_entries = {}
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(self.form_frame, text=col)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
    
            if col in date_fields:
                # Usar DateEntry con el estilo personalizado
                entry = DateEntry(self.form_frame, date_pattern='y-mm-dd', style='my.DateEntry')
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            elif self.tabla == 'Pedido' and col == 'Nombre_Pedido':
                # Usar Combobox para Nombre_Pedido en la tabla Pedidos
                entry = ttk.Combobox(self.form_frame, values=["Pedido Santiago", "Pedido Starken"], state="")
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            else:
                entry = ctk.CTkEntry(self.form_frame, width=200)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.form_entries[col] = entry

        if self.tabla == 'Pedido':
            # Crear etiqueta para mostrar el cliente más frecuente
            self.cliente_frecuente_label = ctk.CTkLabel(
                self.master, 
                text="El cliente más frecuente es: ", 
                font=("Arial", 14),
                text_color="black"
            )
            self.cliente_frecuente_label.pack(pady=10)

            # Crear botón para calcular el cliente más frecuente
            self.cliente_frecuente_button = ctk.CTkButton(
                self.master,
                text="Presionar Cliente Frecuente",
                command=self.mostrar_cliente_frecuente_arbol,
                width=200,
                height=32
            )
            self.cliente_frecuente_button.pack(pady=5)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.master)
        self.button_frame.pack(pady=20, fill='x')
    
        # Crear botones individualmente
        insert_button = ctk.CTkButton(
            self.button_frame,
            text="Insertar",
            command=self.insertar_registro,
            width=100,
            height=32
        )
        insert_button.pack(side='left', padx=10)
    
        update_button = ctk.CTkButton(
            self.button_frame,
            text="Actualizar",
            command=self.update_record,
            width=100,
            height=32
        )
        update_button.pack(side='left', padx=10)
    
        delete_button = ctk.CTkButton(
            self.button_frame,
            text="Eliminar",
            command=self.delete_record,
            width=100,
            height=32
        )
        delete_button.pack(side='left', padx=10)
    
        clear_button = ctk.CTkButton(
            self.button_frame,
            text="Limpiar",
            command=self.clear_entries,
            width=100,
            height=32
        )
        clear_button.pack(side='left', padx=10)
    
        # Agregar botón de hash solo para la tabla de usuarios
        if self.tabla == "usuarios":
            hash_button = ctk.CTkButton(
                self.button_frame,
                text="Encriptar Contraseñas",
                command=self.hash_passwords,
                width=150,
                height=32
            )
            hash_button.pack(side='left', padx=10)
    
        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fotos_dir = os.path.join(current_dir, "fotos")
    
        # Botón para ocultar tablas
        ocultar_tabla_image_path = os.path.join(fotos_dir, "ocultar.png")
        ocultar_tabla_image = Image.open(ocultar_tabla_image_path)
        ocultar_tabla_image = ocultar_tabla_image.resize((20, 20), Image.LANCZOS)
        ocultar_tabla_photo = ImageTk.PhotoImage(ocultar_tabla_image)
        self.ocultar_tabla_photo = ocultar_tabla_photo  # Store reference to prevent garbage collection
    
        ocultar_tablas_button = ctk.CTkButton(
            self.form_frame,
            text="",
            image=ocultar_tabla_photo,
            command=self.ocultar_tablas,
            width=100,
            height=32
        )
        ocultar_tablas_button.place(x=380, y=5)
    
        # Treeview
        self.tree_frame = ctk.CTkFrame(self.master)
        self.tree_frame.pack_forget()  # Ocultar el frame de la tabla inicialmente
    
        # Estilo personalizado para Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', '#347083')])
    
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show='headings', style="Treeview")
        for col in self.columns:
            # Asociar el evento de clic al encabezado
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(_col))
            self.tree.column(col, width=100, stretch=tk.YES)
        self.tree.pack(side='left', fill='both', expand=True)
    
        # Inicializar el diccionario para el estado de orden
        self.tree_sort_reverse = {col: False for col in self.columns}
    
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
    
        # Leer y mostrar los registros de la tabla actual
        self.read_records()
        
    def mostrar_cliente_frecuente_arbol(self):
        try:
            # Obtener todos los ID_Cliente de la tabla Pedido
            self.c.execute("SELECT ID_Cliente FROM Pedido")
            pedidos = self.c.fetchall()
            
            # Construir el árbol binario de clientes
            arbol_clientes = ArbolClientes()
            for pedido in pedidos:
                id_cliente = pedido[0]
                arbol_clientes.insertar(id_cliente)
            
            # Encontrar el cliente más frecuente
            cliente_mas_frecuente, max_pedidos = arbol_clientes.encontrar_cliente_mas_frecuente()
            if cliente_mas_frecuente:
                # Obtener detalles del cliente más frecuente
                self.c.execute("SELECT Nombre, Primer_Apellido FROM Clientes WHERE ID_Cliente = ?", (cliente_mas_frecuente,))
                cliente_info = self.c.fetchone()
                if cliente_info:
                    nombre_completo = f"{cliente_info[0]} {cliente_info[1]}"
                    mensaje = f"El cliente más frecuente es: {nombre_completo} (ID: {cliente_mas_frecuente})\nCantidad de pedidos: {max_pedidos}"
                else:
                    mensaje = f"El cliente más frecuente es: {cliente_mas_frecuente}\nCantidad de pedidos: {max_pedidos}"
                self.cliente_frecuente_label.configure(text=mensaje)
            else:
                self.cliente_frecuente_label.configure(text="No hay pedidos registrados.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el cliente más frecuente: {e}", parent=self.master)    
    
    def hash_passwords(self):
        try:
            hash_existing_passwords()
            messagebox.showinfo("Hash Passwords", "Las contraseñas han sido hasheadas exitosamente.", parent=self.master)
        except Exception as e:
            messagebox.showerror("Error", f"Error al hashear las contraseñas: {e}", parent=self.master)
   
    def insertar_pedido(self, id_cliente, id_producto, cantidad, total):
        try:
            # Iniciar una transacción
            self.conn.execute('BEGIN TRANSACTION;')

            # Insertar el nuevo pedido
            query_pedido = "INSERT INTO pedido (ID_Cliente, ID_Producto, cantidad, total, estado) VALUES (?, ?, ?, ?, 'Pendiente')"
            self.c.execute(query_pedido, (id_cliente, id_producto, cantidad, total))
            
            # Actualizar el inventario
            query_inventario = "UPDATE inventario SET cantidad = cantidad - ? WHERE ID_Producto = ?"
            self.c.execute(query_inventario, (cantidad, id_producto))
            
            # Confirmar la transacción
            self.conn.commit()
            messagebox.showinfo("Éxito", "Pedido creado y inventario actualizado exitosamente.")
        except sqlite3.Error as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al crear pedido: {e}")
   
   
    def treeview_sort_column(self, col):
        data_list = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # Intentar convertir a número para orden numérico
        try:
            data_list.sort(key=lambda t: float(t[0]), reverse=self.tree_sort_reverse[col])
        except ValueError:
            # Si falla, ordenar como cadena
            data_list.sort(key=lambda t: t[0], reverse=self.tree_sort_reverse[col])
        
        # Reorganizar los datos en el árbol
        for index, (val, item) in enumerate(data_list):
            self.tree.move(item, '', index)
        
        # Alternar el estado de orden
        self.tree_sort_reverse[col] = not self.tree_sort_reverse[col]
    
    def ocultar_tablas(self):
        if self.tablas_visibles:
            # Ocultar tablas
            self.tree_frame.pack_forget()  # Oculta el frame de la tabla
            self.tablas_visibles = False
            if self.tabla != "Clientes":
                self.master.geometry("800x600")  # Ajustar el tamaño de la ventana cuando las tablas están ocultas
        else:
            # Mostrar tablas
            self.tree_frame.pack(pady=20, fill='both', expand=True)
            self.tablas_visibles = True
            if self.tabla != "Clientes":
                self.adjust_window_size()  # Ajustar el tamaño de la ventana cuando las tablas están visibles
    
    
    def validar_datos(self, tabla, values, is_update=False):
        if tabla == 'Clientes':
            # Desempaquetar los valores
            id_cliente, nombre, primer_apellido, segundo_apellido, correo, \
            fecha_registro, calle, numero, id_comuna, telefono = values

            # Validar ID_Cliente (números, puntos, guiones y una letra)
            if not re.match(r'^[0-9.-]*[kK0-9]$', id_cliente):
                return "ID_Cliente debe contener solo números, puntos, guiones y una letra (k o K)."

            # Verificar unicidad de ID_Cliente
            if not is_update:
                # En inserción, verificar si ID_Cliente ya existe
                self.c.execute("SELECT COUNT(*) FROM Clientes WHERE ID_Cliente = ?", (id_cliente,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Cliente ya existe en la base de datos."
            else:
                # En actualización, verificar si el ID_Cliente ha cambiado
                if id_cliente != self.original_id_cliente:
                    # Si cambió, verificar si el nuevo ID_Cliente ya existe en otro registro
                    self.c.execute("SELECT COUNT(*) FROM Clientes WHERE ID_Cliente = ?", (id_cliente,))
                    if self.c.fetchone()[0] > 0:
                        return "ID_Cliente ya existe en la base de datos."
            
            # Validar Nombre, Primer_Apellido, Segundo_Apellido
            if not all(re.match(r'^[a-zA-Z\s]{1,50}$', campo) for campo in [nombre, primer_apellido, segundo_apellido]):
                return "Nombre, Primer Apellido y Segundo Apellido deben contener solo letras y espacios, y tener un máximo de 50 caracteres."

            # Validar Correo
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', correo):
                return "Correo debe ser un email válido y tener un máximo de 50 caracteres."

            # Validar Calle
            if not re.match(r'^[a-zA-Z0-9\s]{1,100}$', calle):
                return "Calle debe contener solo letras, números y espacios, y tener un máximo de 100 caracteres."

            # Validar Numero
            if not numero.isdigit():
                return "Numero debe ser un número entero."

            # Validar ID_Comuna
            if not id_comuna.isdigit():
                return "ID_Comuna debe ser un número entero."

            # Validar Telefono
            if not re.match(r'^9\d{8}$', telefono):
                return "Telefono debe ser un número válido de Chile con el formato +569********."

        elif tabla == 'Pedido':
            pass    

        elif tabla == 'Productos':
            # Desempaquetar los valores
            id_producto, nombre_producto, descripcion, precio = values

            # Validar ID_Producto (único y valor entero)
            if not id_producto.isdigit():
                return "ID_Producto debe ser un número entero."

            # Verificar unicidad de ID_Producto
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Productos WHERE ID_Producto = ?", (id_producto,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Producto ya existe en la base de datos."

            # Validar Precio (solo números)
            if not re.match(r'^\d+(\.\d{1,2})?$', precio):
                return "Precio debe ser un número válido."
        
        elif tabla == 'Metodo_Pago':
            # Desempaquetar los valores
            id_pagos, id_metodo_pago, nombre_metodo_pago = values

            # Validar ID_Pagos (único y valor entero)
            if not id_pagos.isdigit():
                return "ID_Pagos debe ser un número entero."

            # Verificar unicidad de ID_Pagos
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Metodo_Pago WHERE ID_Pagos = ?", (id_pagos,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Pagos ya existe en la base de datos."

            # Validar ID_Metodo_Pago (solo 901, 902, 903)
            if id_metodo_pago not in ["901", "902", "903"]:
                return "ID_Metodo_Pago debe ser uno de los valores 901, 902 o 903."

            # Validar Nombre_Metodo_Pago según ID_Metodo_Pago
            metodo_pago_dict = {
                "901": "CREDITO",
                "902": "EFECTIVO",
                "903": "DEBITO"
            }
            if nombre_metodo_pago != metodo_pago_dict[id_metodo_pago]:
                return f"Nombre_Metodo_Pago debe ser '{metodo_pago_dict[id_metodo_pago]}' para ID_Metodo_Pago {id_metodo_pago}."

        elif tabla == 'Estado_Pedido':
            # Desempaquetar los valores
            id_cliente, id_envios, nombre_estado_envio = values

            # Validar ID_Envios (único y valor entero)
            if not id_envios.isdigit():
                return "ID_Envios debe ser un número entero."

            # Verificar unicidad de ID_Envios
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Estado_Pedido WHERE ID_Envios = ?", (id_envios,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Envios ya existe en la base de datos."

        elif tabla == 'Categoria_Productos':
            # Desempaquetar los valores
            id_producto, id_categoria_producto, nombre_categoria = values

            # Validar ID_Producto (entero)
            if not id_producto.isdigit():
                return "ID_Producto debe ser un número entero."

            # Validar ID_Categoria_Producto (entero)
            if not id_categoria_producto.isdigit():
                return "ID_Categoria_Productos debe ser un número entero."

            # Validar Nombre_Categoria (solo opciones válidas)
            if nombre_categoria not in ["Stickers", "Pendones", "Etiquetas"]:
                return "Nombre_Categoria debe ser 'Stickers', 'Pendones' o 'Etiquetas'."

        elif tabla == 'Cliente_Producto':
            # Desempaquetar los valores
            id_cliente_producto, id_boleta_cliente_producto = values

            # Validar ID_Boleta_Cliente_Producto (único)
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Cliente_Producto WHERE ID_Boleta_Cliente_Producto = ?", (id_boleta_cliente_producto,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Boleta_Cliente_Producto ya existe en la base de datos."

        elif tabla == 'Comunas':
            # Desempaquetar los valores
            id_comuna, comuna = values

            # Validar ID_Comuna (único y entero)
            if not id_comuna.isdigit():
                return "ID_Comuna debe ser un número entero."
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Comunas WHERE ID_Comuna = ?", (id_comuna,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Comuna ya existe en la base de datos."

            # Validar Comuna (solo letras)
            if not re.match(r'^[a-zA-Z\s]+$', comuna):
                return "Comuna debe contener solo letras."

        elif tabla == 'Pago_Cliente':
            # Desempaquetar los valores
            id_producto, id_pagos, fecha_pago, monto_total = values

            # Validar ID_Producto (entero)
            if not id_producto.isdigit():
                return "ID_Producto debe ser un número entero."

            # Validar ID_Pagos (único y entero)
            if not id_pagos.isdigit():
                return "ID_Pagos debe ser un número entero."
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Pago_Cliente WHERE ID_Pagos = ?", (id_pagos,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Pagos ya existe en la base de datos."

            # Validar Monto_Total (solo números)
            if not re.match(r'^\d+(\.\d{1,2})?$', monto_total):
                return "Monto_Total debe ser un número válido."

        elif tabla == 'Region':
            # Desempaquetar los valores
            id_region, region = values

            # Validar ID_Region (único y entero)
            if not id_region.isdigit():
                return "ID_Region debe ser un número entero."
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Region WHERE ID_Region = ?", (id_region,))
                if self.c.fetchone()[0] > 0:
                    return "ID_Region ya existe en la base de datos."

            # Validar Region (único y solo letras)
            if not re.match(r'^[a-zA-Z\s]+$', region):
                return "Region debe contener solo letras."
            if not is_update:
                self.c.execute("SELECT COUNT(*) FROM Region WHERE Region = ?", (region,))
                if self.c.fetchone()[0] > 0:
                    return "Region ya existe en la base de datos."

        
        # Agrega más validaciones según sea necesario
        return None  # Retorna None si no hay errores
    
    def read_records(self):
        try:
            query = f"SELECT * FROM {self.tabla}"
            self.c.execute(query)
            all_records = self.c.fetchall()
            self.display_records(all_records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al leer registros de {self.tabla}: {e}")

    def display_records(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in records:
            self.tree.insert('', tk.END, values=row)

    def insertar_registro(self):
        current_values = []
        for col in self.columns:
            widget = self.form_entries[col]
            if isinstance(widget, DateEntry):
                date_value = widget.get_date().strftime('%Y-%m-%d')
                current_values.append(date_value)
            else:
                current_values.append(widget.get())
        
        # Imprimir los valores a insertar para depuración
        print("Valores a insertar en", self.tabla, ":", current_values)
    
        # Validar los datos
        error = self.validar_datos(self.tabla, current_values)
        if error:
            messagebox.showerror("Error de Validación", error, parent=self.master)
            return
    
        query = f"INSERT INTO {self.tabla} ({', '.join(self.columns)}) VALUES ({', '.join(['?'] * len(self.columns))})"
        try:
            self.c.execute(query, current_values)
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Registro insertado exitosamente en {self.tabla}.", parent=self.master)
            self.clear_entries()
            self.read_records()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al insertar el registro en {self.tabla}: {e}", parent=self.master)
            # Imprimir el error para depuración
            print("Error al insertar el registro:", e)
            
    def update_record(self):
        current_values = []
        for col in self.columns:
            widget = self.form_entries[col]
            if isinstance(widget, DateEntry):
                date_value = widget.get_date().strftime('%Y-%m-%d')
                current_values.append(date_value)
            else:
                current_values.append(widget.get())
    
        error = self.validar_datos(self.tabla, current_values, is_update=True)
        if error:
            messagebox.showerror("Error de Validación", error, parent=self.master)
            return
    
        try:
            set_clause = ", ".join(f"{col} = ?" for col in self.columns)
            query = f"UPDATE {self.tabla} SET {set_clause} WHERE {self.columns[0]} = ?"
            self.c.execute(query, current_values + [self.original_id_cliente])
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Registro actualizado exitosamente en {self.tabla}.", parent=self.master)
            self.clear_entries()
            self.read_records()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar el registro en {self.tabla}: {e}", parent=self.master)
    
    def delete_record(self):
        if not self.original_id_cliente:
            messagebox.showerror("Error", "Por favor, selecciona un registro para eliminar.", parent=self.master)
            return
    
        query = f"DELETE FROM {self.tabla} WHERE {self.columns[0]} = ?"
        try:
            self.c.execute(query, (self.original_id_cliente,))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Registro eliminado exitosamente en {self.tabla}", parent=self.master)
            self.clear_entries()
            self.read_records()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el registro: {e}", parent=self.master)
            
    def clear_entries(self):
        for entry in self.form_entries.values():
            entry.delete(0, tk.END)

    def update_query_tree(self):
        # Clear existing tree items
        for item in self.query_tree.get_children():
            self.query_tree.delete(item)
    
        # Fetch customers ordered by purchase count
        self.c.execute("""
            SELECT Clientes.*, COUNT(Pedido.ID_Pedido) as purchase_count
            FROM Clientes
            LEFT JOIN Pedido ON Clientes.ID_Cliente = Pedido.ID_Cliente
            GROUP BY Clientes.ID_Cliente
            ORDER BY purchase_count DESC
        """)
        customers = self.c.fetchall()
    
        for customer in customers:
            customer_id = customer[0]
            customer_name = f"{customer[1]} {customer[2]} (Compras: {customer[-1]})"
            customer_item = self.query_tree.insert('', 'end', text=customer_name, iid=customer_id)
    
            # Fetch and add customer's orders
            self.c.execute("SELECT * FROM Pedido WHERE ID_Cliente=?", (customer_id,))
            orders = self.c.fetchall()
            for order in orders:
                order_id = order[0]
                order_item = self.query_tree.insert(customer_item, 'end', text=f"Pedido ID: {order_id}", iid=order_id)
    
        self.query_tree.pack(side='left', fill='both', expand=True)
    
    def create_query_tree(self):
        # Frame for the query tree
        self.tree_frame = ctk.CTkFrame(self.master)
        self.tree_frame.pack(side='left', fill='both', expand=True)
    
        # Create Treeview
        self.query_tree = ttk.Treeview(self.tree_frame)
        self.query_tree.heading('#0', text='Clientes Más Frecuentes')
    
        # Build the tree dynamically
        self.update_query_tree()
    
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.original_id_cliente = values[0]
            for i, col in enumerate(self.columns):
                widget = self.form_entries[col]
                value = values[i]
                if isinstance(widget, DateEntry):
                    widget.set_date(datetime.strptime(value, '%Y-%m-%d'))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)
            
    def update_query_tree(self):
        # Clear existing tree items
        for item in self.query_tree.get_children():
            self.query_tree.delete(item)
    
        # Fetch customers ordered by purchase count
        self.c.execute("""
            SELECT Clientes.*, COUNT(Pedido.ID_Pedido) as purchase_count
            FROM Clientes
            LEFT JOIN Pedido ON Clientes.ID_Cliente = Pedido.ID_Cliente
            GROUP BY Clientes.ID_Cliente
            ORDER BY purchase_count DESC
        """)
        customers = self.c.fetchall()
    
        for customer in customers:
            customer_id = customer[0]
            customer_name = f"{customer[1]} {customer[2]} (Compras: {customer[-1]})"
            customer_item = self.query_tree.insert('', 'end', text=customer_name, iid=customer_id)
    
            # Fetch and add customer's orders
            self.c.execute("SELECT * FROM Pedido WHERE ID_Cliente=?", (customer_id,))
            orders = self.c.fetchall()
            for order in orders:
                order_id = order[0]
                order_item = self.query_tree.insert(customer_item, 'end', text=f"Pedido ID: {order_id}", iid=order_id)
    
        self.query_tree.pack(side='left', fill='both', expand=True)
    
    def create_display_options(self):
        # Frame for display options
        self.options_frame = ctk.CTkFrame(self.master)
        self.options_frame.pack(side='right', fill='y')

        # Checkboxes for selectable elements
        self.show_clients_var = tk.BooleanVar(value=True)
        self.show_orders_var = tk.BooleanVar(value=True)

        show_clients_cb = ctk.CTkCheckBox(self.options_frame, text="Mostrar Clientes", variable=self.show_clients_var, command=self.update_display)
        show_clients_cb.pack(pady=5)

        show_orders_cb = ctk.CTkCheckBox(self.options_frame, text="Mostrar Pedido", variable=self.show_orders_var, command=self.update_display)
        show_orders_cb.pack(pady=5)
    
    