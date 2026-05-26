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


