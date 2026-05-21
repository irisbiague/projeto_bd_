DROP DATABASE Projeto;
-- script usado para a BD Local
CREATE DATABASE Projeto;
GO
USE Projeto;
GO

-- script para a BD da aula
CREATE SCHEMA Projeto;

-- Cliente
CREATE TABLE Cliente (
    id_cliente      INT IDENTITY PRIMARY KEY,
    tipo_cliente    VARCHAR(50) NOT NULL,
    telefone        VARCHAR(20),
    NIF             CHAR(9) UNIQUE NOT NULL,
    morada          VARCHAR(150),
    codigo_postal   CHAR(8),
    localidade      VARCHAR(80),
    nome            VARCHAR(100),
	isdeleted		INT DEFAULT 0,

    CONSTRAINT CHK_Cliente_Tipo
        CHECK (tipo_cliente IN ('Particular', 'Empresa')),

    CONSTRAINT CHK_Cliente_Telefone
        CHECK (telefone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),

    CONSTRAINT CHK_Cliente_NIF
        CHECK (NIF LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),

	CONSTRAINT CHK_Cliente_IsDeleted
		CHECK (isdeleted IN (0,1))
);

-- Tipo_evento
CREATE TABLE Tipo_evento (
    id_tipo_evento INT IDENTITY PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
	isdeleted INT DEFAULT 0,

    CONSTRAINT CHK_TipoEvento_Descricao
        CHECK (LEN(descricao) > 0),
	
	CONSTRAINT CHK_Tipo_Evento_IsDeleted
		CHECK (isdeleted IN (0,1))
);

-- Tipo_Menu
CREATE TABLE Tipo_Menu (
    id_tipo_menu    INT IDENTITY PRIMARY KEY,
    designacao      VARCHAR(80),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_TipoMenu_Designacao
        CHECK (LEN(designacao) > 0),
    
    CONSTRAINT CHK_Tipo_Menu_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Menu
CREATE TABLE Menu (
    id_menu         INT IDENTITY PRIMARY KEY,    
    id_tipo_menu    INT,
    descricao       VARCHAR(150),
    isdeleted       INT DEFAULT 0,

    FOREIGN KEY (id_tipo_menu)
        REFERENCES Tipo_Menu(id_tipo_menu),    

    CONSTRAINT CHK_Menu_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Evento
CREATE TABLE Evento (
    id_evento       INT IDENTITY PRIMARY KEY,
    id_cliente      INT NOT NULL,
    id_menu         INT NOT NULL,
    id_tipo_evento  INT NOT NULL,
    custo           DECIMAL(10,2),
    morada          VARCHAR(150),
    codigo_postal   CHAR(8),
    duracao         INT,
    nr_pessoas      INT,
    margem          DECIMAL(5,2),
    localidade      VARCHAR(80),
    data_evento     DATETIME NOT NULL,
    isdeleted       INT DEFAULT 0,

    FOREIGN KEY (id_cliente)
        REFERENCES Cliente(id_cliente),

    FOREIGN KEY (id_menu)
        REFERENCES Menu(id_menu),

    FOREIGN KEY (id_tipo_evento)
        REFERENCES Tipo_evento(id_tipo_evento),

    CONSTRAINT CHK_Evento_Custo
        CHECK (custo >= 0),

    CONSTRAINT CHK_Evento_Duracao
        CHECK (duracao > 0),

    CONSTRAINT CHK_Evento_Pessoas
        CHECK (nr_pessoas > 0),

    CONSTRAINT CHK_Evento_Margem
        CHECK (margem BETWEEN 0 AND 100),    

    CONSTRAINT CHK_Evento_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Função_Empregado
CREATE TABLE Funcao_Empregado (
    id_funcao_empregado     INT IDENTITY PRIMARY KEY,
    designacao              VARCHAR(100),
    isdeleted               INT DEFAULT 0,

    CONSTRAINT CHK_FuncaoEmpregado_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Funcao_Empregado_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Empregado
CREATE TABLE Empregado (
    id_empregado            INT IDENTITY PRIMARY KEY,
    id_funcao_empregado     INT NOT NULL,
    localidade              VARCHAR(80),
    morada                  VARCHAR(150),
    codigo_postal           CHAR(8),
    nome                    VARCHAR(100),
    telefone                VARCHAR(20),
    preco_hora              DECIMAL(10,2),
    NIF                     CHAR(9) UNIQUE,
    isdeleted               INT DEFAULT 0,

    FOREIGN KEY (id_funcao_empregado)
        REFERENCES Funcao_Empregado(id_funcao_empregado),

    CONSTRAINT CHK_Empregado_Preco
        CHECK (preco_hora >= 0),

    CONSTRAINT CHK_Empregado_Telefone
        CHECK (telefone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),

    CONSTRAINT CHK_Empregado_NIF
        CHECK (NIF LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),    

    CONSTRAINT CHK_Empregado_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Trabalha_Em
CREATE TABLE Trabalha_Em (
    id_empregado    INT,
    id_evento       INT,
    duracao         INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_empregado, id_evento),

    FOREIGN KEY (id_empregado)
        REFERENCES Empregado(id_empregado),

    FOREIGN KEY (id_evento)
        REFERENCES Evento(id_evento),

    CONSTRAINT CHK_TrabalhaEm_Duracao
        CHECK (duracao > 0),    

    CONSTRAINT CHK_Trabalha_Em_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Serviço
CREATE TABLE Servico (
    id_servico      INT IDENTITY PRIMARY KEY,
    custo           DECIMAL(10,2),
    descricao       VARCHAR(150),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_Servico_Custo
        CHECK (custo >= 0),    

    CONSTRAINT CHK_Servico_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Serviço_Interno
CREATE TABLE Servico_Interno (
    id_servico  INT PRIMARY KEY,
    isdeleted   INT DEFAULT 0,

    FOREIGN KEY (id_servico)    
		REFERENCES Servico(id_servico),    

    CONSTRAINT CHK_Servico_Interno_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Fornecedor
CREATE TABLE Fornecedor (
    id_fornecedor   INT IDENTITY PRIMARY KEY,
    localidade      VARCHAR(80),
    morada          VARCHAR(150),
    codigo_postal   CHAR(8),
    nome            VARCHAR(100),
    telefone        VARCHAR(20),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_Fornecedor_Telefone
        CHECK (telefone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),    

    CONSTRAINT CHK_Fornecedor_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Serviço_Externo
CREATE TABLE Servico_Externo (
    id_servico      INT,
    id_fornecedor   INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_servico, id_fornecedor),

    FOREIGN KEY (id_servico)        
        REFERENCES Servico(id_servico),

    FOREIGN KEY (id_fornecedor)     
        REFERENCES Fornecedor(id_fornecedor),    

    CONSTRAINT CHK_Servico_Externo_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Serviço_Evento
CREATE TABLE Servico_Evento (
	id_servico  INT,
    id_evento   INT,
    isdeleted INT DEFAULT 0,

    PRIMARY KEY (id_servico, id_evento),

    FOREIGN KEY (id_servico)    
        REFERENCES Servico(id_servico),

    FOREIGN KEY (id_evento)     
        REFERENCES Evento(id_evento),    

    CONSTRAINT CHK_Servico_Evento_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Tipo_Ingrediente
CREATE TABLE Tipo_Ingrediente (
    id_tipo_ingrediente     INT IDENTITY PRIMARY KEY,
    designacao              VARCHAR(80),
    isdeleted               INT DEFAULT 0,

    CONSTRAINT CHK_TipoIngrediente_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Tipo_Ingrediente_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Subtipo_Ingrediente
CREATE TABLE Subtipo_Ingrediente (
    id_subtipo_ingrediente  INT IDENTITY PRIMARY KEY,
    id_tipo_ingrediente     INT,
    designacao              VARCHAR(80),
    isdeleted               INT DEFAULT 0,

     FOREIGN KEY (id_tipo_ingrediente)
        REFERENCES Tipo_Ingrediente(id_tipo_ingrediente),

    CONSTRAINT CHK_SubtipoIngrediente_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Subtipo_Ingrediente_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Ingrediente
CREATE TABLE Ingrediente (
    id_ingrediente              INT IDENTITY PRIMARY KEY,
    id_subtipo_ingrediente      INT,
    id_fornecedor               INT,
    data_validade               DATE,
    quantidade                  INT,
    custo                       DECIMAL(10,2),
    nome                        VARCHAR(100),
	unidade						VARCHAR(5),
    isdeleted                   INT DEFAULT 0,

    FOREIGN KEY (id_subtipo_ingrediente)
        REFERENCES Subtipo_Ingrediente(id_subtipo_ingrediente),

    FOREIGN KEY (id_fornecedor)
        REFERENCES Fornecedor(id_fornecedor),

    CONSTRAINT CHK_Ingrediente_Quantidade
        CHECK (quantidade >= 0),

    CONSTRAINT CHK_Ingrediente_Custo
        CHECK (custo >= 0),    

    CONSTRAINT CHK_Ingrediente_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Lote
CREATE TABLE Lote (
    id_lote                 INT IDENTITY PRIMARY KEY,
    id_ingrediente          INT,
    id_fornecedor           INT,
    preco                   DECIMAL(10,2),
    quantidade_deduzida     INT,
    quantidade_deduzivel    INT,
    isdeleted				INT DEFAULT 0,

    FOREIGN KEY (id_ingrediente)
        REFERENCES Ingrediente(id_ingrediente),

    FOREIGN KEY (id_fornecedor)
        REFERENCES Fornecedor(id_fornecedor),

    CONSTRAINT CHK_Lote_Preco
        CHECK (preco >= 0),

    CONSTRAINT CHK_Lote_QuantidadeDeduzida
        CHECK (quantidade_deduzida >= 0),

    CONSTRAINT CHK_Lote_QuantidadeDeduzivel
        CHECK (quantidade_deduzivel >= 0),

    CONSTRAINT CHK_Lote_Quantidades
        CHECK (quantidade_deduzida <= quantidade_deduzivel),    

    CONSTRAINT CHK_Lote_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Tipo_Bebida
CREATE TABLE Tipo_Bebida (
    id_tipo_bebida  INT IDENTITY PRIMARY KEY,
    designacao      VARCHAR(80),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_TipoBebida_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Tipo_Bebida_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Bebida
CREATE TABLE Bebida (
    id_bebida           INT IDENTITY PRIMARY KEY,    
    id_tipo_bebida      INT,
    nome                VARCHAR(80),
    receita             TEXT,
    isdeleted           INT DEFAULT 0,

    FOREIGN KEY (id_tipo_bebida)
        REFERENCES Tipo_Bebida(id_tipo_bebida), 

    CONSTRAINT CHK_Bebida_nome
        CHECK (LEN(nome) > 0),    

    CONSTRAINT CHK_Bebida_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Tipo_Prato
CREATE TABLE Tipo_Prato (
    id_tipo_prato   INT IDENTITY PRIMARY KEY,
    designacao      VARCHAR(80),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_TipoPrato_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Tipo_Prato_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Prato
CREATE TABLE Prato (
    id_prato        INT IDENTITY PRIMARY KEY,    
    id_tipo_prato   INT,
    nome            VARCHAR(80),
    receita         TEXT,
    isdeleted       INT DEFAULT 0,
	   
    FOREIGN KEY (id_tipo_prato)
        REFERENCES Tipo_Prato(id_tipo_prato),

    CONSTRAINT CHK_Prato_nome
        CHECK (LEN(nome) > 0),    

    CONSTRAINT CHK_Prato_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao do Menu (Pratos)
CREATE TABLE Constituicao_Menu_Pratos (
    id_menu     INT,
    id_prato    INT,
    isdeleted INT DEFAULT 0,

    PRIMARY KEY (id_menu,id_prato),

    FOREIGN KEY (id_menu)
        REFERENCES Menu(id_menu),

    FOREIGN KEY (id_prato)
        REFERENCES Prato(id_prato),    

    CONSTRAINT CHK_Constituicao_Menu_Pratos_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao do Menu (Bebidas)
CREATE TABLE Constituicao_Menu_Bebidas (
    id_menu     INT,
    id_bebida   INT,
    isdeleted   INT DEFAULT 0,

    PRIMARY KEY (id_menu,id_bebida),

    FOREIGN KEY (id_menu)
        REFERENCES Menu(id_menu),

    FOREIGN KEY (id_bebida)
        REFERENCES Bebida(id_bebida),    

    CONSTRAINT CHK_Constituicao_Menu_Bebidas_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao_Prato
CREATE TABLE Constituicao_Prato (
    id_prato        INT,
    id_ingrediente  INT,
    quantidade      INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_prato, id_ingrediente),

    FOREIGN KEY (id_prato)
        REFERENCES Prato(id_prato),

    FOREIGN KEY (id_ingrediente)
        REFERENCES Ingrediente(id_ingrediente),

    CONSTRAINT CHK_ConstituicaoPrato_Quantidade
        CHECK (quantidade > 0),    

    CONSTRAINT CHK_Constituicao_Prato_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao_Bebida
CREATE TABLE Constituicao_Bebida (
    id_bebida       INT,
    id_ingrediente  INT,
    quantidade      INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_bebida, id_ingrediente),

    FOREIGN KEY (id_bebida)
        REFERENCES Bebida(id_bebida),

    FOREIGN KEY (id_ingrediente)
        REFERENCES Ingrediente(id_ingrediente),

    CONSTRAINT CHK_ConstituicaoBebida_Quantidade
        CHECK (quantidade > 0),    

    CONSTRAINT CHK_Constituicao_Bebida_IsDeleted
        CHECK (isdeleted IN (0,1))
);