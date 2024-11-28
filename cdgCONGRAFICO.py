import tkinter as tk
from tkinter import messagebox, simpledialog
import conexion_sql

class Usuario:
    def __init__(self, nombre_usuario, contrasena):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.divisa = "ARS"
        self.ingresos_mensuales = 0
        self.gastos = []  

class Gasto:
    def __init__(self, monto, categoria, fecha, descripcion):
        self.monto = monto
        self.categoria = categoria
        self.fecha = fecha
        self.descripcion = descripcion

class Aplicacion:
    def __init__(self):
        self.usuario_actual = None
        self.root = tk.Tk()
        self.root.title("Control de Gastos")
        self.crear_interfaz()

    def crear_interfaz(self):
        # Menú principal
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Control de Gastos", font=("Arial", 16)).grid(row=0, column=0, columnspan=2)

        tk.Button(frame, text="Registrarse", width=20, command=self.registrar).grid(row=1, column=0, pady=10)
        tk.Button(frame, text="Iniciar Sesión", width=20, command=self.iniciar_sesion).grid(row=1, column=1, pady=10)
        tk.Button(frame, text="Elegir Divisa", width=20, command=self.elegir_divisa).grid(row=2, column=0, pady=10)
        tk.Button(frame, text="Ingresar Ingresos", width=20, command=self.ingresar_ingresos_mensuales).grid(row=2, column=1, pady=10)
        tk.Button(frame, text="Añadir Gasto", width=20, command=self.añadir_gasto).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Ver Estadísticas", width=20, command=self.ver_estadisticas).grid(row=3, column=1, pady=10)
        tk.Button(frame, text="Salir", width=20, command=self.root.quit).grid(row=4, column=0, columnspan=2, pady=20)

    def registrar(self):
        nombre_usuario = simpledialog.askstring("Registro", "Nombre de usuario:")
        if not nombre_usuario:
            return
        contrasena = simpledialog.askstring("Registro", "Contraseña:", show="*")
        if not contrasena:
            return
        email = simpledialog.askstring("Registro", "Correo electrónico:")
        if not email:
            return

        try:
            conexion = conexion_sql.conectar()
            if conexion is None:
                return

            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE Nombre = ?", (nombre_usuario,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El usuario ya existe.")
                return

            cursor.execute("INSERT INTO Usuarios (Nombre, Email) VALUES (?, ?)", (nombre_usuario, email))
            conexion.commit()
            cursor.execute("SELECT @@IDENTITY")
            usuario_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO Contrasenas (UsuarioID, Contrasena) VALUES (?, ?)", (usuario_id, contrasena))
            conexion.commit()

            messagebox.showinfo("Éxito", f"Usuario {nombre_usuario} registrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {e}")
        finally:
            if conexion:
                conexion.close()

    def iniciar_sesion(self):
        nombre_usuario = simpledialog.askstring("Inicio de Sesión", "Nombre de usuario:")
        if not nombre_usuario:
            return
        contrasena = simpledialog.askstring("Inicio de Sesión", "Contraseña:", show="*")
        if not contrasena:
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
            """, (nombre_usuario, contrasena))
            resultado = cursor.fetchone()

            if resultado:
                usuario_id, nombre = resultado
                self.usuario_actual = Usuario(nombre_usuario, contrasena)
                messagebox.showinfo("Bienvenido", f"¡Bienvenido, {nombre}!")
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        finally:
            if conexion:
                conexion.close()

    def elegir_divisa(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión primero.")
            return

        divisas = {"USD": "Dólar", "EUR": "Euro", "ARS": "Peso Argentino", "BRL": "Real"}
        opcion = simpledialog.askstring("Divisa", "Elige una divisa (USD, EUR, ARS, BRL):")
        if opcion in divisas:
            self.usuario_actual.divisa = opcion
            messagebox.showinfo("Éxito", f"Divisa seleccionada: {divisas[opcion]}")
        else:
            messagebox.showerror("Error", "Divisa no válida.")

    def ingresar_ingresos_mensuales(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión primero.")
            return

        try:
            ingresos = float(simpledialog.askstring("Ingresos", "Ingresa tus ingresos mensuales:"))
            self.usuario_actual.ingresos_mensuales = ingresos
            messagebox.showinfo("Éxito", f"Ingresaste {ingresos} {self.usuario_actual.divisa} como ingresos mensuales.")
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.")

    def añadir_gasto(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión primero.")
            return

        try:
            monto = float(simpledialog.askstring("Gasto", "Monto del gasto:"))
            categoria = simpledialog.askstring("Gasto", "Categoría del gasto:")
            fecha = simpledialog.askstring("Gasto", "Fecha del gasto (DD-MM-YYYY):")
            descripcion = simpledialog.askstring("Gasto", "Descripción del gasto:")

            nuevo_gasto = Gasto(monto, categoria, fecha, descripcion)
            self.usuario_actual.gastos.append(nuevo_gasto)
            messagebox.showinfo("Éxito", "¡Gasto añadido exitosamente!")
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.")

    def ver_estadisticas(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión primero.")
            return

        if not self.usuario_actual.gastos:
            messagebox.showinfo("Estadísticas", "No hay gastos registrados.")
            return

        total_gastos = sum(g.monto for g in self.usuario_actual.gastos)
        categorias = {}
        for gasto in self.usuario_actual.gastos:
            categorias[gasto.categoria] = categorias.get(gasto.categoria, 0) + gasto.monto

        estadisticas = f"Total de gastos: {total_gastos:.2f} {self.usuario_actual.divisa}\n"
        estadisticas += f"Total de ingresos: {self.usuario_actual.ingresos_mensuales:.2f} {self.usuario_actual.divisa}\n\n"
        estadisticas += "Distribución por categoría:\n"
        for categoria, total in categorias.items():
            porcentaje = (total / total_gastos) * 100
            estadisticas += f"- {categoria}: {total:.2f} ({porcentaje:.2f}%)\n"

        messagebox.showinfo("Estadísticas", estadisticas)

    def ejecutar(self):
        self.root.mainloop()

# Iniciar la aplicación
app = Aplicacion()
app.ejecutar()
