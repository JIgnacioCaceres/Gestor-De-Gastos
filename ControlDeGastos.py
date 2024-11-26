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
        self.usuarios = []  
        self.usuario_actual = None

    def registrar(self):
        print("\n* Crear Usuario *")
        nombre_usuario = input("Nombre de usuario: ")
        contrasena = input("Contraseña: ")

        # Verificar si el usuario ya existe
        if nombre_usuario in [u.nombre_usuario for u in self.usuarios]:
            print("El usuario ya existe.")
            return

        # Crear y agregar un nuevo usuario
        nuevo_usuario = Usuario(nombre_usuario, contrasena)
        self.usuarios.append(nuevo_usuario)
        print(f"Usuario {nombre_usuario} registrado exitosamente.")

    def iniciar_sesion(self):
        print("\n* Iniciar Sesión *")
        nombre_usuario = input("Nombre de usuario: ")
        contrasena = input("Contraseña: ")

        # Buscar al usuario
        usuario = next((u for u in self.usuarios if u.nombre_usuario == nombre_usuario and u.contrasena == contrasena), None)

        if usuario:
            self.usuario_actual = usuario
            print(f"Bienvenido, {nombre_usuario}!")
        else:
            print("Usuario o contraseña incorrectos.")

    def elegir_divisa(self):
        if not self.usuario_actual:
            print("Debes iniciar sesión primero.")
            return

        print("\n* Elige una divisa *")
        print("1. USD\n2. EUR\n3. ARS\n4. BRL")
        opcion = input("Selecciona una opción: ")
        divisas = {"1": "USD", "2": "EUR", "3": "ARS", "4": "BRL"}
        self.usuario_actual.divisa = divisas.get(opcion, "USD")
        print(f"Divisa seleccionada: {self.usuario_actual.divisa}")

    def ingresar_ingresos_mensuales(self):
        if not self.usuario_actual:
            print("Debes iniciar sesión primero.")
            return

        print("\n* Ingresa tus ingresos mensuales *")
        try:
            ingresos = float(input("Monto mensual: "))
            self.usuario_actual.ingresos_mensuales = ingresos
            print(f"Ingresaste {ingresos} {self.usuario_actual.divisa} como tus ingresos mensuales.")
        except ValueError:
            print("Monto inválido.")

    def añadir_gasto(self):
        if not self.usuario_actual:
            print("Debes iniciar sesión primero.")
            return

        print("\n* Añadir Gasto *")
        try:
            monto = float(input("Monto del gasto: "))
            categoria = input("Categoría (ejemplo: Alimentación, Transporte): ")
            fecha = input("Fecha (DD-MM-YYYY): ")
            descripcion = input("Descripción del gasto: ")

            nuevo_gasto = Gasto(monto, categoria, fecha, descripcion)
            self.usuario_actual.gastos.append(nuevo_gasto)
            print("¡Gasto añadido exitosamente!")
        except ValueError:
            print("Monto inválido.")

    def ver_estadisticas(self):
        if not self.usuario_actual:
            print("Debe iniciar sesión primero.")
            return

        if not self.usuario_actual.gastos:
            print("No hay gastos registrados.")
            return

        print("\n* Estadísticas Mensuales *")
        total_gastos = sum(g.monto for g in self.usuario_actual.gastos)

        print(f"Total de gastos: {total_gastos:.2f} {self.usuario_actual.divisa}")
        print(f"Total de ingresos: {self.usuario_actual.ingresos_mensuales:.2f} {self.usuario_actual.divisa}")
        print("\nDistribución por categoría:")

        categorias = {}
        for gasto in self.usuario_actual.gastos:
            categorias[gasto.categoria] = categorias.get(gasto.categoria, 0) + gasto.monto

        for categoria, total in categorias.items():
            porcentaje = (total / total_gastos) * 100
            print(f"- {categoria}: {total:.2f} {self.usuario_actual.divisa} ({porcentaje:.2f}%)")

    def menu(self):
        while True:
            print("\n--- Menú Principal ---")
            print("[1] Registrarse")
            print("[2] Iniciar Sesión")
            print("[3] Elegir Divisa")
            print("[4] Ingresar Ingresos Mensuales")
            print("[5] Añadir Gasto")
            print("[6] Ver Estadísticas")
            print("[7] Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.registrar()
            elif opcion == "2":
                self.iniciar_sesion()
            elif opcion == "3":
                self.elegir_divisa()
            elif opcion == "4":
                self.ingresar_ingresos_mensuales()
            elif opcion == "5":
                self.añadir_gasto()
            elif opcion == "6":
                self.ver_estadisticas()
            elif opcion == "7":
                print("\u00a1Hasta luego!")
                break
            else:
                print("Opción inválida, Intente nuevamente.")

app = Aplicacion()
app.menu()