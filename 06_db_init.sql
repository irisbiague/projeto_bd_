USE Projeto;
GO

-- =========================
-- CLIENTES
-- =========================
INSERT INTO DDL.Cliente (tipo_cliente, telefone, NIF, morada, codigo_postal, localidade, nome)
VALUES
(N'Particular', N'912345678', N'123456789', N'Rua das Flores 10',    N'4700-100', N'Braga',            N'João Silva'),
(N'Empresa',    N'913456789', N'987654321', N'Avenida Central 50',   N'4000-200', N'Porto',            N'Eventos XPTO Lda'),
(N'Particular', N'914567890', N'456789123', N'Rua do Sol 22',        N'3000-150', N'Coimbra',          N'Maria Costa'),
(N'Empresa',    N'915678901', N'321654987', N'Rua Industrial 9',     N'4710-250', N'Braga',            N'Tech Solutions'),
(N'Particular', N'916789012', N'741852963', N'Rua Nova 15',          N'4800-300', N'Guimarães',        N'Pedro Fernandes'),
(N'Particular', N'917890123', N'159357486', N'Rua Verde 2',          N'4900-500', N'Viana do Castelo', N'Inês Ribeiro'),
(N'Empresa',    N'918901234', N'258369147', N'Zona Empresarial',      N'3800-120', N'Aveiro',           N'Atlantic Corp'),
(N'Particular', N'919012345', N'951753852', N'Rua do Monte 90',      N'5000-200', N'Vila Real',        N'Rita Lopes');

-- =========================
-- TIPOS DE EVENTO
-- =========================
INSERT INTO DDL.Tipo_evento (descricao)
VALUES
(N'Casamento'),
(N'Batizado'),
(N'Evento Empresarial'),
(N'Aniversário'),
(N'Conferência'),
(N'Jantar de Gala'),
(N'Workshop');

-- =========================
-- TIPOS DE MENU
-- =========================
INSERT INTO DDL.Tipo_Menu (designacao)
VALUES
(N'Premium'),
(N'Tradicional'),
(N'Vegetariano'),
(N'Executivo'),
(N'Buffet');

-- =========================
-- MENUS
-- =========================
INSERT INTO DDL.Menu (id_tipo_menu, descricao)
VALUES
(1, N'Menu premium com entradas, prato principal e sobremesa'),
(2, N'Menu tradicional português'),
(3, N'Menu vegetariano saudável'),
(4, N'Menu executivo para empresas'),
(5, N'Buffet livre com bebidas incluídas'),
(1, N'Menu luxo gourmet'),
(2, N'Menu económico para festas');

-- =========================
-- FUNÇÕES DE EMPREGADO
-- =========================
INSERT INTO DDL.Funcao_Empregado (designacao)
VALUES
(N'Cozinheiro'),
(N'Empregado de Mesa'),
(N'Barman'),
(N'Gestor de Evento'),
(N'Auxiliar de Cozinha'),
(N'Segurança');

-- =========================
-- EMPREGADOS
-- =========================
INSERT INTO DDL.Empregado (id_funcao_empregado, localidade, morada, codigo_postal, nome, telefone, preco_hora, NIF)
VALUES
(1, N'Braga',            N'Rua A 10', N'4700-200', N'Carlos Ferreira',  N'915111111', 15.00, N'111111111'),
(2, N'Porto',            N'Rua B 20', N'4000-300', N'Ana Martins',      N'916222222', 10.50, N'222222222'),
(3, N'Braga',            N'Rua C 30', N'4700-300', N'Ricardo Sousa',    N'917333333', 12.00, N'333333333'),
(4, N'Coimbra',          N'Rua D 40', N'3000-400', N'Sofia Almeida',    N'918444444', 20.00, N'444444444'),
(5, N'Guimarães',        N'Rua E 50', N'4800-200', N'Miguel Costa',     N'919555555',  9.00, N'555555555'),
(1, N'Aveiro',           N'Rua F 60', N'3800-100', N'Bruno Gomes',      N'911666666', 16.00, N'666666666'),
(2, N'Braga',            N'Rua G 70', N'4700-400', N'Mariana Dias',     N'912777777', 11.50, N'777777777'),
(3, N'Porto',            N'Rua H 80', N'4000-500', N'Tiago Pinto',      N'913888888', 13.00, N'888888888'),
(6, N'Coimbra',          N'Rua I 90', N'3000-500', N'Hugo Mendes',      N'914999999',  8.50, N'999999999'),
(4, N'Viana do Castelo', N'Rua J 11', N'4900-100', N'Patrícia Vieira',  N'915000000', 22.00, N'101010101');

-- =========================
-- FORNECEDORES
-- =========================
INSERT INTO DDL.Fornecedor (localidade, morada, codigo_postal, nome, telefone)
VALUES
(N'Braga',      N'Zona Industrial Braga',  N'4705-100', N'Carnes do Minho',           N'919111111'),
(N'Porto',      N'Rua das Bebidas 15',     N'4000-500', N'Distribuidora Bebidas Norte',N'919222222'),
(N'Coimbra',    N'Rua Verde 7',            N'3000-250', N'Hortifruti Coimbra',         N'919333333'),
(N'Aveiro',     N'Rua do Mar 8',           N'3800-220', N'Peixes Atlântico',           N'919444444'),
(N'Guimarães',  N'Rua do Campo 12',        N'4800-350', N'Quinta Agrícola',            N'919555555');

-- =========================
-- SERVIÇOS
-- =========================
INSERT INTO DDL.Servico (custo, descricao)
VALUES
( 500.00, N'Animação musical'),
( 300.00, N'Decoração do espaço'),
( 200.00, N'Fotografia profissional'),
( 700.00, N'DJ e iluminação'),
(1000.00, N'Fireworks show'),
( 450.00, N'Vídeo profissional');

INSERT INTO DDL.Servico_Interno (id_servico)
VALUES (2), (4);

INSERT INTO DDL.Servico_Externo (id_servico, id_fornecedor)
VALUES (1, 2), (3, 1), (5, 2), (6, 4);

-- =========================
-- TIPOS DE INGREDIENTE
-- =========================
INSERT INTO DDL.Tipo_Ingrediente (designacao)
VALUES
(N'Carne'),
(N'Vegetais'),
(N'Bebidas'),
(N'Laticínios'),
(N'Peixe'),
(N'Fruta');

-- =========================
-- SUBTIPOS DE INGREDIENTE
-- =========================
INSERT INTO DDL.Subtipo_Ingrediente (id_tipo_ingrediente, designacao)
VALUES
(1, N'Vaca'),
(1, N'Frango'),
(2, N'Legumes Frescos'),
(3, N'Refrigerantes'),
(4, N'Queijos'),
(5, N'Salmão'),
(6, N'Citrinos'),
(1, N'Porco');

-- =========================
-- INGREDIENTES
-- =========================
INSERT INTO DDL.Ingrediente (id_subtipo_ingrediente, id_fornecedor, data_validade, quantidade, custo, nome)
VALUES
(1, 1, '2026-12-31', 50, 250.00, N'Carne de Vaca'),
(2, 1, '2026-10-15', 80, 180.00, N'Peito de Frango'),
(3, 3, '2026-08-20',100,  90.00, N'Cenoura'),
(4, 2, '2027-01-01',200, 120.00, N'Coca-Cola'),
(5, 3, '2026-09-10', 40,  75.00, N'Queijo Flamengo'),
(6, 4, '2026-11-20', 60, 320.00, N'Salmão Fresco'),
(7, 5, '2026-07-30', 90,  50.00, N'Laranja'),
(8, 1, '2026-12-01', 70, 210.00, N'Carne de Porco');

-- =========================
-- LOTES
-- =========================
INSERT INTO DDL.Lote (id_ingrediente, id_fornecedor, preco, quantidade_deduzida, quantidade_deduzivel)
VALUES
(1, 1, 250.00, 10, 50),
(2, 1, 180.00, 20, 80),
(3, 3,  90.00, 15,100),
(4, 2, 120.00, 50,200),
(5, 3,  75.00,  5, 40),
(6, 4, 320.00, 10, 60),
(7, 5,  50.00, 12, 90),
(8, 1, 210.00,  8, 70);

-- =========================
-- TIPOS DE BEBIDA
-- =========================
INSERT INTO DDL.Tipo_Bebida (designacao)
VALUES
(N'Refrigerante'),
(N'Sumo'),
(N'Água'),
(N'Cocktail');

-- =========================
-- BEBIDAS
-- =========================
INSERT INTO DDL.Bebida (id_tipo_bebida, nome, receita)
VALUES
(1, N'Coca-Cola',       N'Servir fresca'),
(2, N'Sumo de Laranja', N'Laranja espremida natural'),
(3, N'Água Mineral',    N'Servir fria'),
(4, N'Mojito',          N'Misturar lima e hortelã'),
(2, N'Sumo Tropical',   N'Mistura de frutas');

-- =========================
-- TIPOS DE PRATO
-- =========================
INSERT INTO DDL.Tipo_Prato (designacao)
VALUES
(N'Entrada'),
(N'Prato Principal'),
(N'Sobremesa');

-- =========================
-- PRATOS
-- =========================
INSERT INTO DDL.Prato (id_tipo_prato, nome, receita)
VALUES
(1, N'Sopa de Legumes',    N'Cozer legumes e triturar'),
(2, N'Francesinha',        N'Preparar carne e molho'),
(2, N'Frango Assado',      N'Assar frango temperado'),
(3, N'Mousse de Chocolate',N'Misturar chocolate e natas'),
(2, N'Salmão Grelhado',    N'Grelhar salmão com ervas'),
(1, N'Bruschetta',         N'Pão torrado com tomate'),
(3, N'Cheesecake',         N'Preparar base e recheio');

-- =========================
-- CONSTITUIÇÃO DOS MENUS
-- =========================
INSERT INTO DDL.Constituicao_Menu_Pratos (id_menu, id_prato)
VALUES
(1,1),(1,2),(1,4),
(2,1),(2,3),
(3,1),(3,6),
(4,2),(4,5),
(5,1),(5,2),(5,3),(5,7),
(6,5),(6,7),
(7,3);

INSERT INTO DDL.Constituicao_Menu_Bebidas (id_menu, id_bebida)
VALUES
(1,1),(1,3),
(2,2),
(3,3),
(4,4),
(5,1),(5,2),(5,3),
(6,4),(6,5),
(7,3);

-- =========================
-- CONSTITUIÇÃO DOS PRATOS
-- =========================
INSERT INTO DDL.Constituicao_Prato (id_prato, id_ingrediente, quantidade)
VALUES
(1,3,5),
(2,1,3),
(3,2,2),
(4,5,1),
(5,6,2),
(6,3,1),
(7,5,2);

-- =========================
-- CONSTITUIÇÃO DAS BEBIDAS
-- =========================
INSERT INTO DDL.Constituicao_Bebida (id_bebida, id_ingrediente, quantidade)
VALUES
(1,4,1),
(2,7,2),
(4,7,1),
(5,7,3);

-- =========================
-- EVENTOS
-- =========================
INSERT INTO DDL.Evento (id_cliente, id_menu, id_tipo_evento, custo, morada, codigo_postal, duracao, nr_pessoas, margem, localidade, data_evento)
VALUES
(1,1,1, 5000.00, N'Quinta do Lago',         N'4700-500',  8,120,25.00, N'Braga',            N'2026-08-10 15:00:00'),
(2,2,3, 2500.00, N'Centro de Congressos',   N'4000-600',  6, 80,20.00, N'Porto',            N'2026-09-15 10:00:00'),
(3,3,4, 1200.00, N'Rua das Festas 12',      N'3000-300',  5, 40,15.00, N'Coimbra',          N'2026-07-20 18:00:00'),
(4,4,5, 7000.00, N'Hotel Premium',          N'4710-400', 10,200,30.00, N'Braga',            N'2026-11-05 09:00:00'),
(5,5,2, 1800.00, N'Quinta da Serra',        N'4800-500',  7, 60,18.00, N'Guimarães',        N'2026-06-22 14:00:00'),
(6,6,6, 9500.00, N'Salão Atlântico',        N'4900-700', 12,300,35.00, N'Viana do Castelo', N'2026-12-18 20:00:00'),
(7,5,3, 4000.00, N'Centro Empresarial',     N'3800-300',  9,150,22.00, N'Aveiro',           N'2026-10-11 11:00:00'),
(8,7,4,  900.00, N'Casa Particular',        N'5000-400',  4, 25,10.00, N'Vila Real',        N'2026-05-30 17:00:00');

-- =========================
-- EMPREGADOS NOS EVENTOS
-- =========================
INSERT INTO DDL.Trabalha_Em (id_empregado, id_evento, duracao)
VALUES
(1,1,8),(2,1,8),(3,1,8),
(4,2,6),(2,3,5),
(5,4,10),(6,4,10),(7,4,10),(10,4,10),
(1,5,7),(9,5,7),
(3,6,12),(8,6,12),(10,6,12),
(4,7,9),(7,7,9),
(2,8,4);

-- =========================
-- SERVIÇOS NOS EVENTOS
-- =========================
INSERT INTO DDL.Servico_Evento (id_servico, id_evento)
VALUES
(1,1),(2,1),(3,2),
(4,4),(5,6),(6,7),
(1,5),(2,7),(3,8);
