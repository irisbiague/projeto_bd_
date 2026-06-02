import pyodbc
from flask import Blueprint, redirect, render_template, request, session, url_for
from db.database import SQL_SERVER_CONFIG, set_db_config, build_connection_string, init_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.before_app_request
def ensure_db():
    if request.endpoint in ('auth.login', 'static', 'auth.logout'):
        return
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    init_db()


@auth_bp.route('/', endpoint='home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return redirect(url_for('events.create_event'))


@auth_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    message = None
    form = {
        'driver': SQL_SERVER_CONFIG['driver'],
        'server': SQL_SERVER_CONFIG['server'],
        'database': SQL_SERVER_CONFIG['database'],
        'trusted_connection': 'yes',
        'username': '',
        'password': ''
    }

    if request.method == 'POST':
        form = {
            'driver': request.form.get('driver', SQL_SERVER_CONFIG['driver']).strip(),
            'server': request.form.get('server', SQL_SERVER_CONFIG['server']).strip(),
            'database': request.form.get('database', SQL_SERVER_CONFIG['database']).strip(),
            'trusted_connection': request.form.get('trusted_connection', 'yes'),
            'username': request.form.get('username', '').strip(),
            'password': request.form.get('password', '').strip()
        }

        if not form['server'] or not form['database']:
            message = 'Servidor e base de dados são obrigatórios.'
        else:
            config = {
                'driver': form['driver'] or SQL_SERVER_CONFIG['driver'],
                'server': form['server'],
                'database': form['database'],
                'trusted_connection': form['trusted_connection']
            }
            if config['trusted_connection'].lower() not in ('yes', 'true', 'sspi'):
                config['username'] = form['username']
                config['password'] = form['password']

            try:
                test_conn = pyodbc.connect(build_connection_string(config), autocommit=False)
                test_conn.close()
                set_db_config(config)
                session['logged_in'] = True
                return redirect(url_for('events.create_event'))
            except pyodbc.Error as error:
                message = f'Não foi possível conectar: {error}'

    return render_template('login.html', message=message, form=form)


@auth_bp.route('/logout', endpoint='logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
