import customtkinter as ctk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import sqlite3
from crud_window import *
from encargado import *
from admin import *
import hashlib
import os

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    global root
    root = ctk.CTk()
    root.title("Inicio de Sesión")
    root.geometry("600x750")
    root.resizable(False, False)

    global main_frame
    main_frame = ctk.CTkFrame(root)
    main_frame.place(relwidth=1, relheight=1)

    # Mostrar el menú principal
    mostrar_menu_principal()

    root.mainloop()
    
def login_admin():
    # Limpiar el frame principal
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Actualizar el título
    title_label = ctk.CTkLabel(
        main_frame,
        text="Administrador",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title_label.place(x=395, y=90, anchor="e")

    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fotos_dir = os.path.join(current_dir, "fotos")
    
    # Cargar la imagen principal
    image_path = os.path.join(fotos_dir, "Logo_RGB.png")
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label = ctk.CTkLabel(main_frame, image=photo, text="")
    label.image = photo
    label.place(x=200, y=130)
        
    # Etiquetas y campos de entrada
    username_label = ctk.CTkLabel(main_frame, text="Usuario", font=ctk.CTkFont(size=18))
    username_label.place(x=120, y=360, anchor="e")

    username_entry = ctk.CTkEntry(
        main_frame,
        placeholder_text="RUT",
        font=ctk.CTkFont(size=18),
        width=350
    )
    username_entry.place(x=150, y=350)

    password_label = ctk.CTkLabel(main_frame, text="Contraseña", font=ctk.CTkFont(size=18))
    password_label.place(x=125, y=415, anchor="e")

    password_entry = ctk.CTkEntry(
        main_frame,
        placeholder_text="**********",
        show="*",
        font=ctk.CTkFont(size=18),
        width=350
    )
    password_entry.place(x=150, y=400)
    
        # Botones
    login_button = ctk.CTkButton(
        main_frame,
        text="Iniciar Sesión",
        command=lambda: verificar_login_admin(username_entry, password_entry),
        font=ctk.CTkFont(size=18),
        width=200,
        height=50
    )
    login_button.place(x=50, y=500)

    volver_button = ctk.CTkButton(
        main_frame,
        text="Volver",
        command=mostrar_menu_principal,
        font=ctk.CTkFont(size=18),
        width=200,
        height=50
    )
    volver_button.place(x=350, y=500)

def login_encargado():
    # Limpiar el frame principal
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Actualizar el título
    title_label = ctk.CTkLabel(
        main_frame,
        text="Encargado",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title_label.place(x=380, y=90, anchor="e")

    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fotos_dir = os.path.join(current_dir, "fotos")
    
    # Cargar la imagen principal
    image_path = os.path.join(fotos_dir, "Logo_RGB.png")
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label = ctk.CTkLabel(main_frame, image=photo, text="")
    label.image = photo
    label.place(x=210, y=130)
        
    # Etiquetas y campos de entrada
    username_label = ctk.CTkLabel(main_frame, text="Usuario", font=ctk.CTkFont(size=18))
    username_label.place(x=120, y=360, anchor="e")

    username_entry = ctk.CTkEntry(
        main_frame,
        placeholder_text="RUT",
        font=ctk.CTkFont(size=18),
        width=350
    )
    username_entry.place(x=150, y=350)

    password_label = ctk.CTkLabel(main_frame, text="Contraseña", font=ctk.CTkFont(size=18))
    password_label.place(x=125, y=415, anchor="e")

    password_entry = ctk.CTkEntry(
        main_frame,
        placeholder_text="**********",
        show="*",
        font=ctk.CTkFont(size=18),
        width=350
    )
    password_entry.place(x=150, y=400)

    # Botones
    login_button = ctk.CTkButton(
        main_frame,
        text="Iniciar Sesión",
        command=lambda: verificar_login_encargado(username_entry, password_entry),
        font=ctk.CTkFont(size=18),
        width=200,
        height=50
    )
    login_button.place(x=50, y=500)

    volver_button = ctk.CTkButton(
        main_frame,
        text="Volver",
        command=mostrar_menu_principal,
        font=ctk.CTkFont(size=18),
        width=200,
        height=50
    )
    volver_button.place(x=350, y=500)      
    
def mostrar_menu_principal():
    # Limpiar el frame principal
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fotos_dir = os.path.join(current_dir, "fotos")

    # Cargar la imagen principal
    image_path = os.path.join(fotos_dir, "Logo_RGB.png")
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Mostrar la imagen principal
    image_label = ctk.CTkLabel(main_frame, image=photo, text="")
    image_label.image = photo
    image_label.pack(pady=10)

    title_label = ctk.CTkLabel(
        main_frame,
        text="Seleccionar tipo de usuario:",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    title_label.pack(pady=10)

    # Cargar imágenes para los botones
    img_encargado_path = os.path.join(fotos_dir, "login_encargado.png")
    img_encargado = ctk.CTkImage(
        Image.open(img_encargado_path),
        size=(200, 200)
    )
    img_admin_path = os.path.join(fotos_dir, "login_admin.png")
    img_admin = ctk.CTkImage(
        Image.open(img_admin_path),
        size=(200, 200)
    )

    #Label de encargado
    label_encargado = ctk.CTkLabel(
        main_frame,
        text="Encargado",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    label_encargado.place(x=410, y=510)
    
    # Botón de Login Encargado
    ctk.CTkButton(
        main_frame,
        image=img_encargado,
        text="",
        command=login_encargado
    ).place(x=350, y=300)

    #Label de admin
    label_admin = ctk.CTkLabel(
        main_frame,
        text="Admin",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    label_admin.place(x=130, y=510)
    
    # Botón de Login Admin
    ctk.CTkButton(
        main_frame,
        image=img_admin,
        text="",
        command=login_admin
    ).place(x=50, y=300)

def verificar_login_encargado(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Verify credentials with hashed password
    try:
        conn = sqlite3.connect('empresa.db')
        c = conn.cursor()
        c.execute("SELECT nombre, role FROM usuarios WHERE RUT = ? AND contraseña = ?", (username, hashed_password))
        result = c.fetchone()

        if result:
            nombre_usuario, role = result
            if role == "Encargado":
                messagebox.showinfo("Login exitoso", f"Bienvenido, {nombre_usuario}")
                root.destroy()
                root2 = ThemedTk(theme="radiance")
                app = EncargadoApp(root2)
                root2.mainloop()
            else:
                messagebox.showerror("Login fallido", "No tienes permisos de Encargado")
        else:
            messagebox.showerror("Login fallido", "Usuario o contraseña incorrectos")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
    finally:
        conn.close()


def verificar_login_admin(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Verify credentials with hashed password
    print(f"Intentando iniciar sesión con RUT: {username} y Contraseña: {password}")  # Mensaje de depuración

    try:
        conn = sqlite3.connect('empresa.db')
        c = conn.cursor()
        c.execute("SELECT nombre, role FROM usuarios WHERE RUT = ? AND contraseña = ?", (username, hashed_password))
        result = c.fetchone()

        print(f"Resultado de la consulta: {result}")  # Mensaje de depuración

        if result:
            nombre_usuario, role = result
            if role == "Admin":
                messagebox.showinfo("Login exitoso", f"Bienvenido, {nombre_usuario}")
                root.destroy()
                root2 = ThemedTk(theme="radiance")
                app = AdminApp(root2)
                root2.mainloop()
            else:
                messagebox.showerror("Login fallido", "No tienes permisos de Admin")
        else:
            messagebox.showerror("Login fallido", "Usuario o contraseña incorrectos")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
        print(f"Error al conectar con la base de datos: {e}")  # Mensaje de depuración
    finally:
        if conn:
            conn.close()
            print("Conexión a la base de datos cerrada")  # Mensaje de depuración

if __name__ == "__main__":
    main()