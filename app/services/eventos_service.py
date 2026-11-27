from db import eventos as db_eventos


class EventosService:
    """Serviço de negócio para gestão de eventos."""

    @staticmethod
    def get_all_events():
        """Retorna todos os eventos com detalhes formatados."""
        return db_eventos.get_events()

    @staticmethod
    def get_event_by_id(event_id):
        """Retorna um evento específico com todos os detalhes."""
        return db_eventos.get_event_by_id(event_id)

    @staticmethod
    def get_tipos_evento():
        """Retorna todos os tipos de evento com configurações de UI."""
        return db_eventos.get_tipos_evento()

    @staticmethod
    def get_servicos():
        """Retorna lista de serviços disponíveis."""
        return db_eventos.get_servicos()

    @staticmethod
    def get_empregados():
        """Retorna lista de empregados para eventos."""
        return db_eventos.get_empregados()

    @staticmethod
    def save_event(db, form, event_id=None):
        """Cria ou atualiza um evento."""
        return db_eventos.save_evento(db, form, event_id)

    @staticmethod
    def delete_event(db, event_id):
        """Deleta um evento."""
        return db_eventos.delete_evento(db, event_id)

    @staticmethod
    def get_event_inventory(event_id):
        """Retorna o inventário necessário para um evento."""
        return db_eventos.get_event_inventory(event_id)

    @staticmethod
    def get_or_create_cliente(db, nome, nif, tipo, cp, localidade):
        """Obtém ou cria um cliente."""
        return db_eventos.get_or_create_cliente(db, nome, nif, tipo, cp, localidade)

    @staticmethod
    def get_or_create_tipo_evento(db, descricao):
        """Obtém ou cria um tipo de evento."""
        return db_eventos.get_or_create_tipo_evento(db, descricao)

    @staticmethod
    def get_or_create_servico(db, descricao):
        """Obtém ou cria um serviço."""
        return db_eventos.get_or_create_servico(db, descricao)
