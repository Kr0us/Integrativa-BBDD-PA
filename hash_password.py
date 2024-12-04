import sqlite3
import hashlib

def hash_existing_passwords():
    try:
        conn = sqlite3.connect('empresa.db')
        c = conn.cursor()

        # Obtener todos los usuarios
        c.execute("SELECT RUT, contraseña FROM usuarios")
        usuarios = c.fetchall()

        for rut, contrasenia in usuarios:
            # Verificar si la contraseña ya está hasheada (opcional)
            if len(contrasenia) != 64:  # SHA-256 produce un hash de 64 caracteres hexadecimales
                hashed_password = hashlib.sha256(contrasenia.encode()).hexdigest()
                # Actualizar la contraseña en la base de datos
                c.execute("UPDATE usuarios SET contraseña = ? WHERE RUT = ?", (hashed_password, rut))

        conn.commit()
        print("Contraseñas actualizadas a hashes correctamente.")
    except sqlite3.Error as e:
        print(f"Error al actualizar contraseñas: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    hash_existing_passwords()