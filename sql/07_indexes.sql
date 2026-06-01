-- ==========================================
-- 07_indexes.sql
-- Script de Otimização de Performance (Índices)
-- ==========================================

USE Projeto;
GO

-- ============================================================================
-- A. Índices em Chaves Estrangeiras muito utilizadas (Non-Clustered)
-- O SQL Server não indexa FKs por defeito. Como a aplicação faz imensos JOINs 
-- entre estas tabelas, indexar as FKs mais pesadas aumenta imenso a performance.
-- ============================================================================
CREATE NONCLUSTERED INDEX IX_Evento_Cliente ON DDL.Evento(id_cliente);
CREATE NONCLUSTERED INDEX IX_Evento_Menu ON DDL.Evento(id_menu);
CREATE NONCLUSTERED INDEX IX_Evento_TipoEvento ON DDL.Evento(id_tipo_evento);

CREATE NONCLUSTERED INDEX IX_Lote_Fornecedor ON DDL.Lote(id_fornecedor);
CREATE NONCLUSTERED INDEX IX_Ingrediente_Fornecedor ON DDL.Ingrediente(id_fornecedor);

CREATE NONCLUSTERED INDEX IX_Empregado_Funcao ON DDL.Empregado(id_funcao_empregado);

-- ============================================================================
-- B. Índices para pesquisas frequentes (Non-Clustered)
-- Para acelerar a pesquisa textual de nomes na Interface de Utilizador (UI).
-- ============================================================================
CREATE NONCLUSTERED INDEX IX_Cliente_Nome ON DDL.Cliente(nome);
CREATE NONCLUSTERED INDEX IX_Empregado_Nome ON DDL.Empregado(nome);
CREATE NONCLUSTERED INDEX IX_Fornecedor_Nome ON DDL.Fornecedor(nome);

-- ============================================================================
-- C. Filtered Indexes (Otimização para o Soft-Delete)
-- Poupa espaço de armazenamento indexando apenas os registos "ativos" (isdeleted=0)
-- e torna as queries da aplicação aos dados "vivos" incrivelmente rápidas.
-- ============================================================================
CREATE NONCLUSTERED INDEX IX_Prato_Ativos ON DDL.Prato(nome) WHERE isdeleted = 0;
CREATE NONCLUSTERED INDEX IX_Bebida_Ativos ON DDL.Bebida(nome) WHERE isdeleted = 0;
CREATE NONCLUSTERED INDEX IX_Ingrediente_Ativos ON DDL.Ingrediente(nome) WHERE isdeleted = 0;
CREATE NONCLUSTERED INDEX IX_Evento_Ativos ON DDL.Evento(id_evento) WHERE isdeleted = 0;

-- ============================================================================
-- D. Clustered Index Estratégico na Tabela Evento
-- A Primary Key (id_evento) foi definida como NONCLUSTERED no script 01_ddl.sql.
-- O Clustered Index dita a forma como os dados são guardados fisicamente no disco.
-- Como as listas de eventos na app real são quase sempre puxadas por intervalo 
-- de datas (ex: "eventos desta semana"), ter os dados ordenados pela data 
-- torna os range scans super eficientes!
-- ============================================================================
CREATE CLUSTERED INDEX CIX_Evento_DataEvento ON DDL.Evento(data_evento);
GO
