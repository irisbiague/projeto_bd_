from db import menus as db_menus


class MenusService:
    """Serviço de negócio para gestão de menus."""

    CATEGORIAS_CATERING = db_menus.categorias_catering

    @staticmethod
    def map_categoria_bd(designacao):
        """Mapeia uma designação de BD para a categoria de UI."""
        return db_menus.map_categoria_bd(designacao)

    @staticmethod
    def get_all_menus():
        """Retorna todos os menus com detalhes de pratos e bebidas."""
        return db_menus.get_menus()

    @staticmethod
    def get_menu_by_id(menu_id):
        """Retorna um menu específico com detalhes."""
        return db_menus.get_menu_by_id(menu_id)

    @staticmethod
    def save_menu(db, form):
        """Cria ou atualiza um menu com suas constituições."""
        return db_menus.save_menu(db, form)

    @staticmethod
    def delete_menu(db, menu_id):
        """Marca um menu como deletado."""
        return db_menus.delete_menu(db, menu_id)

    @staticmethod
    def get_all_dishes():
        """Retorna todos os pratos."""
        return db_menus.get_todos_pratos()

    @staticmethod
    def get_all_drinks():
        """Retorna todas as bebidas."""
        return db_menus.get_todas_bebidas()

    @staticmethod
    def get_categorias_catering():
        """Retorna categorias disponíveis para catering."""
        return MenusService.CATEGORIAS_CATERING

    @staticmethod
    def get_ingredientes():
        """Retorna todos os ingredientes."""
        return db_menus.get_ingredientes()
