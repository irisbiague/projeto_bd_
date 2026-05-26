USE Projeto;
GO

CREATE FUNCTION UDF.fn_CalcularCustoEvento (@id_evento INT)
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

CREATE FUNCTION UDF.fn_IngredientesPorEvento (@id_evento INT)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        ev.id_evento,
        p.nome AS prato,
        i.nome AS ingrediente,
        cp.quantidade AS quantidade_necessaria
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
);