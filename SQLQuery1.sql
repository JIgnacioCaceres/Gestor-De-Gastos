CREATE DATABASE ControlDeGastos

--Crear la tabla Usuario
CREATE TABLE Usuarios(
	idUsuario INT IDENTITY(1,1) PRIMARY KEY,
	NombreUsuario NVARCHAR(50) NOT NULL UNIQUE,
	Contraseña NVARCHAR(100) NOT NULL,
	Divisa NVARCHAR(10) DEFAULT 'ARS',
	IngresosMensuales DECIMAL(10,2) DEFAULT 0
);

--Crear la tabla Gastos
CREATE TABLE Gastos(
	IdGasto INT IDENTITY(1,1) PRIMARY KEY,
	IdUsuario INT NOT NULL,
	Monto DECIMAL(10,2) NOT NULL,
	Categoria NVARCHAR(50) NOT NULL,
	Fecha DATE NOT NULL,
	Descripcion NVARCHAR(255),
	FOREIGN KEY (IdUsuario) REFERENCES Usuarios(IdUsuario)
);

