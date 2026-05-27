USE Projeto;
GO

CREATE OR ALTER FUNCTION UDF.fn_CalcularCustoEvento (@id_evento INT)
RETURNS DECIMAL(10,2)
AS
BEGIN

    DECLARE @custoIngredientes DECIMAL(10,2)
    DECLARE @custoEmpregados DECIMAL(10,2)
    DECLARE @custoServicos DECIMAL(10,2)
    DECLARE @nrPessoas INT
    DECLARE @total DECIMAL(10,2)
	  
    SELECT @nrPessoas = nr_pessoas
    FROM DDL.Evento
    WHERE id_evento = @id_evento

   SELECT 
        @custoIngredientes = SUM(
            (cp.quantidade * @nrPessoas) * 
            (i.custo / NULLIF(i.quantidade,0))
        )
    FROM DDL.Evento ev
    INNER JOIN DDL.Menu m
        ON ev.id_menu = m.id_menu
    INNER JOIN DDL.Constituicao_Menu_Pratos cmp
        ON m.id_menu = cmp.id_menu
    INNER JOIN DDL.Constituicao_Prato cp
        ON cmp.id_prato = cp.id_prato
    INNER JOIN DDL.Ingrediente i
        ON cp.id_ingrediente = i.id_ingrediente
    WHERE ev.id_evento = @id_evento  

    SELECT 
        @custoEmpregados = SUM(
            e.preco_hora * te.duracao
        )
    FROM DDL.Trabalha_Em te
    INNER JOIN DDL.Empregado e
        ON te.id_empregado = e.id_empregado
    WHERE te.id_evento = @id_evento
	
    SELECT 
        @custoServicos = SUM(s.custo)
    FROM DDL.Servico_Evento se
    INNER JOIN DDL.Servico s
        ON se.id_servico = s.id_servico
    WHERE se.id_evento = @id_evento

   SET @total =
        ISNULL(@custoIngredientes,0) +
        ISNULL(@custoEmpregados,0) +
        ISNULL(@custoServicos,0)

    RETURN @total

END;
GO

CREATE OR ALTER FUNCTION UDF.fn_IngredientesPorEvento (@id_evento INT)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        ev.id_evento,
        p.nome AS item_menu,
        i.nome AS ingrediente,
        (cp.quantidade * ISNULL(ev.nr_pessoas, 1)) AS quantidade_necessaria
    FROM DDL.Evento ev
    INNER JOIN DDL.Menu m 
        ON ev.id_menu = m.id_menu
    INNER JOIN DDL.Constituicao_Menu_Pratos cmp 
        ON m.id_menu = cmp.id_menu
    INNER JOIN DDL.Prato p 
        ON cmp.id_prato = p.id_prato
    INNER JOIN DDL.Constituicao_Prato cp 
        ON p.id_prato = cp.id_prato
    INNER JOIN DDL.Ingrediente i 
        ON cp.id_ingrediente = i.id_ingrediente
    WHERE ev.id_evento = @id_evento

    UNION ALL

    SELECT 
        ev.id_evento,
        b.nome AS item_menu,
        i.nome AS ingrediente,
        (cb.quantidade * ISNULL(ev.nr_pessoas, 1)) AS quantidade_necessaria
    FROM DDL.Evento ev
    INNER JOIN DDL.Menu m 
        ON ev.id_menu = m.id_menu
    INNER JOIN DDL.Constituicao_Menu_Bebidas cmb 
        ON m.id_menu = cmb.id_menu
    INNER JOIN DDL.Bebida b 
        ON cmb.id_bebida = b.id_bebida
    INNER JOIN DDL.Constituicao_Bebida cb 
        ON b.id_bebida = cb.id_bebida
    INNER JOIN DDL.Ingrediente i 
        ON cb.id_ingrediente = i.id_ingrediente
    WHERE ev.id_evento = @id_evento
);
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
    SELECT V.* FROM VIEWS.V_Empregados_Evento V
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
