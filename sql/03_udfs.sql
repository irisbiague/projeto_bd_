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
