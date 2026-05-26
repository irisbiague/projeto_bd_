CREATE TRIGGER DDL.trg_ImpedirDeleteIngrediente
ON DDL.Ingrediente
INSTEAD OF DELETE
AS
BEGIN
    
    IF EXISTS
    (
        SELECT *
        FROM DDL.Lote l
        INNER JOIN deleted d
            ON l.id_ingrediente = d.id_ingrediente
        WHERE l.quantidade_deduzida < l.quantidade_deduzivel
    )
    BEGIN
        RAISERROR(
            'N�o � poss�vel eliminar o ingrediente porque ainda existem lotes por consumir.',
            16,
            1
        )

        RETURN
    END
    
    UPDATE DDL.Ingrediente
	SET isdeleted = 1
    WHERE id_ingrediente IN
    (
        SELECT id_ingrediente
        FROM deleted
    )

END;
GO

CREATE TRIGGER DDL.trg_SoftDeleteMenu
ON DDL.Menu
INSTEAD OF DELETE
AS
BEGIN

    -- Soft delete do menu
    UPDATE DDL.Menu
    SET isDeleted = 1
    WHERE id_menu IN (
        SELECT id_menu
        FROM deleted
    );

    -- Soft delete das ligações menu-prato
    UPDATE DDL.Constituicao_Menu_Pratos
    SET isDeleted = 1
    WHERE id_menu IN (
        SELECT id_menu
        FROM deleted
    );

END;
GO

CREATE TRIGGER DDL.trg_SoftDeletePrato
ON DDL.Prato
INSTEAD OF DELETE
AS
BEGIN   

    -- Soft delete do prato
    UPDATE DDL.Prato
    SET isDeleted = 1
    WHERE id_prato IN (
        SELECT id_prato
        FROM deleted
    );

    -- Soft delete das ligações prato-ingrediente
    UPDATE DDL.Constituicao_Prato
    SET isDeleted = 1
    WHERE id_prato IN (
        SELECT id_prato
        FROM deleted
    );

END;
GO

CREATE TRIGGER DDL.trg_DeleteServico
ON DDL.Servico
INSTEAD OF DELETE
AS
BEGIN   

    -- Soft delete do serviço
    UPDATE DDL.Servico
    SET isDeleted = 1
    WHERE id_servico IN (
        SELECT id_servico
        FROM deleted
    );  

    UPDATE DDL.Servico_Interno
    SET isDeleted = 1
    WHERE id_servico IN (
        SELECT id_servico
        FROM deleted
    ); 

    UPDATE DDL.Servico_Externo
    SET isDeleted = 1
    WHERE id_servico IN (
        SELECT id_servico
        FROM deleted
    );  

END;