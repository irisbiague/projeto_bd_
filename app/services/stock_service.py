from db import stock as db_stock


class StockService:
    """Serviço de negócio para gestão de stock."""

    @staticmethod
    def get_all_stock_items():
        """Retorna todos os itens de stock."""
        return db_stock.get_stock_items()

    @staticmethod
    def get_stock_item(item_id):
        """Retorna um item específico de stock."""
        return db_stock.get_stock_item(item_id)

    @staticmethod
    def get_fornecedores():
        """Retorna lista de fornecedores."""
        return db_stock.get_fornecedores()

    @staticmethod
    def save_stock_item(db, form):
        """Cria um novo item de stock com lote inicial."""
        return db_stock.save_stock_item(db, form)

    @staticmethod
    def update_stock_item(db, item_id, form):
        """Atualiza um item de stock existente."""
        return db_stock.update_stock_item(db, item_id, form)

    @staticmethod
    def delete_stock_item(db, item_id):
        """Marca um item de stock como deletado."""
        return db_stock.delete_stock_item(db, item_id)

    @staticmethod
    def add_lote(db, ingredient_id, fornecedor_id, preco, quantidade_deduzivel):
        """Adiciona um novo lote a um ingrediente."""
        return db_stock.add_lote_item(db, ingredient_id, fornecedor_id, preco, quantidade_deduzivel)

    @staticmethod
    def update_lote(db, id_lote, fornecedor_id, preco, quantidade_deduzivel, quantidade_deduzida=0):
        """Atualiza um lote existente."""
        return db_stock.edit_lote_item(db, id_lote, fornecedor_id, preco, quantidade_deduzivel, quantidade_deduzida)

    @staticmethod
    def delete_lote(db, id_lote):
        """Marca um lote como deletado."""
        return db_stock.delete_lote_item(db, id_lote)

    @staticmethod
    def get_stock_lotes(ingredient_id):
        """Retorna todos os lotes de um ingrediente."""
        return db_stock.stock_lotes(ingredient_id)

    @staticmethod
    def get_ingredientes():
        """Retorna todos os ingredientes."""
        return db_stock.get_stock_items()

