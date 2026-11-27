# -*- coding: utf-8 -*-
import json
import pyodbc
from datetime import date, datetime
from flask import Flask, g, redirect, render_template, request, session, url_for

# Configurações do SQL Server
SQL_SERVER_CONFIG = {
    'driver': '{ODBC Driver 18 for SQL Server}',
    'server': '.\\SQLEXPRESS',
    'database': 'Projeto',
    'trusted_connection': 'yes',
}

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'mudar-isto-para-uma-chave-secreta'
CURRENT_SQL_SERVER_CONFIG = SQL_SERVER_CONFIG.copy()

categorias_catering = [
    {'id': 'entradas', 'titulo': 'Entradas e Aperitivos', 'placeholderNome': 'Ex: Tábua de Queijos...'},
    {'id': 'pratoPrincipal', 'titulo': 'Prato Principal', 'placeholderNome': 'Ex: Lombo Assado...'},
    {'id': 'acompanhamentos', 'titulo': 'Acompanhamentos', 'placeholderNome': 'Ex: Arroz Árabe...'},
    {'id': 'sobremesa', 'titulo': 'Sobremesa', 'placeholderNome': 'Ex: Buffet de Doces...'},
    {'id': 'bebidas', 'titulo': 'Serviço de Bebidas', 'placeholderNome': 'Ex: Vinhos do Douro...'},
    {'id': 'ceia', 'titulo': 'Ceia / Snacks Extra', 'placeholderNome': 'Ex: Caldo Verde...'}
]

servicos_list = [
    ('bar', 'Serviço de Bar Aberto'),
    ('limpeza', 'Equipa de Limpeza'),
    ('staff', 'Staff de Bengaleiro'),
    ('decoracao', 'Decoração e Cenografia'),
    ('som_luz', 'Som e Iluminação'),
    ('fotografia', 'Fotografia e Vídeo'),
    ('seguranca', 'Segurança de Evento'),
    ('transporte', 'Transporte de Convidados')
]

tipos_evento = {
    'casamento': {'label': 'Casamento', 'emoji': '💍', 'corFundo': '#FDF2F8', 'corBorda': '#FBCFE8', 'corTexto': '#9D174D'},
    'batizado': {'label': 'Batizado', 'emoji': '🕊️', 'corFundo': '#F0FDF4', 'corBorda': '#BBF7D0', 'corTexto': '#166534'},
    'corporate': {'label': 'Corporate / Empresa', 'emoji': '💼', 'corFundo': '#EFF6FF', 'corBorda': '#BFDBFE', 'corTexto': '#1E3A8A'},
    'jantar': {'label': 'Jantar / Festa', 'emoji': '🥂', 'corFundo': '#FFFBEB', 'corBorda': '#FEF08A', 'corTexto': '#854D0E'}
}

dias_da_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
meses_do_ano = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


def build_connection_string(config):
    driver = config['driver']
    server = config['server']
    database = config['database']
    if config.get('trusted_connection', 'no').lower() in ('yes', 'true', 'sspi'):
        return f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;"

    username = config['username']
    password = config['password']
    return f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"


def get_db_config():
    return CURRENT_SQL_SERVER_CONFIG


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        connection_string = build_connection_string(get_db_config())
        db = pyodbc.connect(connection_string, autocommit=False)
        g.db = db
    return db


def close_db(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_one(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def init_db():
    db = get_db()
    db.execute(
        '''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'menus')
        BEGIN
            CREATE TABLE menus (
                id INT IDENTITY(1,1) PRIMARY KEY,
                nome NVARCHAR(255),
                entradas_nome NVARCHAR(255),
                entradas_ingredientes NVARCHAR(MAX),
                pratoPrincipal_nome NVARCHAR(255),
                pratoPrincipal_ingredientes NVARCHAR(MAX),
                acompanhamentos_nome NVARCHAR(255),
                acompanhamentos_ingredientes NVARCHAR(MAX),
                sobremesa_nome NVARCHAR(255),
                sobremesa_ingredientes NVARCHAR(MAX),
                bebidas_nome NVARCHAR(255),
                bebidas_ingredientes NVARCHAR(MAX),
                ceia_nome NVARCHAR(255),
                ceia_ingredientes NVARCHAR(MAX)
            );
        END
        '''
    )
    db.execute(
        '''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'events')
        BEGIN
            CREATE TABLE events (
                id INT IDENTITY(1,1) PRIMARY KEY,
                cliente NVARCHAR(255),
                titulo NVARCHAR(255),
                tipo NVARCHAR(100),
                data NVARCHAR(50),
                pessoas INT,
                local NVARCHAR(255),
                menu_id INT NULL,
                servicos NVARCHAR(MAX),
                created_at DATETIME2
            );
        END
        '''
    )
    db.execute(
        '''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'stock_items')
        BEGIN
            CREATE TABLE stock_items (
                id INT IDENTITY(1,1) PRIMARY KEY,
                produto NVARCHAR(255),
                quantidade INT,
                localizacao NVARCHAR(255),
                status NVARCHAR(100),
                notas NVARCHAR(MAX),
                updated_at DATETIME2
            );
        END
        '''
    )
    db.commit()


app.teardown_appcontext(close_db)


@app.before_request
def ensure_db():
    if request.endpoint in ('login', 'static', 'logout'):
        return
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    init_db()


def row_to_menu(row):
    return {
        'id': row['id'],
        'nome': row['nome'],
        'entradas': {'nome': row['entradas_nome'] or '', 'ingredientes': row['entradas_ingredientes'] or ''},
        'pratoPrincipal': {'nome': row['pratoPrincipal_nome'] or '', 'ingredientes': row['pratoPrincipal_ingredientes'] or ''},
        'acompanhamentos': {'nome': row['acompanhamentos_nome'] or '', 'ingredientes': row['acompanhamentos_ingredientes'] or ''},
        'sobremesa': {'nome': row['sobremesa_nome'] or '', 'ingredientes': row['sobremesa_ingredientes'] or ''},
        'bebidas': {'nome': row['bebidas_nome'] or '', 'ingredientes': row['bebidas_ingredientes'] or ''},
        'ceia': {'nome': row['ceia_nome'] or '', 'ingredientes': row['ceia_ingredientes'] or ''}
    }


def row_to_event(row):
    return {
        'id': row['id'],
        'cliente': row['cliente'],
        'titulo': row['titulo'] or '',
        'tipo': row['tipo'] or 'corporate',
        'data': row['data'],
        'pessoas': row['pessoas'],
        'local': row['local'],
        'menuId': row['menu_id'],
        'servicos': json.loads(row['servicos'] or '[]'),
        'createdAt': row['created_at']
    }


def row_to_stock(row):
    return {
        'id': row['id'],
        'produto': row['produto'],
        'quantidade': row['quantidade'],
        'localizacao': row['localizacao'],
        'status': row['status'],
        'notas': row['notas'],
        'updatedAt': row['updated_at']
    }


def get_menus():
    db = get_db()
    cursor = db.execute('SELECT * FROM menus ORDER BY id DESC')
    return [row_to_menu(row) for row in fetch_all(cursor)]


def get_menu_by_id(menu_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM menus WHERE id = ?', (menu_id,))
    row = fetch_one(cursor)
    return row_to_menu(row) if row else None


def get_events():
    db = get_db()
    cursor = db.execute('SELECT * FROM Evento ORDER BY id DESC')
    return [row_to_event(row) for row in fetch_all(cursor)]


def get_stock_items():
    db = get_db()
    cursor = db.execute('SELECT * FROM stock_items ORDER BY id DESC')
    return [row_to_stock(row) for row in fetch_all(cursor)]


def get_stock_item(item_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM stock_items WHERE id = ?', (item_id,))
    row = fetch_one(cursor)
    return row_to_stock(row) if row else None


def get_event_by_id(event_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM Evento WHERE id_evento = ?', (event_id,))
    row = fetch_one(cursor)
    return row_to_event(row) if row else None


def previous_month(year, month):
    if month == 1:
        return year - 1, 12
    return year, month - 1


def next_month(year, month):
    if month == 12:
        return year + 1, 1
    return year, month + 1


def make_calendar(year, month, events):
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1)
    else:
        last_day = date(year, month + 1, 1)
    total_days = (last_day - first_day).days
    empty_cells = first_day.weekday() + 1
    if empty_cells == 7:
        empty_cells = 0

    events_by_day = {}
    for event in events:
        if not event['data']:
            continue
        try:
            event_date = datetime.fromisoformat(event['data']).date()
        except ValueError:
            continue
        if event_date.year == year and event_date.month == month:
            events_by_day.setdefault(event_date.day, []).append(event)

    return {
        'dias_do_mes': list(range(1, total_days + 1)),
        'empty_cells': list(range(empty_cells)),
        'events_by_day': events_by_day
    }


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('create_event'))


@app.route('/login', methods=['GET', 'POST'])
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
                global CURRENT_SQL_SERVER_CONFIG
                CURRENT_SQL_SERVER_CONFIG = config
                session['logged_in'] = True
                return redirect(url_for('create_event'))
            except pyodbc.Error as error:
                message = f'Não foi possível conectar: {error}'

    return render_template('login.html', message=message, form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    message = None
    editing_event = None
    form = {
        'titulo': '',
        'tipo': 'corporate',
        'cliente': '',
        'data': '',
        'pessoas': '',
        'local': '',
        'menu_id': '',
        'servicos': []
    }

    if request.method == 'POST':
        form = {
            'titulo': request.form.get('titulo', '').strip(),
            'tipo': request.form.get('tipo', 'corporate'),
            'cliente': request.form.get('cliente', '').strip(),
            'data': request.form.get('data', '').strip(),
            'pessoas': request.form.get('pessoas', '').strip(),
            'local': request.form.get('local', '').strip(),
            'menu_id': request.form.get('menu_id', '').strip(),
            'servicos': request.form.getlist('servicos')
        }
        event_id = request.form.get('event_id')

        if not form['titulo'] or not form['cliente'] or not form['data'] or not form['local']:
            message = 'Por favor, preencha o nome do evento, cliente, data e local.'
        else:
            db = get_db()
            if event_id and event_id.isdigit():
                db.execute(
                    '''
                    UPDATE events
                    SET cliente = ?, titulo = ?, tipo = ?, data = ?, pessoas = ?, local = ?, menu_id = ?, servicos = ?
                    WHERE id = ?
                    ''',
                    (
                        form['cliente'],
                        form['titulo'],
                        form['tipo'],
                        form['data'],
                        int(form['pessoas']) if form['pessoas'].isdigit() else 0,
                        form['local'],
                        int(form['menu_id']) if form['menu_id'].isdigit() else None,
                        json.dumps(form['servicos'], ensure_ascii=False),
                        int(event_id)
                    )
                )
                get_db().commit()
                return redirect(url_for('create_event', success=1))
            else:
                db.execute(
                    '''
                    INSERT INTO events (cliente, titulo, tipo, data, pessoas, local, menu_id, servicos, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        form['cliente'],
                        form['titulo'],
                        form['tipo'],
                        form['data'],
                        int(form['pessoas']) if form['pessoas'].isdigit() else 0,
                        form['local'],
                        int(form['menu_id']) if form['menu_id'].isdigit() else None,
                        json.dumps(form['servicos'], ensure_ascii=False),
                        datetime.utcnow().isoformat()
                    )
                )
                get_db().commit()
                return redirect(url_for('create_event', success=1))

    else:
        edit_id = request.args.get('edit_id')
        if edit_id and edit_id.isdigit():
            editing_event = get_event_by_id(int(edit_id))
            if editing_event:
                form = {
                    'titulo': editing_event['titulo'],
                    'tipo': editing_event['tipo'],
                    'cliente': editing_event['cliente'],
                    'data': editing_event['data'],
                    'pessoas': str(editing_event['pessoas'] or ''),
                    'local': editing_event['local'],
                    'menu_id': str(editing_event['menuId']) if editing_event['menuId'] else '',
                    'servicos': editing_event['servicos'] or []
                }

    if request.args.get('success'):
        message = 'Evento guardado com sucesso!'

    menus = get_menus()
    selected_menu = get_menu_by_id(int(form['menu_id'])) if form['menu_id'].isdigit() else None

    return render_template(
        'index.html',
        active_page='create_event',
        message=message,
        form=form,
        menus=menus,
        selected_menu=selected_menu,
        categorias_catering=categorias_catering,
        servicos_list=servicos_list,
        tipos_evento=tipos_evento,
        editing_event=editing_event
    )


@app.route('/manage-menus', methods=['GET', 'POST'])
def manage_menus():
    message = None
    editing_menu = None
    form = {'menu_id': '', 'menu_name': ''}
    for cat in categorias_catering:
        form[cat['id']] = {'nome': '', 'ingredientes': ''}

    if request.method == 'POST':
        form['menu_id'] = request.form.get('menu_id', '').strip()
        form['menu_name'] = request.form.get('menu_name', '').strip()
        for cat in categorias_catering:
            form[cat['id']]['nome'] = request.form.get(f"{cat['id']}_nome", '').strip()
            form[cat['id']]['ingredientes'] = request.form.get(f"{cat['id']}_ingredientes", '').strip()

        if not form['menu_name']:
            message = 'Por favor, indique um nome para o menu.'
        else:
            db = get_db()
            if form['menu_id'] and form['menu_id'].isdigit():
                db.execute(
                    '''
                    UPDATE menus SET
                        nome = ?,
                        entradas_nome = ?,
                        entradas_ingredientes = ?,
                        pratoPrincipal_nome = ?,
                        pratoPrincipal_ingredientes = ?,
                        acompanhamentos_nome = ?,
                        acompanhamentos_ingredientes = ?,
                        sobremesa_nome = ?,
                        sobremesa_ingredientes = ?,
                        bebidas_nome = ?,
                        bebidas_ingredientes = ?,
                        ceia_nome = ?,
                        ceia_ingredientes = ?
                    WHERE id = ?
                    ''',
                    (
                        form['menu_name'],
                        form['entradas']['nome'],
                        form['entradas']['ingredientes'],
                        form['pratoPrincipal']['nome'],
                        form['pratoPrincipal']['ingredientes'],
                        form['acompanhamentos']['nome'],
                        form['acompanhamentos']['ingredientes'],
                        form['sobremesa']['nome'],
                        form['sobremesa']['ingredientes'],
                        form['bebidas']['nome'],
                        form['bebidas']['ingredientes'],
                        form['ceia']['nome'],
                        form['ceia']['ingredientes'],
                        int(form['menu_id'])
                    )
                )
            else:
                db.execute(
                    '''
                    INSERT INTO menus (
                        nome,
                        entradas_nome,
                        entradas_ingredientes,
                        pratoPrincipal_nome,
                        pratoPrincipal_ingredientes,
                        acompanhamentos_nome,
                        acompanhamentos_ingredientes,
                        sobremesa_nome,
                        sobremesa_ingredientes,
                        bebidas_nome,
                        bebidas_ingredientes,
                        ceia_nome,
                        ceia_ingredientes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        form['menu_name'],
                        form['entradas']['nome'],
                        form['entradas']['ingredientes'],
                        form['pratoPrincipal']['nome'],
                        form['pratoPrincipal']['ingredientes'],
                        form['acompanhamentos']['nome'],
                        form['acompanhamentos']['ingredientes'],
                        form['sobremesa']['nome'],
                        form['sobremesa']['ingredientes'],
                        form['bebidas']['nome'],
                        form['bebidas']['ingredientes'],
                        form['ceia']['nome'],
                        form['ceia']['ingredientes']
                    )
                )
            get_db().commit()
            return redirect(url_for('manage_menus', success=1))

    else:
        edit_id = request.args.get('edit_id')
        if edit_id and edit_id.isdigit():
            editing_menu = get_menu_by_id(int(edit_id))
            if editing_menu:
                form = {
                    'menu_id': str(editing_menu['id']),
                    'menu_name': editing_menu['nome']
                }
                for cat in categorias_catering:
                    form[cat['id']] = {
                        'nome': editing_menu[cat['id']]['nome'],
                        'ingredientes': editing_menu[cat['id']]['ingredientes']
                    }

    if request.args.get('success'):
        message = 'Menu guardado com sucesso!'

    menus = get_menus()
    return render_template(
        'manage_menus.html',
        active_page='manage_menus',
        message=message,
        form=form,
        menus=menus,
        categorias_catering=categorias_catering,
        editing_menu=editing_menu
    )


@app.route('/events')
def events():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    today = date.today()
    if not year:
        year = today.year
    if not month:
        month = today.month
    if month < 1:
        year, month = previous_month(year, month)
    if month > 12:
        year, month = next_month(year, month)

    all_events = get_events()
    result = make_calendar(year, month, all_events)
    events_of_month = []
    for event in all_events:
        if not event['data']:
            continue
        try:
            event_date = datetime.fromisoformat(event['data']).date()
        except ValueError:
            continue
        if event_date.year == year and event_date.month == month:
            events_of_month.append(event)

    prev_year, prev_month = previous_month(year, month)
    next_year, next_month_value = next_month(year, month)

    return render_template(
        'events.html',
        active_page='events',
        message=None,
        dias_da_semana=dias_da_semana,
        dias_do_mes=result['dias_do_mes'],
        empty_cells=result['empty_cells'],
        events_by_day=result['events_by_day'],
        events_of_month=events_of_month,
        month_name=meses_do_ano[month - 1],        month=month,        year=year,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month_value,
        tipos_evento=tipos_evento
    )


@app.route('/events/day/<int:year>/<int:month>/<int:day>')
def events_by_day(year, month, day):
    events = []
    for event in get_events():
        if not event['data']:
            continue
        try:
            event_date = datetime.fromisoformat(event['data']).date()
        except ValueError:
            continue
        if event_date.year == year and event_date.month == month and event_date.day == day:
            events.append(event)

    return render_template(
        'day_events.html',
        active_page='events',
        year=year,
        month=month,
        day=day,
        events=events,
        month_name=meses_do_ano[month - 1],
        tipos_evento=tipos_evento
    )


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    message = None
    form = {
        'produto': '',
        'quantidade': '',
        'localizacao': '',
        'status': 'Em Stock',
        'notas': ''
    }
    editing_item = None

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        form['produto'] = request.form.get('produto', '').strip()
        form['quantidade'] = request.form.get('quantidade', '').strip()
        form['localizacao'] = request.form.get('localizacao', '').strip()
        form['status'] = request.form.get('status', 'Em Stock')
        form['notas'] = request.form.get('notas', '').strip()

        if not form['produto']:
            message = 'Por favor, indique o nome do produto.'
        else:
            db = get_db()
            if item_id and item_id.isdigit():
                db.execute(
                    '''
                    UPDATE stock_items
                    SET produto = ?, quantidade = ?, localizacao = ?, status = ?, notas = ?, updated_at = ?
                    WHERE id = ?
                    ''',
                    (
                        form['produto'],
                        int(form['quantidade']) if form['quantidade'].isdigit() else 0,
                        form['localizacao'],
                        form['status'],
                        form['notas'],
                        datetime.utcnow().isoformat(),
                        int(item_id)
                    )
                )
            else:
                db.execute(
                    '''
                    INSERT INTO stock_items (produto, quantidade, localizacao, status, notas, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        form['produto'],
                        int(form['quantidade']) if form['quantidade'].isdigit() else 0,
                        form['localizacao'],
                        form['status'],
                        form['notas'],
                        datetime.utcnow().isoformat()
                    )
                )
            get_db().commit()
            return redirect(url_for('stock', success=1))

    edit_id = request.args.get('edit_id')
    if edit_id and edit_id.isdigit():
        editing_item = get_stock_item(int(edit_id))
        if editing_item:
            form = {
                'produto': editing_item['produto'],
                'quantidade': editing_item['quantidade'],
                'localizacao': editing_item['localizacao'],
                'status': editing_item['status'],
                'notas': editing_item['notas']
            }

    if request.args.get('success'):
        message = 'Stock atualizado com sucesso!'

    stock_items = get_stock_items()
    return render_template(
        'stock.html',
        active_page='stock',
        message=message,
        stock_items=stock_items,
        stock_form=form,
        editing_item=editing_item
    )


@app.route('/stock/delete/<int:item_id>', methods=['POST'])
def delete_stock(item_id):
    db = get_db()
    db.execute('DELETE FROM stock_items WHERE id = ?', (item_id,))
    db.commit()
    return redirect(url_for('stock', success=1))


@app.route('/menus/delete/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    db = get_db()
    db.execute('DELETE FROM menus WHERE id = ?', (menu_id,))
    db.commit()
    return redirect(url_for('manage_menus', success=1))


@app.route('/events/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    db = get_db()
    db.execute('DELETE FROM events WHERE id = ?', (event_id,))
    db.commit()
    return redirect(url_for('events'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
