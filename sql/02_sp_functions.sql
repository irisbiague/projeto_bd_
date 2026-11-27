--- Functions
USE Projeto;
GO

CREATE OR ALTER FUNCTION UDF.fn_CalcularCustoEvento (@id_evento INT)
RETURNS DECIMAL(10,2)
AS
BEGIN

    DECLARE @custoIngredientes DECIMAL(10,2) = 0;
    DECLARE @custoEmpregados DECIMAL(10,2) = 0;
    DECLARE @custoServicos DECIMAL(10,2) = 0;
    DECLARE @nrPessoas INT = 0;
    DECLARE @total DECIMAL(10,2) = 0;
      
    SELECT @nrPessoas = nr_pessoas
    FROM DDL.Evento
    WHERE id_evento = @id_evento AND isdeleted = 0;

    SELECT @custoIngredientes = COALESCE(SUM(
            p.quantidade_necessaria *
            COALESCE(l.custo_total / NULLIF(l.quantidade_disponivel, 0), 0)
        ), 0)
    FROM (
        SELECT cp.id_ingrediente, SUM(cp.quantidade * ISNULL(ev.nr_pessoas, 0)) AS quantidade_necessaria
        FROM DDL.Evento ev
        INNER JOIN DDL.Menu m
            ON ev.id_menu = m.id_menu AND m.isdeleted = 0
        INNER JOIN DDL.Constituicao_Menu_Pratos cmp
            ON m.id_menu = cmp.id_menu
        INNER JOIN DDL.Constituicao_Prato cp
            ON cmp.id_prato = cp.id_prato
        INNER JOIN DDL.Ingrediente i
            ON cp.id_ingrediente = i.id_ingrediente AND i.isdeleted = 0
        WHERE ev.id_evento = @id_evento AND ev.isdeleted = 0
        GROUP BY cp.id_ingrediente

        UNION ALL

        SELECT cb.id_ingrediente, SUM(cb.quantidade * ISNULL(ev.nr_pessoas, 0)) AS quantidade_necessaria
        FROM DDL.Evento ev
        INNER JOIN DDL.Menu m
            ON ev.id_menu = m.id_menu AND m.isdeleted = 0
        INNER JOIN DDL.Constituicao_Menu_Bebidas cmb
            ON m.id_menu = cmb.id_menu
        INNER JOIN DDL.Bebida b
            ON cmb.id_bebida = b.id_bebida AND b.isdeleted = 0
        INNER JOIN DDL.Constituicao_Bebida cb
            ON b.id_bebida = cb.id_bebida
        INNER JOIN DDL.Ingrediente i
            ON cb.id_ingrediente = i.id_ingrediente AND i.isdeleted = 0
        WHERE ev.id_evento = @id_evento AND ev.isdeleted = 0
        GROUP BY cb.id_ingrediente
    ) p
    LEFT JOIN (
        SELECT id_ingrediente,
               SUM(preco * (quantidade_deduzivel - quantidade_deduzida)) AS custo_total,
               SUM(quantidade_deduzivel - quantidade_deduzida) AS quantidade_disponivel
        FROM DDL.Lote
        WHERE isdeleted = 0
        GROUP BY id_ingrediente
    ) l
        ON p.id_ingrediente = l.id_ingrediente;

    SELECT 
        @custoEmpregados = SUM(
            e.preco_hora * te.duracao
        )
    FROM DDL.Trabalha_Em te
    INNER JOIN DDL.Empregado e
        ON te.id_empregado = e.id_empregado AND e.isdeleted = 0
    WHERE te.id_evento = @id_evento AND te.isdeleted = 0;
    
    SELECT 
        @custoServicos = SUM(s.custo)
    FROM DDL.Servico_Evento se
    INNER JOIN DDL.Servico s
        ON se.id_servico = s.id_servico AND s.isdeleted = 0
    WHERE se.id_evento = @id_evento AND se.isdeleted = 0;

   SET @total =
        ISNULL(@custoIngredientes,0) +
        ISNULL(@custoEmpregados,0) +
        ISNULL(@custoServicos,0);

    RETURN @total;
END;
GO

CREATE OR ALTER FUNCTION UDF.fn_ServicosPorEvento (@id_evento INT)
RETURNS TABLE
AS
RETURN
(
    SELECT
        S.id_servico AS id_servico, 
        S.descricao
    FROM DDL.Servico_Evento SE
    INNER JOIN DDL.Servico S
        ON SE.id_servico = S.id_servico
    WHERE SE.id_evento = @id_evento AND SE.isdeleted = 0 AND S.isdeleted = 0
);
GO

CREATE OR ALTER FUNCTION UDF.fn_EventoPorId (@id_evento INT)
RETURNS TABLE
AS
RETURN
(
    SELECT E.*, 
        C.nome as cliente_nome, 
        C.NIF as cliente_nif, 
        C.tipo_cliente as cliente_tipo, 
        C.codigo_postal as cliente_cp, 
        C.localidade as cliente_localidade, 
        TE.descricao as tipo_evento
    FROM DDL.Evento E
        INNER JOIN DDL.Cliente C 
            ON E.id_cliente = C.id_cliente
        INNER JOIN DDL.Tipo_evento TE 
            ON E.id_tipo_evento = TE.id_tipo_evento
    WHERE E.id_evento = @id_evento AND E.isdeleted = 0
);
GO

CREATE OR ALTER FUNCTION UDF.fn_EmpregadosPorEvento (@id_evento INT)
RETURNS TABLE
AS
RETURN
(
    SELECT V.* 
    FROM VIEWS.V_Empregados_Evento V
    INNER JOIN DDL.Trabalha_Em TE 
        ON V.id_empregado = TE.id_empregado
    WHERE TE.id_evento = @id_evento 
      AND TE.isdeleted = 0
);
GO

CREATE OR ALTER FUNCTION UDF.fn_IngredientesQuantidadeCustoPorId (@id_ingrediente INT)
RETURNS TABLE
AS
RETURN
(
   SELECT * 
   FROM VIEWS.V_Ingredientes_quantidade_custo 
   WHERE id_ingrediente = @id_ingrediente 
);
GO

CREATE OR ALTER FUNCTION UDF.fn_LotesDetalhadosPorIngrediente (@id_ingrediente INT)
RETURNS TABLE
AS
RETURN
(
    SELECT L.id_lote, L.preco, L.quantidade_deduzivel, L.quantidade_deduzida, L.id_fornecedor, F.nome as fornecedor_nome
    FROM DDL.Lote L
        INNER JOIN DDL.Fornecedor F 
            ON L.id_fornecedor = F.id_fornecedor
        WHERE L.id_ingrediente = @id_ingrediente AND L.isdeleted = 0          
);
GO

--- Store Procedures
USE Projeto;
GO

CREATE OR ALTER PROCEDURE SP.sp_AdicionarEvento
(
    @id_cliente INT,
    @id_menu INT,
    @id_tipo_evento INT,
    @morada VARCHAR(255),
    @codigo_postal VARCHAR(20),
    @duracao INT,
    @nr_pessoas INT,
    @margem DECIMAL(10,2),
    @localidade VARCHAR(100),
    @data_evento DATETIME,
    @servicos VARCHAR(MAX)
)
AS
BEGIN

    DECLARE @id_evento INT;
    DECLARE @custo DECIMAL(10,2);

    BEGIN TRANSACTION;

    BEGIN TRY

        INSERT INTO DDL.Evento
        (
            id_cliente,
            id_menu,
            id_tipo_evento,
            custo,
            morada,
            codigo_postal,
            duracao,
            nr_pessoas,
            margem,
            localidade,
            data_evento
        )
        VALUES
        (
            @id_cliente,
            @id_menu,
            @id_tipo_evento,
            NULL,
            @morada,
            @codigo_postal,
            @duracao,
            @nr_pessoas,
            @margem,
            @localidade,
            @data_evento
        );

        SET @id_evento = SCOPE_IDENTITY();

        -- Associar serviços ao evento
        INSERT INTO DDL.Servico_Evento(id_servico, id_evento)
            SELECT
                CAST(value AS INT),
                @id_evento
            FROM STRING_SPLIT(@servicos, ',');

        -- Calcular custo já com os serviços associados
        SET @custo = UDF.fn_CalcularCustoEvento(@id_evento);

        SET @custo =
            @custo +
            (@custo * (@margem / 100));

        UPDATE DDL.Evento
        SET custo = @custo
        WHERE id_evento = @id_evento;

        COMMIT TRANSACTION;

    END TRY
    BEGIN CATCH

        ROLLBACK TRANSACTION;
        THROW;

    END CATCH

END;
GO

CREATE OR ALTER PROCEDURE SP.sp_AdicionarEmpregadoAEvento
(
    @id_evento INT,
    @id_empregado INT
)
AS
BEGIN

    DECLARE @duracao INT = 0;

    SET @duracao = (
        SELECT duracao 
        FROM DDL.Evento 
        WHERE id_evento = @id_evento AND isdeleted = 0
    );

    INSERT INTO DDL.Trabalha_Em (id_empregado, id_evento, duracao)
    VALUES (@id_empregado, @id_evento, @duracao + 4); 
    -- Adiciona 4 horas por cada empregado para cobrir preparação e limpeza

END;
GO

CREATE OR ALTER PROCEDURE SP.sp_AtualizarEvento
(
    @id_evento INT,
    @id_cliente INT,
    @id_menu INT,
    @id_tipo_evento INT,
    @morada VARCHAR(255),
    @codigo_postal VARCHAR(20),
    @duracao INT,
    @nr_pessoas INT,
    @margem DECIMAL(10,2),
    @localidade VARCHAR(100),
    @data_evento DATETIME,
    @servicos VARCHAR(MAX)
)
AS
BEGIN

    DECLARE @custo DECIMAL(10,2);

    BEGIN TRANSACTION;

    BEGIN TRY

        UPDATE DDL.Evento
        SET 
            id_cliente = @id_cliente,
            id_menu = @id_menu,
            id_tipo_evento = @id_tipo_evento,
            morada = @morada,
            codigo_postal = @codigo_postal,
            duracao = @duracao,
            nr_pessoas = @nr_pessoas,
            margem = @margem,
            localidade = @localidade,
            data_evento = @data_evento
        WHERE id_evento = @id_evento;

        -- Reset aos serviços (marcamos como apagados)
        UPDATE DDL.Servico_Evento 
        SET isdeleted = 1 
        WHERE id_evento = @id_evento;

        -- Associar novos serviços ao evento (ou reativar)
        IF @servicos IS NOT NULL AND LEN(@servicos) > 0
        BEGIN
            MERGE INTO DDL.Servico_Evento AS Target
            USING (SELECT CAST(value AS INT) as id_servico FROM STRING_SPLIT(@servicos, ',')) AS Source
            ON Target.id_evento = @id_evento AND Target.id_servico = Source.id_servico
            WHEN MATCHED THEN
                UPDATE SET isdeleted = 0
            WHEN NOT MATCHED THEN
                INSERT (id_evento, id_servico) VALUES (@id_evento, Source.id_servico);
        END

        -- Calcular custo já com os serviços atualizados
        SET @custo = UDF.fn_CalcularCustoEvento(@id_evento);

        SET @custo =
            @custo +
            (@custo * (@margem / 100));

        UPDATE DDL.Evento
        SET custo = @custo
        WHERE id_evento = @id_evento;

        COMMIT TRANSACTION;

    END TRY
    BEGIN CATCH

        ROLLBACK TRANSACTION;
        THROW;

    END CATCH

END;
GO

CREATE OR ALTER PROCEDURE SP.sp_NovoLote 
(
    @id_ingrediente INT,
    @id_fornecedor INT,
    @preco DECIMAL(10,2),
    @quantidade_deduzivel INT
)
AS
BEGIN
    INSERT INTO DDL.Lote
    (
        id_ingrediente,
        id_fornecedor,
        preco,
        quantidade_deduzida,
        quantidade_deduzivel
    )
    VALUES
    (
        @id_ingrediente,
        @id_fornecedor,
        @preco,
        0,
        @quantidade_deduzivel
    );

END;
GO