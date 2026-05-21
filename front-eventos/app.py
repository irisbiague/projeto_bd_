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

categorias_catering = [
    {'id': 'entradas', 'titulo': 'Entradas e Aperitivos', 'placeholderNome': 'Ex: Tábua de Queijos...'},
    {'id': 'pratoPrincipal', 'titulo': 'Prato Principal', 'placeholderNome': 'Ex: Lombo Assado...'},
    {'id': 'acompanhamentos', 'titulo': 'Acompanhamentos', 'placeholderNome': 'Ex: Arroz Árabe...'},
    {'id': 'sobremesa', 'titulo': 'Sobremesa', 'placeholderNome': 'Ex: Buffet de Doces...'},
    {'id': 'bebidas', 'titulo': 'Serviço de Bebidas', 'placeholderNome': 'Ex: Vinhos do Douro...'},
    {'id': 'ceia', 'titulo': 'Ceia / Snacks Extra', 'placeholderNome': 'Ex: Caldo Verde...'}
]

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
    pass


app.teardown_appcontext(close_db)


@app.before_request
def ensure_db():
    if request.endpoint in ('login', 'static', 'logout'):
        return
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    init_db()


def get_or_create_tipo_prato(db, designacao):
    cursor = db.execute('SELECT id_tipo_prato FROM Tipo_Prato WHERE designacao = ?', (designacao,))
    row = fetch_one(cursor)
    if row:
        return row['id_tipo_prato']
    db.execute('INSERT INTO Tipo_Prato (designacao) VALUES (?)', (designacao,))
    db.commit() # commit if autocommit is false
    cursor = db.execute('SELECT id_tipo_prato FROM Tipo_Prato WHERE designacao = ?', (designacao,))
    return fetch_one(cursor)['id_tipo_prato']

def get_menu_details(menu_row, db):
    cursor = db.execute('''
        SELECT P.nome, P.receita, TP.designacao as cat
        FROM Constituicao_Menu_Pratos CMP
        JOIN Prato P ON CMP.id_prato = P.id_prato
        LEFT JOIN Tipo_Prato TP ON P.id_tipo_prato = TP.id_tipo_prato
        WHERE CMP.id_menu = ? AND CMP.isdeleted = 0 AND P.isdeleted = 0
    ''', (menu_row['id_menu'],))
    pratos = fetch_all(cursor)
    
    cursor = db.execute('''
        SELECT B.nome, B.receita
        FROM Constituicao_Menu_Bebidas CMB
        JOIN Bebida B ON CMB.id_bebida = B.id_bebida
        WHERE CMB.id_menu = ? AND CMB.isdeleted = 0 AND B.isdeleted = 0
    ''', (menu_row['id_menu'],))
    bebidas = fetch_all(cursor)

    res = {
        'id': menu_row['id_menu'],
        'nome': menu_row['descricao'],
        'entradas': {'nome': '', 'ingredientes': ''},
        'pratoPrincipal': {'nome': '', 'ingredientes': ''},
        'acompanhamentos': {'nome': '', 'ingredientes': ''},
        'sobremesa': {'nome': '', 'ingredientes': ''},
        'bebidas': {'nome': '', 'ingredientes': ''},
        'ceia': {'nome': '', 'ingredientes': ''}
    }
    
    for p in pratos:
        cat = p['cat']
        if cat in res:
            res[cat] = {'nome': p['nome'] or '', 'ingredientes': p['receita'] or ''}
            
    for b in bebidas:
        res['bebidas'] = {'nome': b['nome'] or '', 'ingredientes': b['receita'] or ''}
        
    return res


def get_events():
    db = get_db()
    cursor = db.execute('''
        SELECT E.*, C.nome as cliente_nome, TE.descricao as tipo_evento
        FROM Evento E
        JOIN Cliente C ON E.id_cliente = C.id_cliente
        JOIN Tipo_evento TE ON E.id_tipo_evento = TE.id_tipo_evento
        WHERE E.isdeleted = 0
        ORDER BY E.id_evento DESC
    ''')
    events = fetch_all(cursor)
    res = []
    for e in events:
        s_cursor = db.execute('''
            SELECT S.descricao 
            FROM Servico_Evento SE
            JOIN Servico S ON SE.id_servico = S.id_servico
            WHERE SE.id_evento = ? AND SE.isdeleted = 0 AND S.isdeleted = 0
        ''', (e['id_evento'],))
        servs = [row['descricao'] for row in fetch_all(s_cursor)]
        res.append({
            'id': e['id_evento'],
            'cliente': e['cliente_nome'],
            'tipo': e['tipo_evento'],
            'data': e['data_evento'].isoformat() if isinstance(e['data_evento'], datetime) else str(e['data_evento']),
            'pessoas': e['nr_pessoas'],
            'local': e['morada'],
            'menuId': e['id_menu'],
            'servicos': servs
        })
    return res


def row_to_stock(row):
    return {
        'id': row['id_ingrediente'],
        'nome': row['nome'],
        'quantidade': row['quantidade'],
        'unidade': row['unidade'],
        'custo': row['custo'],
        'data_validade': row['data_validade']
    }


def get_menus():
    db = get_db()
    cursor = db.execute('SELECT * FROM Menu WHERE isdeleted = 0 ORDER BY id_menu DESC')
    return [get_menu_details(row, db) for row in fetch_all(cursor)]


def get_menu_by_id(menu_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM Menu WHERE id_menu = ? AND isdeleted = 0', (menu_id,))
    row = fetch_one(cursor)
    return get_menu_details(row, db) if row else None


def get_event_by_id(event_id):
    db = get_db()
    cursor = db.execute('''
        SELECT E.*, C.nome as cliente_nome, C.NIF as cliente_nif, C.tipo_cliente as cliente_tipo, TE.descricao as tipo_evento
        FROM Evento E
        JOIN Cliente C ON E.id_cliente = C.id_cliente
        JOIN Tipo_evento TE ON E.id_tipo_evento = TE.id_tipo_evento
        WHERE E.id_evento = ? AND E.isdeleted = 0
    ''', (event_id,))
    e = fetch_one(cursor)
    if not e:
        return None
    s_cursor = db.execute('''
        SELECT S.descricao 
        FROM Servico_Evento SE
        JOIN Servico S ON SE.id_servico = S.id_servico
        WHERE SE.id_evento = ? AND SE.isdeleted = 0 AND S.isdeleted = 0
    ''', (event_id,))
    servs = [row['descricao'] for row in fetch_all(s_cursor)]
    return {
        'id': e['id_evento'],
        'cliente': e['cliente_nome'],
        'cliente_nif': e['cliente_nif'],
        'cliente_tipo': e['cliente_tipo'],
        'tipo': e['tipo_evento'],
        'data': e['data_evento'].isoformat() if isinstance(e['data_evento'], datetime) else str(e['data_evento']),
        'pessoas': e['nr_pessoas'],
        'local': e['morada'],
        'menuId': e['id_menu'],
        'servicos': servs
    }


def get_stock_items():
    db = get_db()
    cursor = db.execute('SELECT * FROM Ingrediente WHERE isdeleted = 0 ORDER BY id_ingrediente DESC')
    return [row_to_stock(row) for row in fetch_all(cursor)]


def get_stock_item(item_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM Ingrediente WHERE id_ingrediente = ? AND isdeleted = 0', (item_id,))
    row = fetch_one(cursor)
    return row_to_stock(row) if row else None


def get_tipos_evento():
    db = get_db()
    cursor = db.execute('SELECT descricao FROM Tipo_evento WHERE isdeleted = 0')
    tipos_db = fetch_all(cursor)
    
    configs = {
        'casamento': {'emoji': '💍', 'corFundo': '#FDF2F8', 'corBorda': '#FBCFE8', 'corTexto': '#9D174D'},
        'batizado': {'emoji': '🕊️', 'corFundo': '#F0FDF4', 'corBorda': '#BBF7D0', 'corTexto': '#166534'},
        'evento empresarial': {'emoji': '💼', 'corFundo': '#EFF6FF', 'corBorda': '#BFDBFE', 'corTexto': '#1E3A8A'},
        'aniversário': {'emoji': '🎂', 'corFundo': '#FFFBEB', 'corBorda': '#FEF08A', 'corTexto': '#854D0E'},
        'conferência': {'emoji': '🎤', 'corFundo': '#F3E8FF', 'corBorda': '#D8B4FE', 'corTexto': '#6B21A8'},
        'jantar de gala': {'emoji': '🥂', 'corFundo': '#FEF2F2', 'corBorda': '#FECACA', 'corTexto': '#991B1B'},
        'workshop': {'emoji': '🛠️', 'corFundo': '#ECFEFF', 'corBorda': '#A5F3FC', 'corTexto': '#155E75'}
    }
    
    res = {}
    for t in tipos_db:
        desc = t['descricao']
        desc_lower = desc.lower().replace('á', 'a').replace('â', 'a').replace('é', 'e').replace('ê', 'e')
        # Simple fuzzy match for "empresarial", "aniversário"
        matched = False
        for k, v in configs.items():
            if k.replace('á', 'a') in desc_lower:
                res[desc] = v.copy()
                res[desc]['label'] = desc
                matched = True
                break
        
        if not matched:
            res[desc] = {
                'label': desc, 
                'emoji': '📅', 
                'corFundo': '#F3F4F6', 
                'corBorda': '#D1D5DB', 
                'corTexto': '#374151'
            }
    
    # If db is empty, return a default so it doesn't break
    if not res:
        res['Corporate / Empresa'] = {'label': 'Corporate / Empresa', 'emoji': '💼', 'corFundo': '#EFF6FF', 'corBorda': '#BFDBFE', 'corTexto': '#1E3A8A'}
    return res

def get_servicos():
    db = get_db()
    cursor = db.execute('SELECT descricao FROM Servico WHERE isdeleted = 0')
    servs = fetch_all(cursor)
    return [(row['descricao'], row['descricao']) for row in servs]

# get_event_by_id replaced above


def get_or_create_cliente(db, nome, nif, tipo):
    cursor = db.execute('SELECT id_cliente FROM Cliente WHERE NIF = ?', (nif,))
    row = fetch_one(cursor)
    if row:
        db.execute('UPDATE Cliente SET nome = ?, tipo_cliente = ? WHERE NIF = ?', (nome, tipo, nif))
        db.commit()
        return row['id_cliente']
    db.execute('INSERT INTO Cliente (nome, NIF, tipo_cliente) VALUES (?, ?, ?)', (nome, nif, tipo))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def get_or_create_tipo_evento(db, descricao):
    cursor = db.execute('SELECT id_tipo_evento FROM Tipo_evento WHERE descricao = ?', (descricao,))
    row = fetch_one(cursor)
    if row:
        return row['id_tipo_evento']
    db.execute('INSERT INTO Tipo_evento (descricao) VALUES (?)', (descricao,))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def get_or_create_servico(db, descricao):
    cursor = db.execute('SELECT id_servico FROM Servico WHERE descricao = ?', (descricao,))
    row = fetch_one(cursor)
    if row:
        return row['id_servico']
    db.execute('INSERT INTO Servico (descricao, custo) VALUES (?, 0)', (descricao,))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

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
        'tipo': 'Corporate / Empresa',
        'cliente': '',
        'cliente_nif': '',
        'cliente_tipo': 'Empresa',
        'data': '',
        'pessoas': '',
        'local': '',
        'menu_id': '',
        'servicos': []
    }

    if request.method == 'POST':
        form = {
            'tipo': request.form.get('tipo', 'Corporate / Empresa').strip(),
            'cliente': request.form.get('cliente', '').strip(),
            'cliente_nif': request.form.get('cliente_nif', '').strip(),
            'cliente_tipo': request.form.get('cliente_tipo', 'Empresa').strip(),
            'data': request.form.get('data', '').strip(),
            'pessoas': request.form.get('pessoas', '').strip(),
            'local': request.form.get('local', '').strip(),
            'menu_id': request.form.get('menu_id', '').strip(),
            'servicos': request.form.getlist('servicos')
        }
        event_id = request.form.get('event_id')

        if not form['cliente'] or not form['cliente_nif'] or not form['data'] or not form['local'] or not form['menu_id']:
            message = 'Por favor, preencha o cliente, NIF, data, local e escolha um menu.'
        else:
            db = get_db()
            id_cliente = get_or_create_cliente(db, form['cliente'], form['cliente_nif'], form['cliente_tipo'])
            id_tipo_evento = get_or_create_tipo_evento(db, form['tipo'])
            nr_pessoas = int(form['pessoas']) if form['pessoas'].isdigit() else 1
            data_sql = form['data'].replace('T', ' ')
            if len(data_sql) == 16:
                data_sql += ':00'
            
            if event_id and event_id.isdigit():
                db.execute(
                    '''
                    UPDATE Evento
                    SET id_cliente = ?, id_menu = ?, id_tipo_evento = ?, morada = ?, data_evento = ?, nr_pessoas = ?
                    WHERE id_evento = ?
                    ''',
                    (
                        id_cliente,
                        int(form['menu_id']),
                        id_tipo_evento,
                        form['local'],
                        data_sql,
                        nr_pessoas,
                        int(event_id)
                    )
                )
                db.execute('UPDATE Servico_Evento SET isdeleted = 1 WHERE id_evento = ?', (int(event_id),))
                db.commit()
                e_id = int(event_id)
            else:
                db.execute(
                    '''
                    INSERT INTO Evento (id_cliente, id_menu, id_tipo_evento, morada, data_evento, nr_pessoas, duracao, custo, margem)
                    VALUES (?, ?, ?, ?, ?, ?, 1, 0, 0)
                    ''',
                    (
                        id_cliente,
                        int(form['menu_id']),
                        id_tipo_evento,
                        form['local'],
                        data_sql,
                        nr_pessoas
                    )
                )
                db.commit()
                e_id = fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

            for serv in form['servicos']:
                id_serv = get_or_create_servico(db, serv)
                cursor = db.execute('SELECT * FROM Servico_Evento WHERE id_evento = ? AND id_servico = ?', (e_id, id_serv))
                if fetch_one(cursor):
                    db.execute('UPDATE Servico_Evento SET isdeleted = 0 WHERE id_evento = ? AND id_servico = ?', (e_id, id_serv))
                else:
                    db.execute('INSERT INTO Servico_Evento (id_evento, id_servico) VALUES (?, ?)', (e_id, id_serv))
            db.commit()
            return redirect(url_for('create_event', success=1))

    else:
        edit_id = request.args.get('edit_id')
        if edit_id and edit_id.isdigit():
            editing_event = get_event_by_id(int(edit_id))
            if editing_event:
                form = {
                    'tipo': editing_event['tipo'],
                    'cliente': editing_event['cliente'],
                    'cliente_nif': editing_event['cliente_nif'],
                    'cliente_tipo': editing_event['cliente_tipo'],
                    'data': editing_event['data'].replace(' ', 'T')[:16] if editing_event['data'] else '',
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
        servicos_list=get_servicos(),
        tipos_evento=get_tipos_evento(),
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
                menu_id = int(form['menu_id'])
                db.execute('UPDATE Menu SET descricao = ? WHERE id_menu = ?', (form['menu_name'], menu_id))
                db.execute('UPDATE Constituicao_Menu_Pratos SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
                db.execute('UPDATE Constituicao_Menu_Bebidas SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
            else:
                db.execute('INSERT INTO Menu (descricao) VALUES (?)', (form['menu_name'],))
                db.commit()
                cursor = db.execute('SELECT @@IDENTITY AS id')
                menu_id = fetch_one(cursor)['id']
            
            for cat in categorias_catering:
                cat_id = cat['id']
                p_nome = form[cat_id]['nome']
                p_ing = form[cat_id]['ingredientes']
                if p_nome:
                    if cat_id == 'bebidas':
                        db.execute('INSERT INTO Bebida (nome, receita) VALUES (?, ?)', (p_nome, p_ing))
                        db.commit()
                        b_id = fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']
                        db.execute('INSERT INTO Constituicao_Menu_Bebidas (id_menu, id_bebida) VALUES (?, ?)', (menu_id, b_id))
                    else:
                        tp_id = get_or_create_tipo_prato(db, cat_id)
                        db.execute('INSERT INTO Prato (id_tipo_prato, nome, receita) VALUES (?, ?, ?)', (tp_id, p_nome, p_ing))
                        db.commit()
                        p_id = fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']
                        db.execute('INSERT INTO Constituicao_Menu_Pratos (id_menu, id_prato) VALUES (?, ?)', (menu_id, p_id))
                        
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
        tipos_evento=get_tipos_evento()
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
        tipos_evento=get_tipos_evento()
    )


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    message = None
    form = {
        'nome': '',
        'quantidade': '',
        'unidade': '',
        'custo': '',
        'data_validade': ''
    }
    editing_item = None

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        input_id = request.form.get('input_id', '').strip()
        
        form['nome'] = request.form.get('nome', '').strip()
        form['quantidade'] = request.form.get('quantidade', '').strip()
        form['unidade'] = request.form.get('unidade', '').strip()
        form['custo'] = request.form.get('custo', '').strip()
        form['data_validade'] = request.form.get('data_validade', '').strip()
        form['input_id'] = input_id

        if not form['nome'] and not input_id:
            message = 'Por favor, indique o nome do ingrediente ou insira o seu ID.'
        else:
            db = get_db()
            
            if item_id and item_id.isdigit():
                db.execute(
                    '''
                    UPDATE Ingrediente
                    SET nome = ?, quantidade = ?, unidade = ?, custo = ?, data_validade = ?
                    WHERE id_ingrediente = ?
                    ''',
                    (
                        form['nome'],
                        int(form['quantidade']) if form['quantidade'].isdigit() else 0,
                        form['unidade'],
                        float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else 0.0,
                        form['data_validade'] if form['data_validade'] else None,
                        int(item_id)
                    )
                )
                db.commit()
                return redirect(url_for('stock', success=1))
                
            elif input_id and input_id.isdigit():
                target_id = int(input_id)
                existing = get_stock_item(target_id)
                if not existing:
                    message = f'Erro: Não existe nenhum produto no stock com o ID {target_id}. Deixe o ID em branco para criar um novo.'
                else:
                    add_qtd = int(form['quantidade']) if form['quantidade'].isdigit() else 0
                    new_qtd = existing['quantidade'] + add_qtd
                    
                    new_nome = form['nome'] if form['nome'] else existing['nome']
                    new_unidade = form['unidade'] if form['unidade'] else existing['unidade']
                    new_custo = float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else existing['custo']
                    new_validade = form['data_validade'] if form['data_validade'] else existing['data_validade']

                    db.execute(
                        '''
                        UPDATE Ingrediente
                        SET nome = ?, quantidade = ?, unidade = ?, custo = ?, data_validade = ?
                        WHERE id_ingrediente = ?
                        ''',
                        (new_nome, new_qtd, new_unidade, new_custo, new_validade, target_id)
                    )
                    db.commit()
                    return redirect(url_for('stock', success=1))
                    
            else:
                db.execute(
                    '''
                    INSERT INTO Ingrediente (nome, quantidade, unidade, custo, data_validade)
                    VALUES (?, ?, ?, ?, ?)
                    ''',
                    (
                        form['nome'],
                        int(form['quantidade']) if form['quantidade'].isdigit() else 0,
                        form['unidade'],
                        float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else 0.0,
                        form['data_validade'] if form['data_validade'] else None
                    )
                )
                db.commit()
                return redirect(url_for('stock', success=1))

    edit_id = request.args.get('edit_id')
    if edit_id and edit_id.isdigit():
        editing_item = get_stock_item(int(edit_id))
        if editing_item:
            form = {
                'nome': editing_item['nome'],
                'quantidade': editing_item['quantidade'],
                'unidade': editing_item['unidade'],
                'custo': editing_item['custo'],
                'data_validade': editing_item['data_validade']
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
    db.execute('UPDATE Ingrediente SET isdeleted = 1 WHERE id_ingrediente = ?', (item_id,))
    db.commit()
    return redirect(url_for('stock', success=1))


@app.route('/menus/delete/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    db = get_db()
    db.execute('UPDATE Menu SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
    db.commit()
    return redirect(url_for('manage_menus', success=1))


@app.route('/events/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    db = get_db()
    db.execute('UPDATE Evento SET isdeleted = 1 WHERE id_evento = ?', (event_id,))
    db.commit()
    return redirect(url_for('events'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
