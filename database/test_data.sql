-- Inserción en tabla de roles
INSERT INTO gestion_perfumance.rol (descripcion) VALUES
('Gerente'),
('Empleado'),
('Cliente');

-- Inserción en tabla de  géneros
INSERT INTO gestion_perfumance.genero (descripcion) VALUES
('Hombre'),
('Mujer'),
('Unisex');

INSERT INTO gestion_perfumance.perfume
(marca, presentacion, talla, id_genero, stock, fecha_caducidad, precio)VALUES
('Scandal', 'Eau de Parfum', '100ml', 2, 10, '2030-12-31', 3320),
('D&G Light Blue', 'Eau de Parfum', '100ml', 2, 12, '2030-12-31', 3350),
('Miss Dior', 'Eau de Parfum', '100ml', 2, 8, '2030-12-31', 2400),
('Coach for Men', 'Eau de Parfum', '100ml', 1, 9, '2030-12-31', 3290),
('Versace Eros', 'Eau de Toilette', '100ml', 1, 11, '2030-12-31', 4300),
('Acqua di Giò', 'Eau de Toilette', '100ml', 1, 10, '2030-12-31', 2469),
('Valentino Uomo', 'Eau de Parfum', '100ml', 1, 7, '2030-12-31', 2548),
('Dior Sauvage', 'Eau de Parfum', '100ml', 1, 6, '2030-12-31', 5900);
