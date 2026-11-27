from flask import Flask
from db.database import close_db
from controllers import init_app

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'mudar-isto-para-uma-chave-secreta'

app.teardown_appcontext(close_db)
init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
