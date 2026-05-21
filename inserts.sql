USE Projeto;
GO

-- =========================
-- CLIENTES
-- =========================
INSERT INTO Cliente (tipo_cliente, telefone, NIF, morada, codigo_postal, localidade, nome)
VALUES
('Particular', '912345678', '123456789', 'Rua das Flores 10', '4700-100', 'Braga', 'João Silva'),
('Empresa', '913456789', '987654321', 'Avenida Central 50', '4000-200', 'Porto', 'Eventos XPTO Lda'),
('Particular', '914567890', '456789123', 'Rua do Sol 22', '3000-150', 'Coimbra', 'Maria Costa'),
('Empresa', '915678901', '321654987', 'Rua Industrial 9', '4710-250', 'Braga', 'Tech Solutions'),
('Particular', '916789012', '741852963', 'Rua Nova 15', '4800-300', 'Guimarães', 'Pedro Fernandes'),
('Particular', '917890123', '159357486', 'Rua Verde 2', '4900-500', 'Viana do Castelo', 'Inês Ribeiro'),
('Empresa', '918901234', '258369147', 'Zona Empresarial', '3800-120', 'Aveiro', 'Atlantic Corp'),
('Particular', '919012345', '951753852', 'Rua do Monte 90', '5000-200', 'Vila Real', 'Rita Lopes');

-- =========================
-- TIPOS DE EVENTO
-- =========================
INSERT INTO Tipo_evento (descricao)
VALUES
('Casamento'),
('Batizado'),
('Evento Empresarial'),
('Aniversário'),
('Conferência'),
('Jantar de Gala'),
('Workshop');

-- =========================
-- TIPOS DE MENU
-- =========================
INSERT INTO Tipo_Menu (designacao)
VALUES
('Premium'),
('Tradicional'),
('Vegetariano'),
('Executivo'),
('Buffet');

-- =========================
-- MENUS
-- =========================
INSERT INTO Menu (id_tipo_menu, descricao)
VALUES
(1, 'Menu premium com entradas, prato principal e sobremesa'),
(2, 'Menu tradicional português'),
(3, 'Menu vegetariano saudável'),
(4, 'Menu executivo para empresas'),
(5, 'Buffet livre com bebidas incluídas'),
(1, 'Menu luxo gourmet'),
(2, 'Menu económico para festas');

-- =========================
-- FUNÇÕES DE EMPREGADO
-- =========================
INSERT INTO Funcao_Empregado (designacao)
VALUES
('Cozinheiro'),
('Empregado de Mesa'),
('Barman'),
('Gestor de Evento'),
('Auxiliar de Cozinha'),
('Segurança');

-- =========================
-- EMPREGADOS
-- =========================
INSERT INTO Empregado (id_funcao_empregado, localidade, morada, codigo_postal, nome, telefone, preco_hora, NIF)
VALUES
(1, 'Braga', 'Rua A 10', '4700-200', 'Carlos Ferreira', '915111111', 15.00, '111111111'),
(2, 'Porto', 'Rua B 20', '4000-300', 'Ana Martins', '916222222', 10.50, '222222222'),
(3, 'Braga', 'Rua C 30', '4700-300', 'Ricardo Sousa', '917333333', 12.00, '333333333'),
(4, 'Coimbra', 'Rua D 40', '3000-400', 'Sofia Almeida', '918444444', 20.00, '444444444'),
(5, 'Guimarães', 'Rua E 50', '4800-200', 'Miguel Costa', '919555555', 9.00, '555555555'),
(1, 'Aveiro', 'Rua F 60', '3800-100', 'Bruno Gomes', '911666666', 16.00, '666666666'),
(2, 'Braga', 'Rua G 70', '4700-400', 'Mariana Dias', '912777777', 11.50, '777777777'),
(3, 'Porto', 'Rua H 80', '4000-500', 'Tiago Pinto', '913888888', 13.00, '888888888'),
(6, 'Coimbra', 'Rua I 90', '3000-500', 'Hugo Mendes', '914999999', 8.50, '999999999'),
(4, 'Viana do Castelo', 'Rua J 11', '4900-100', 'Patrícia Vieira', '915000000', 22.00, '101010101');

-- =========================
-- FORNECEDORES
-- =========================
INSERT INTO Fornecedor (localidade, morada, codigo_postal, nome, telefone)
VALUES
('Braga', 'Zona Industrial Braga', '4705-100', 'Carnes do Minho', '919111111'),
('Porto', 'Rua das Bebidas 15', '4000-500', 'Distribuidora Bebidas Norte', '919222222'),
('Coimbra', 'Rua Verde 7', '3000-250', 'Hortifruti Coimbra', '919333333'),
('Aveiro', 'Rua do Mar 8', '3800-220', 'Peixes Atlântico', '919444444'),
('Guimarães', 'Rua do Campo 12', '4800-350', 'Quinta Agrícola', '919555555');

-- =========================
-- SERVIÇOS
-- =========================
INSERT INTO Servico (custo, descricao)
VALUES
(500.00, 'Animação musical'),
(300.00, 'Decoração do espaço'),
(200.00, 'Fotografia profissional'),
(700.00, 'DJ e iluminação'),
(1000.00, 'Fireworks show'),
(450.00, 'Vídeo profissional');

INSERT INTO Servico_Interno (id_servico)
VALUES
(2),
(4);

INSERT INTO Servico_Externo (id_servico, id_fornecedor)
VALUES
(1, 2),
(3, 1),
(5, 2),
(6, 4);

-- =========================
-- TIPOS DE INGREDIENTE
-- =========================
INSERT INTO Tipo_Ingrediente (designacao)
VALUES
('Carne'),
('Vegetais'),
('Bebidas'),
('Laticínios'),
('Peixe'),
('Fruta');

-- =========================
-- SUBTIPOS DE INGREDIENTE
-- =========================
INSERT INTO Subtipo_Ingrediente (id_tipo_ingrediente, designacao)
VALUES
(1, 'Vaca'),
(1, 'Frango'),
(2, 'Legumes Frescos'),
(3, 'Refrigerantes'),
(4, 'Queijos'),
(5, 'Salmão'),
(6, 'Citrinos'),
(1, 'Porco');

-- =========================
-- INGREDIENTES
-- =========================
INSERT INTO Ingrediente (id_subtipo_ingrediente, id_fornecedor, data_validade, quantidade, custo, nome)
VALUES
(1, 1, '2026-12-31', 50, 250.00, 'Carne de Vaca'),
(2, 1, '2026-10-15', 80, 180.00, 'Peito de Frango'),
(3, 3, '2026-08-20', 100, 90.00, 'Cenoura'),
(4, 2, '2027-01-01', 200, 120.00, 'Coca-Cola'),
(5, 3, '2026-09-10', 40, 75.00, 'Queijo Flamengo'),
(6, 4, '2026-11-20', 60, 320.00, 'Salmão Fresco'),
(7, 5, '2026-07-30', 90, 50.00, 'Laranja'),
(8, 1, '2026-12-01', 70, 210.00, 'Carne de Porco');

-- =========================
-- LOTES
-- =========================
INSERT INTO Lote (id_ingrediente, id_fornecedor, preco, quantidade_deduzida, quantidade_deduzivel)
VALUES
(1, 1, 250.00, 10, 50),
(2, 1, 180.00, 20, 80),
(3, 3, 90.00, 15, 100),
(4, 2, 120.00, 50, 200),
(5, 3, 75.00, 5, 40),
(6, 4, 320.00, 10, 60),
(7, 5, 50.00, 12, 90),
(8, 1, 210.00, 8, 70);

-- =========================
-- TIPOS DE BEBIDA
-- =========================
INSERT INTO Tipo_Bebida (designacao)
VALUES
('Refrigerante'),
('Sumo'),
('Água'),
('Cocktail');

-- =========================
-- BEBIDAS
-- =========================
INSERT INTO Bebida (id_tipo_bebida, nome, receita)
VALUES
(1, 'Coca-Cola', 'Servir fresca'),
(2, 'Sumo de Laranja', 'Laranja espremida natural'),
(3, 'Água Mineral', 'Servir fria'),
(4, 'Mojito', 'Misturar lima e hortelã'),
(2, 'Sumo Tropical', 'Mistura de frutas');

-- =========================
-- TIPOS DE PRATO
-- =========================
INSERT INTO Tipo_Prato (designacao)
VALUES
('Entrada'),
('Prato Principal'),
('Sobremesa');

-- =========================
-- PRATOS
-- =========================
INSERT INTO Prato (id_tipo_prato, nome, receita)
VALUES
(1, 'Sopa de Legumes', 'Cozer legumes e triturar'),
(2, 'Francesinha', 'Preparar carne e molho'),
(2, 'Frango Assado', 'Assar frango temperado'),
(3, 'Mousse de Chocolate', 'Misturar chocolate e natas'),
(2, 'Salmão Grelhado', 'Grelhar salmão com ervas'),
(1, 'Bruschetta', 'Pão torrado com tomate'),
(3, 'Cheesecake', 'Preparar base e recheio');

-- =========================
-- CONSTITUIÇÃO DOS MENUS
-- =========================
INSERT INTO Constituicao_Menu_Pratos (id_menu, id_prato)
VALUES
(1, 1),(1, 2),(1, 4),
(2, 1),(2, 3),
(3, 1),(3, 6),
(4, 2),(4, 5),
(5, 1),(5, 2),(5, 3),(5, 7),
(6, 5),(6, 7),
(7, 3);

INSERT INTO Constituicao_Menu_Bebidas (id_menu, id_bebida)
VALUES
(1, 1),(1, 3),
(2, 2),
(3, 3),
(4, 4),
(5, 1),(5, 2),(5, 3),
(6, 4),(6, 5),
(7, 3);

-- =========================
-- CONSTITUIÇÃO DOS PRATOS
-- =========================
INSERT INTO Constituicao_Prato (id_prato, id_ingrediente, quantidade)
VALUES
(1, 3, 5),
(2, 1, 3),
(3, 2, 2),
(4, 5, 1),
(5, 6, 2),
(6, 3, 1),
(7, 5, 2);

-- =========================
-- CONSTITUIÇÃO DAS BEBIDAS
-- =========================
INSERT INTO Constituicao_Bebida (id_bebida, id_ingrediente, quantidade)
VALUES
(1, 4, 1),
(2, 7, 2),
(4, 7, 1),
(5, 7, 3);

-- =========================
-- EVENTOS
-- =========================
INSERT INTO Evento (id_cliente, id_menu, id_tipo_evento, custo, morada, codigo_postal, duracao, nr_pessoas, margem, localidade, data_evento)
VALUES
(1, 1, 1, 5000.00, 'Quinta do Lago', '4700-500', 8, 120, 25.00, 'Braga', '2026-08-10 15:00:00'),
(2, 2, 3, 2500.00, 'Centro de Congressos', '4000-600', 6, 80, 20.00, 'Porto', '2026-09-15 10:00:00'),
(3, 3, 4, 1200.00, 'Rua das Festas 12', '3000-300', 5, 40, 15.00, 'Coimbra', '2026-07-20 18:00:00'),
(4, 4, 5, 7000.00, 'Hotel Premium', '4710-400', 10, 200, 30.00, 'Braga', '2026-11-05 09:00:00'),
(5, 5, 2, 1800.00, 'Quinta da Serra', '4800-500', 7, 60, 18.00, 'Guimarães', '2026-06-22 14:00:00'),
(6, 6, 6, 9500.00, 'Salão Atlântico', '4900-700', 12, 300, 35.00, 'Viana do Castelo', '2026-12-18 20:00:00'),
(7, 5, 3, 4000.00, 'Centro Empresarial', '3800-300', 9, 150, 22.00, 'Aveiro', '2026-10-11 11:00:00'),
(8, 7, 4, 900.00, 'Casa Particular', '5000-400', 4, 25, 10.00, 'Vila Real', '2026-05-30 17:00:00');

-- =========================
-- EMPREGADOS NOS EVENTOS
-- =========================
INSERT INTO Trabalha_Em (id_empregado, id_evento, duracao)
VALUES
(1, 1, 8),(2, 1, 8),(3, 1, 8),
(4, 2, 6),(2, 3, 5),
(5, 4, 10),(6, 4, 10),(7, 4, 10),(10, 4, 10),
(1, 5, 7),(9, 5, 7),
(3, 6, 12),(8, 6, 12),(10, 6, 12),
(4, 7, 9),(7, 7, 9),
(2, 8, 4);

-- =========================
-- SERVIÇOS NOS EVENTOS
-- =========================
INSERT INTO Servico_Evento (id_servico, id_evento)
VALUES
(1, 1),(2, 1),(3, 2),
(4, 4),(5, 6),(6, 7),
(1, 5),(2, 7),(3, 8);


