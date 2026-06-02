from .auth import auth_bp
from .dishes import dishes_bp
from .events import events_bp
from .menus import menus_bp
from .stock import stock_bp

__all__ = [
    'auth_bp',
    'dishes_bp',
    'events_bp',
    'menus_bp',
    'stock_bp',
    'init_app'
]


def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(menus_bp)
    app.register_blueprint(dishes_bp)
    app.register_blueprint(stock_bp)
