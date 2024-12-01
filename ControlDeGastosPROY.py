import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import conexion_sql
import requests


class Usuario:
    def __init__(self, usuario_id, nombre_usuario, contrasena, divisa="ARS"):
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.divisa = divisa


class Aplicacion:
    def __init__(self):
        self.usuario_actual = None
        self.root = tk.Tk()
        self.root.title("Control de Gastos")
        self.crear_interfaz_inicio()

    def crear_interfaz_inicio(self):
        self.limpiar_interfaz()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Control de Gastos", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="Registrarse", width=20, command=self.registrar).grid(row=1, column=0, pady=10)
        tk.Button(frame, text="Iniciar Sesión", width=20, command=self.iniciar_sesion).grid(row=1, column=1, pady=10)
        tk.Button(frame, text="Salir", width=20, command=self.root.quit).grid(row=2, column=0, columnspan=2, pady=20)

    def limpiar_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def registrar(self):
        self.limpiar_interfaz()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Registro de Usuario", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text="Nombre de Usuario:").grid(row=1, column=0, pady=5)
        nombre_usuario = tk.Entry(frame)
        nombre_usuario.grid(row=1, column=1)

        tk.Label(frame, text="Contraseña:").grid(row=2, column=0, pady=5)
        contrasena = tk.Entry(frame, show="*")
        contrasena.grid(row=2, column=1)

        tk.Label(frame, text="Correo Electrónico:").grid(row=3, column=0, pady=5)
        email = tk.Entry(frame)
        email.grid(row=3, column=1)

        def guardar_usuario():
            if not nombre_usuario.get() or not contrasena.get() or not email.get():
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                conexion = conexion_sql.conectar()
                if conexion is None:
                    return

                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM Usuarios WHERE Nombre = ?", (nombre_usuario.get(),))
                if cursor.fetchone():
                    messagebox.showerror("Error", "El usuario ya existe.")
                    return

                cursor.execute("INSERT INTO Usuarios (Nombre, Email) VALUES (?, ?)", (nombre_usuario.get(), email.get()))
                conexion.commit()
                cursor.execute("SELECT @@IDENTITY")
                usuario_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO Contrasenas (UsuarioID, Contrasena) VALUES (?, ?)", (usuario_id, contrasena.get()))
                conexion.commit()

                messagebox.showinfo("Éxito", f"Usuario {nombre_usuario.get()} registrado exitosamente.")
                self.crear_interfaz_inicio()
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar: {e}")
            finally:
                if conexion:
                    conexion.close()

        tk.Button(frame, text="Guardar", command=guardar_usuario).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Volver", command=self.crear_interfaz_inicio).grid(row=5, column=0, columnspan=2, pady=10)

    def iniciar_sesion(self):
        self.limpiar_interfaz()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Inicio de Sesión", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text="Nombre de Usuario:").grid(row=1, column=0, pady=5)
        nombre_usuario = tk.Entry(frame)
        nombre_usuario.grid(row=1, column=1)

        tk.Label(frame, text="Contraseña:").grid(row=2, column=0, pady=5)
        contrasena = tk.Entry(frame, show="*")
        contrasena.grid(row=2, column=1)

        def verificar_usuario():
            if not nombre_usuario.get() or not contrasena.get():
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                conexion = conexion_sql.conectar()
                if conexion is None:
                    return

                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT u.UsuarioID, u.Nombre
                    FROM Usuarios u
                    INNER JOIN Contrasenas c ON u.UsuarioID = c.UsuarioID
                    WHERE u.Nombre = ? AND c.Contrasena = ?
                """, (nombre_usuario.get(), contrasena.get()))
                resultado = cursor.fetchone()

                if resultado:
                    usuario_id, nombre = resultado
                    self.usuario_actual = Usuario(usuario_id, nombre, contrasena.get())
                    self.mostrar_menu_principal()
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
            finally:
                if conexion:
                    conexion.close()

        tk.Button(frame, text="Ingresar", command=verificar_usuario).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Volver", command=self.crear_interfaz_inicio).grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_menu_principal(self):
        self.limpiar_interfaz()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text=f"Bienvenido, {self.usuario_actual.nombre_usuario}", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Agregar Gasto", width=20, command=self.agregar_gasto).grid(row=1, column=0, pady=5)
        tk.Button(frame, text="Ver Gastos", width=20, command=self.ver_gastos).grid(row=1, column=1, pady=5)
        tk.Button(frame, text="Estadísticas", width=20, command=self.ver_estadisticas).grid(row=2, column=0, pady=5)
        tk.Button(frame, text="Elegir Divisa", width=20, command=self.elegir_divisa).grid(row=2, column=1, pady=5)
        tk.Button(frame, text="Modificar Usuario", width=20, command=self.modificar_usuario).grid(row=3, column=0, pady=5)
        tk.Button(frame, text="Cerrar Sesión", width=20, command=self.cerrar_sesion).grid(row=3, column=1, pady=5)

    def agregar_gasto(self):
        monto = simpledialog.askfloat("Agregar Gasto", "Ingrese el monto del gasto:")
        descripcion = simpledialog.askstring("Agregar Gasto", "Ingrese una descripción del gasto:")
        if not monto or not descripcion:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return
        try:
            conexion = conexion_sql.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO GastosXUsuario (UsuarioID, Monto, Descripcion) VALUES (?, ?, ?)",
                (self.usuario_actual.usuario_id, monto, descripcion)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Gasto agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el gasto: {e}")
        finally:
            if conexion:
                conexion.close()

    def ver_gastos(self):
        try:
            conexion = conexion_sql.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT Monto, Descripcion FROM GastosXUsuario WHERE UsuarioID = ?", (self.usuario_actual.usuario_id,))
            gastos = cursor.fetchall()
            if gastos:
                listado = "\n".join([f"${monto:.2f} - {descripcion}" for monto, descripcion in gastos])
                messagebox.showinfo("Gastos", listado)
            else:
                messagebox.showinfo("Gastos", "No se encontraron gastos registrados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recuperar los gastos: {e}")
        finally:
            if conexion:
                conexion.close()

    def ver_estadisticas(self):
        try:
            conexion = conexion_sql.conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT SUM(Monto), AVG(Monto), COUNT(*) 
                FROM GastosXUsuario
                WHERE UsuarioID = ?
            """, (self.usuario_actual.usuario_id,))
            resultado = cursor.fetchone()
            if resultado:
                total, promedio, cantidad = resultado
                estadisticas = f"Total de gastos: ${total:.2f}\nPromedio por gasto: ${promedio:.2f}\nCantidad de gastos: {cantidad}"
                messagebox.showinfo("Estadísticas", estadisticas)
            else:
                messagebox.showinfo("Estadísticas", "No se encontraron gastos registrados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener las estadísticas: {e}")
        finally:
            if conexion:
                conexion.close()

    def modificar_usuario(self):
        self.limpiar_interfaz()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Modificar Datos del Usuario", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Nombre de Usuario:").grid(row=1, column=0, pady=5)
        nombre_usuario = tk.Entry(frame)
        nombre_usuario.grid(row=1, column=1)
        nombre_usuario.insert(0, self.usuario_actual.nombre_usuario)

        tk.Label(frame, text="Contraseña:").grid(row=2, column=0, pady=5)
        contrasena = tk.Entry(frame, show="*")
        contrasena.grid(row=2, column=1)

        tk.Label(frame, text="Correo Electrónico:").grid(row=3, column=0, pady=5)
        email = tk.Entry(frame)
        email.grid(row=3, column=1)

        def guardar_modificaciones():
            if not nombre_usuario.get() or not contrasena.get() or not email.get():
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                conexion = conexion_sql.conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE Usuarios 
                    SET Nombre = ?, Email = ?
                    WHERE UsuarioID = ?
                """, (nombre_usuario.get(), email.get(), self.usuario_actual.usuario_id))
                conexion.commit()
                cursor.execute("""
                    UPDATE Contrasenas
                    SET Contrasena = ?
                    WHERE UsuarioID = ?
                """, (contrasena.get(), self.usuario_actual.usuario_id))
                conexion.commit()

                self.usuario_actual.nombre_usuario = nombre_usuario.get()
                messagebox.showinfo("Éxito", "Datos de usuario modificados correctamente.")
                self.mostrar_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar usuario: {e}")
            finally:
                if conexion:
                    conexion.close()

        tk.Button(frame, text="Guardar Cambios", command=guardar_modificaciones).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Volver", command=self.mostrar_menu_principal).grid(row=5, column=0, columnspan=2, pady=10)

    def elegir_divisa(self):
        self.limpiar_interfaz()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Seleccione su divisa", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        divisas = ["ARS", "USD", "EUR", "BRL", "JPY"]
        divisa_seleccionada = tk.StringVar(value=self.usuario_actual.divisa)

        tk.Label(frame, text="Divisa:").grid(row=1, column=0, pady=5)
        combo_divisas = ttk.Combobox(frame, textvariable=divisa_seleccionada, values=divisas, state="readonly")
        combo_divisas.grid(row=1, column=1, pady=5)

        def guardar_divisa():
            self.usuario_actual.divisa = divisa_seleccionada.get()
            messagebox.showinfo("Éxito", f"Divisa cambiada a {self.usuario_actual.divisa}.")
            self.mostrar_menu_principal()

        tk.Button(frame, text="Elegir Divisa", width=20, command=guardar_divisa).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Volver", width=20, command=self.mostrar_menu_principal).grid(row=3, column=0, columnspan=2, pady=5)

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.crear_interfaz_inicio()

    def iniciar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Aplicacion()
    app.iniciar()
