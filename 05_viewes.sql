 -- Criar view para listar os eventos com o nome do cliente e a descrição do tipo de evento
CREATE VIEW VIEWS.V_Eventos_Detalhados
AS
SELECT E.*, 
    C.nome as cliente_nome, 
    TE.descricao as tipo_evento
FROM DDL.Evento E
    INNER JOIN DDL.Cliente C 
        ON E.id_cliente = C.id_cliente
    INNER JOIN DDL.Tipo_evento TE 
        ON E.id_tipo_evento = TE.id_tipo_evento
WHERE E.isdeleted = 0;
GO

CREATE VIEW VIEWS.V_Empregados_Evento
AS
SELECT 
    E.id_empregado, 
    E.nome, 
    FE.designacao as funcao
FROM DDL.Empregado E
    INNER JOIN DDL.Funcao_Empregado FE 
        ON E.id_funcao_empregado = FE.id_funcao_empregado
WHERE E.isdeleted = 0;
GO

CREATE VIEW VIEWS.V_Ingredientes_quantidade_custo
AS
SELECT
    I.id_ingrediente,
    I.nome,
    COALESCE(SUM(L.quantidade_deduzivel - L.quantidade_deduzida), 0) AS quantidade,
    I.unidade,
    COALESCE(SUM(L.preco * (L.quantidade_deduzivel - L.quantidade_deduzida)), 0) AS custo,
    I.data_validade
FROM DDL.Ingrediente AS I
    LEFT JOIN DDL.Lote AS L
        ON I.id_ingrediente = L.id_ingrediente
        AND L.isdeleted = 0
WHERE I.isdeleted = 0
GROUP BY
    I.id_ingrediente,
    I.nome,
    I.unidade,
    I.data_validade;
GO

CREATE VIEW VIEWS.V_Lotes_Detalhados
AS
SELECT L.id_lote, L.preco, L.quantidade_deduzivel, L.quantidade_deduzida, L.id_fornecedor, F.nome as fornecedor_nome
        FROM DDL.Lote L
        LEFT JOIN DDL.Fornecedor F ON L.id_fornecedor = F.id_fornecedor
        WHERE L.isdeleted = 0;
GO

SELECT * FROM DDL.Lote;
SELECT * FROM DDL.Ingrediente;
SELECT * FROM DDL.Fornecedor;