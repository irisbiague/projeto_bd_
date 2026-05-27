USE Projeto;
GO

CREATE PROCEDURE SP.sp_AdicionarEvento
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

CREATE PROCEDURE SP.sp_AdicionarEmpregadoAEvento
(
    @id_evento INT,
    @id_empregado INT
)
AS
BEGIN

    INSERT INTO DDL.Trabalha_Em (id_empregado, id_evento, duracao)
    VALUES (@id_empregado, @id_evento, 0);

END;
GO

CREATE PROCEDURE SP.sp_AtualizarEvento
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

CREATE PROCEDURE SP.sp_NovoLote 
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