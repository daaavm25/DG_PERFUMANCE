-- Inserción en tabla de roles
INSERT INTO gestion_perfumance.rol (descripcion) VALUES
('Gerente'),
('Empleado'),
('Cliente');

-- Inserción en tabla de  empleados
INSERT INTO gestion_perfumance.empleado (nombres, apellidos, telefono, email, id_rol) VALUES
('Diego', 'Grimaldo Osorio', '5591007013', 'grimaldodiego380@gmail.com', 1);

-- Inserción en tabla de  usuarios 
INSERT INTO gestion_perfumance.usuario (username, password, email, id_rol, activo, id_cliente, id_empleado) VALUES
('Diego-Ghost', 'DummyPassword123', 'grimaldodiego380@gmail.com', 1, TRUE, NULL, 1);

-- Inserción en tabla de  géneros
INSERT INTO gestion_perfumance.genero (descripcion) VALUES
('Hombre'),
('Mujer');