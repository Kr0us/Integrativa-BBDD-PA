import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from crud_window import *
import main
import os

class EncargadoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Casa de la Impresión - Encargado")
        self.master.geometry("550x600")# Ajustar el tamaño de la ventana
        self.sort_orders = {}
        self.conn = None
        self.c = None
        self.connect_to_db()
        self.tablas_visibles = False
        self.create_widgets()

        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
    def connect_to_db(self):
        try:
            self.conn = sqlite3.connect('empresa.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}\nDetails: {e.args}")

    def close_db_connection(self):
        if self.conn:
            self.conn.close()

    def create_widgets(self):
        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fotos_dir = os.path.join(current_dir, "fotos")
        
        # Cargar imágenes usando rutas relativas
        img_categoria_producto = Image.open(os.path.join(fotos_dir, "imagen_categoria_producto.png"))
        img_categoria_producto = img_categoria_producto.resize((50, 50), Image.LANCZOS)
        photo_categoria_producto = ImageTk.PhotoImage(img_categoria_producto)

        img_clientes = Image.open(os.path.join(fotos_dir, "imagen_clientes.png"))
        img_clientes = img_clientes.resize((50, 50), Image.LANCZOS)
        photo_clientes = ImageTk.PhotoImage(img_clientes)

        img_comuna_region = Image.open(os.path.join(fotos_dir, "imagen_comuna_region.png"))
        img_comuna_region = img_comuna_region.resize((50, 50), Image.LANCZOS)
        photo_comuna_region = ImageTk.PhotoImage(img_comuna_region)

        img_estado_pedido = Image.open(os.path.join(fotos_dir, "imagen_estado_pedido.png"))
        img_estado_pedido = img_estado_pedido.resize((50, 50), Image.LANCZOS)
        photo_estado_pedido = ImageTk.PhotoImage(img_estado_pedido)

        img_metodo_pago = Image.open(os.path.join(fotos_dir, "imagen_metodo_pago.png"))
        img_metodo_pago = img_metodo_pago.resize((50, 50), Image.LANCZOS)
        photo_metodo_pago = ImageTk.PhotoImage(img_metodo_pago)

        img_cliente_producto = Image.open(os.path.join(fotos_dir, "imagen_cliente_producto.png"))
        img_cliente_producto = img_cliente_producto.resize((50, 50), Image.LANCZOS)
        photo_cliente_producto = ImageTk.PhotoImage(img_cliente_producto)

        img_pago_cliente = Image.open(os.path.join(fotos_dir, "imagen_pago_cliente.png"))
        img_pago_cliente = img_pago_cliente.resize((50, 50), Image.LANCZOS)
        photo_pago_cliente = ImageTk.PhotoImage(img_pago_cliente)

        img_pedidos = Image.open(os.path.join(fotos_dir, "imagen_pedidos.png"))
        img_pedidos = img_pedidos.resize((50, 50), Image.LANCZOS)
        photo_pedidos = ImageTk.PhotoImage(img_pedidos)

        img_productos = Image.open(os.path.join(fotos_dir, "imagen_productos.png"))
        img_productos = img_productos.resize((50, 50), Image.LANCZOS)
        photo_productos = ImageTk.PhotoImage(img_productos)

        img_usuarios = Image.open(os.path.join(fotos_dir, "imagen_usuarios.png"))
        img_usuarios = img_usuarios.resize((50, 50), Image.LANCZOS)
        photo_usuarios = ImageTk.PhotoImage(img_usuarios)

        # Crear botones individualmente y posicionarlos con .place()
        boton_categoria_producto = ctk.CTkButton(
            self.master,
            text="Categoria_Productos",
            image=photo_categoria_producto,
            compound="left",
            command=self.mostrar_restriccion,
            width=120,
            height=52
        )
        boton_categoria_producto.place(x=300, y=150)

        boton_clientes = ctk.CTkButton(
            self.master,
            text="Clientes",
            image=photo_clientes,
            compound="left",
            command=lambda: self.abrir_crud("Clientes"),
            width=120,
            height=32
        )
        boton_clientes.place(x=300, y=220)

        boton_comuna_region = ctk.CTkButton(
            self.master,
            text="Region",
            image=photo_comuna_region,
            compound="left",
            command=lambda: self.abrir_crud("Region"),
            width=120,
            height=32
        )
        boton_comuna_region.place(x=300, y=290)

        boton_estado_pedido = ctk.CTkButton(
            self.master,
            text="Estado_Pedido",
            image=photo_estado_pedido,
            compound="left",
            command=lambda: self.abrir_crud("Estado_Pedido"),
            width=120,
            height=32
        )
        boton_estado_pedido.place(x=300, y=360)

        boton_metodo_pago = ctk.CTkButton(
            self.master,
            text="Metodo_Pago",
            image=photo_metodo_pago,
            compound="left",
            command=self.mostrar_restriccion,
            width=120,
            height=32
        )
        boton_metodo_pago.place(x=300, y=430)

        boton_cliente_producto = ctk.CTkButton(
            self.master,
            text="Cliente_Producto",
            image=photo_cliente_producto,
            compound="left",
            command=self.mostrar_restriccion,
            width=120,
            height=32
        )
        boton_cliente_producto.place(x=80, y=150)

        boton_pago_cliente = ctk.CTkButton(
            self.master,
            text="Pago_Cliente",
            image=photo_pago_cliente,
            compound="left",
            command=lambda: self.abrir_crud("Pago_Cliente"),
            width=120,
            height=32
        )
        boton_pago_cliente.place(x=80, y=220)

        boton_pedidos = ctk.CTkButton(
            self.master,
            text="Pedido",
            image=photo_pedidos,
            compound="left",
            command=lambda: self.abrir_crud("Pedido"),
            width=120,
            height=32
        )
        boton_pedidos.place(x=80, y=290)

        boton_productos = ctk.CTkButton(
            self.master,
            text="Productos",
            image=photo_productos,
            compound="left",
            command=lambda: self.abrir_crud("Productos"),
            width=120,
            height=32
        )
        boton_productos.place(x=80, y=360)

        boton_usuarios = ctk.CTkButton(
            self.master,
            text="usuarios",
            image=photo_usuarios,
            compound="left",
            command=self.mostrar_restriccion,
            width=120,
            height=32
        )
        boton_usuarios.place(x=80, y=430)
        
        # Botón de Cerrar Sesión
        logout_button = ctk.CTkButton(
            self.master,
            text="Cerrar Sesión",
            command=self.logout,
            width=120,
            height=32
        )
        logout_button.place(x=400, y=20)  # Ajusta la posición según tu interfaz

    def mostrar_restriccion(self):
        messagebox.showwarning("Acceso Denegado", "Solo permitido para admins.")
    
    def abrir_crud(self, tabla):
        new_window = tk.Toplevel(self.master)
        CRUDWindow(new_window, tabla)
            
    def logout(self):
        self.master.destroy()
        main.main()

    