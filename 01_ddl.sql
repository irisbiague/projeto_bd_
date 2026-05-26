DROP DATABASE Projeto;
-- script usado para a BD Local
CREATE DATABASE Projeto;
GO
USE Projeto;
GO

-- script para a BD da aula
CREATE SCHEMA DDL;
GO

CREATE SCHEMA UDF;
GO

CREATE SCHEMA SP;
GO

CREATE SCHEMA VIEWS;
GO

-- Cliente
CREATE TABLE DDL.Cliente (
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
CREATE TABLE DDL.Tipo_evento (
    id_tipo_evento INT IDENTITY PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
	isdeleted INT DEFAULT 0,

    CONSTRAINT CHK_TipoEvento_Descricao
        CHECK (LEN(descricao) > 0),
	
	CONSTRAINT CHK_Tipo_Evento_IsDeleted
		CHECK (isdeleted IN (0,1))
);

-- Tipo_Menu
CREATE TABLE DDL.Tipo_Menu (
    id_tipo_menu    INT IDENTITY PRIMARY KEY,
    designacao      VARCHAR(80),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_TipoMenu_Designacao
        CHECK (LEN(designacao) > 0),
    
    CONSTRAINT CHK_Tipo_Menu_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Menu
CREATE TABLE DDL.Menu (
    id_menu         INT IDENTITY PRIMARY KEY,    
    id_tipo_menu    INT,
    descricao       VARCHAR(150),
    isdeleted       INT DEFAULT 0,

    FOREIGN KEY (id_tipo_menu)
        REFERENCES DDL.Tipo_Menu(id_tipo_menu),    

    CONSTRAINT CHK_Menu_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Evento
CREATE TABLE DDL.Evento (
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
        REFERENCES DDL.Cliente(id_cliente),

    FOREIGN KEY (id_menu)
        REFERENCES DDL.Menu(id_menu),

    FOREIGN KEY (id_tipo_evento)
        REFERENCES DDL.Tipo_evento(id_tipo_evento),

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

-- Fun��o_Empregado
CREATE TABLE DDL.Funcao_Empregado (
    id_funcao_empregado     INT IDENTITY PRIMARY KEY,
    designacao              VARCHAR(100),
    isdeleted               INT DEFAULT 0,

    CONSTRAINT CHK_FuncaoEmpregado_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Funcao_Empregado_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Empregado
CREATE TABLE DDL.Empregado (
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
        REFERENCES DDL.Funcao_Empregado(id_funcao_empregado),

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
CREATE TABLE DDL.Trabalha_Em (
    id_empregado    INT,
    id_evento       INT,
    duracao         INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_empregado, id_evento),

    FOREIGN KEY (id_empregado)
        REFERENCES DDL.Empregado(id_empregado),

    FOREIGN KEY (id_evento)
        REFERENCES DDL.Evento(id_evento),

    CONSTRAINT CHK_TrabalhaEm_Duracao
        CHECK (duracao > 0),    

    CONSTRAINT CHK_Trabalha_Em_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Servi�o
CREATE TABLE DDL.Servico (
    id_servico      INT IDENTITY PRIMARY KEY,
    custo           DECIMAL(10,2),
    descricao       VARCHAR(150),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_Servico_Custo
        CHECK (custo >= 0),    

    CONSTRAINT CHK_Servico_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Servi�o_Interno
CREATE TABLE DDL.Servico_Interno (
    id_servico  INT PRIMARY KEY,
    isdeleted   INT DEFAULT 0,

    FOREIGN KEY (id_servico)    
		REFERENCES DDL.Servico(id_servico),    

    CONSTRAINT CHK_Servico_Interno_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Fornecedor
CREATE TABLE DDL.Fornecedor (
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

-- Servi�o_Externo
CREATE TABLE DDL.Servico_Externo (
    id_servico      INT,
    id_fornecedor   INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_servico, id_fornecedor),

    FOREIGN KEY (id_servico)        
        REFERENCES DDL.Servico(id_servico),

    FOREIGN KEY (id_fornecedor)     
        REFERENCES DDL.Fornecedor(id_fornecedor),    

    CONSTRAINT CHK_Servico_Externo_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Servi�o_Evento
CREATE TABLE DDL.Servico_Evento (
	id_servico  INT,
    id_evento   INT,
    isdeleted INT DEFAULT 0,

    PRIMARY KEY (id_servico, id_evento),

    FOREIGN KEY (id_servico)
        REFERENCES DDL.Servico(id_servico),

    FOREIGN KEY (id_evento)     
        REFERENCES DDL.Evento(id_evento),    

    CONSTRAINT CHK_Servico_Evento_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Tipo_Ingrediente
CREATE TABLE DDL.Tipo_Ingrediente (
    id_tipo_ingrediente     INT IDENTITY PRIMARY KEY,
    designacao              VARCHAR(80),
    isdeleted               INT DEFAULT 0,

    CONSTRAINT CHK_TipoIngrediente_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Tipo_Ingrediente_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Subtipo_Ingrediente
CREATE TABLE DDL.Subtipo_Ingrediente (
    id_subtipo_ingrediente  INT IDENTITY PRIMARY KEY,
    id_tipo_ingrediente     INT,
    designacao              VARCHAR(80),
    isdeleted               INT DEFAULT 0,

     FOREIGN KEY (id_tipo_ingrediente)
        REFERENCES DDL.Tipo_Ingrediente(id_tipo_ingrediente),

    CONSTRAINT CHK_SubtipoIngrediente_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Subtipo_Ingrediente_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Ingrediente
CREATE TABLE DDL.Ingrediente (
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
        REFERENCES DDL.Subtipo_Ingrediente(id_subtipo_ingrediente),

    FOREIGN KEY (id_fornecedor)
        REFERENCES DDL.Fornecedor(id_fornecedor),

    CONSTRAINT CHK_Ingrediente_Quantidade
        CHECK (quantidade >= 0),

    CONSTRAINT CHK_Ingrediente_Custo
        CHECK (custo >= 0),    

    CONSTRAINT CHK_Ingrediente_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Lote
CREATE TABLE DDL.Lote (
    id_lote                 INT IDENTITY PRIMARY KEY,
    id_ingrediente          INT,
    id_fornecedor           INT,
    preco                   DECIMAL(10,2),
    quantidade_deduzida     INT,
    quantidade_deduzivel    INT,
    isdeleted				INT DEFAULT 0,

    FOREIGN KEY (id_ingrediente)
        REFERENCES DDL.Ingrediente(id_ingrediente),

    FOREIGN KEY (id_fornecedor)
        REFERENCES DDL.Fornecedor(id_fornecedor),

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
CREATE TABLE DDL.Tipo_Bebida (
    id_tipo_bebida  INT IDENTITY PRIMARY KEY,
    designacao      VARCHAR(80),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_TipoBebida_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Tipo_Bebida_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Bebida
CREATE TABLE DDL.Bebida (
    id_bebida           INT IDENTITY PRIMARY KEY,    
    id_tipo_bebida      INT,
    nome                VARCHAR(80),
    receita             TEXT,
    isdeleted           INT DEFAULT 0,

    FOREIGN KEY (id_tipo_bebida)
        REFERENCES DDL.Tipo_Bebida(id_tipo_bebida), 

    CONSTRAINT CHK_Bebida_nome
        CHECK (LEN(nome) > 0),    

    CONSTRAINT CHK_Bebida_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Tipo_Prato
CREATE TABLE DDL.Tipo_Prato (
    id_tipo_prato   INT IDENTITY PRIMARY KEY,
    designacao      VARCHAR(80),
    isdeleted       INT DEFAULT 0,

    CONSTRAINT CHK_TipoPrato_Designacao
        CHECK (LEN(designacao) > 0),    

    CONSTRAINT CHK_Tipo_Prato_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Prato
CREATE TABLE DDL.Prato (
    id_prato        INT IDENTITY PRIMARY KEY,    
    id_tipo_prato   INT,
    nome            VARCHAR(80),
    receita         TEXT,
    isdeleted       INT DEFAULT 0,
	   
    FOREIGN KEY (id_tipo_prato)
        REFERENCES DDL.Tipo_Prato(id_tipo_prato),

    CONSTRAINT CHK_Prato_nome
        CHECK (LEN(nome) > 0),    

    CONSTRAINT CHK_Prato_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao do Menu (Pratos)
CREATE TABLE DDL.Constituicao_Menu_Pratos (
    id_menu     INT,
    id_prato    INT,
    isdeleted INT DEFAULT 0,

    PRIMARY KEY (id_menu,id_prato),

    FOREIGN KEY (id_menu)
        REFERENCES DDL.Menu(id_menu),

    FOREIGN KEY (id_prato)
        REFERENCES DDL.Prato(id_prato),    

    CONSTRAINT CHK_Constituicao_Menu_Pratos_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao do Menu (Bebidas)
CREATE TABLE DDL.Constituicao_Menu_Bebidas (
    id_menu     INT,
    id_bebida   INT,
    isdeleted   INT DEFAULT 0,

    PRIMARY KEY (id_menu,id_bebida),

    FOREIGN KEY (id_menu)
        REFERENCES DDL.Menu(id_menu),

    FOREIGN KEY (id_bebida)
        REFERENCES DDL.Bebida(id_bebida),    

    CONSTRAINT CHK_Constituicao_Menu_Bebidas_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao_Prato
CREATE TABLE DDL.Constituicao_Prato (
    id_prato        INT,
    id_ingrediente  INT,
    quantidade      INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_prato, id_ingrediente),

    FOREIGN KEY (id_prato)
        REFERENCES DDL.Prato(id_prato),

    FOREIGN KEY (id_ingrediente)
        REFERENCES DDL.Ingrediente(id_ingrediente),

    CONSTRAINT CHK_ConstituicaoPrato_Quantidade
        CHECK (quantidade > 0),    

    CONSTRAINT CHK_Constituicao_Prato_IsDeleted
        CHECK (isdeleted IN (0,1))
);

-- Constituicao_Bebida
CREATE TABLE DDL.Constituicao_Bebida (
    id_bebida       INT,
    id_ingrediente  INT,
    quantidade      INT,
    isdeleted       INT DEFAULT 0,

    PRIMARY KEY (id_bebida, id_ingrediente),

    FOREIGN KEY (id_bebida)
        REFERENCES DDL.Bebida(id_bebida),

    FOREIGN KEY (id_ingrediente)
        REFERENCES DDL.Ingrediente(id_ingrediente),

    CONSTRAINT CHK_ConstituicaoBebida_Quantidade
        CHECK (quantidade > 0),    

    CONSTRAINT CHK_Constituicao_Bebida_IsDeleted
        CHECK (isdeleted IN (0,1))
);