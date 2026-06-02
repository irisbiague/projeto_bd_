from db import menus as db_menus


class DishesService:
    """Serviço de negócio para gestão de pratos e bebidas."""

    @staticmethod
    def save_prato(db, prato_id, nome, receita, categoria, ingredientes=None):
        """Cria ou atualiza um prato com seus ingredientes."""
        return db_menus.save_prato(db, prato_id, nome, receita, categoria, ingredientes)

    @staticmethod
    def save_bebida(db, bebida_id, nome, receita, ingredientes=None):
        """Cria ou atualiza uma bebida com seus ingredientes."""
        return db_menus.save_bebida(db, bebida_id, nome, receita, ingredientes)

    @staticmethod
    def delete_prato(db, prato_id):
        """Marca um prato como deletado."""
        return db_menus.delete_prato(db, prato_id)

    @staticmethod
    def delete_bebida(db, bebida_id):
        """Marca uma bebida como deletada."""
        return db_menus.delete_bebida(db, bebida_id)

    @staticmethod
    def get_prato_details(prato_id):
        """Retorna detalhes de um prato com ingredientes."""
        return db_menus.get_prato_details(prato_id)

    @staticmethod
    def get_bebida_details(bebida_id):
        """Retorna detalhes de uma bebida com ingredientes."""
        return db_menus.get_bebida_details(bebida_id)
