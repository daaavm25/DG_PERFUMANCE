-- Inserción en tabla de roles
INSERT INTO gestion_perfumance.rol (descripcion) VALUES
('Gerente'),
('Empleado'),
('Cliente');

-- Inserción en tabla de  géneros
INSERT INTO gestion_perfumance.genero (descripcion) VALUES
('Hombre'),
('Mujer');

INSERT INTO gestion_perfumance.perfume
(marca, presentacion, talla, id_genero, stock, fecha_caducidad)
VALUES
('Coach Green', 'Eau de Parfum', '100ml', 3, 10, '2030-12-31'),
('Victoria Secret Bombshell', 'Eau de Parfum', '100ml', 2, 12, '2030-12-31'),
('Victoria Secret Champagne', 'Eau de Parfum', '100ml', 2, 8, '2030-12-31'),
('Montblanc Explorer', 'Eau de Parfum', '100ml', 1, 9, '2030-12-31'),
('Versace Eros', 'Eau de Toilette', '100ml', 1, 11, '2030-12-31'),
('Acqua di Giò', 'Eau de Toilette', '100ml', 1, 10, '2030-12-31'),
('Jean Paul Elixir', 'Eau de Parfum', '100ml', 1, 7, '2030-12-31'),
('Yves Saint Laurent Y', 'Eau de Parfum', '100ml', 1, 6, '2030-12-31');



 INSERT INTO gestion_perfumance.genero (descripcion)
VALUES
('Masculino'),
('Femenino'),
('Unisex');
