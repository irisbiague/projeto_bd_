# -*- coding: utf-8 -*-
import json
import pyodbc
from datetime import date, datetime
from flask import Flask, g, redirect, render_template, request, session, url_for

from db.database import SQL_SERVER_CONFIG, set_db_config, get_db, close_db, build_connection_string, init_db
from db.eventos import get_events, get_event_by_id, get_tipos_evento, get_servicos, save_evento, delete_evento as db_delete_evento
from db.menus import (
    get_menus, get_menu_by_id, save_menu, delete_menu as db_delete_menu, categorias_catering,
    get_todos_pratos, get_todas_bebidas, save_prato, save_bebida, delete_prato as db_delete_prato, delete_bebida as db_delete_bebida
)
from db.stock import get_stock_items, get_stock_item, save_stock_item, delete_stock_item

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'mudar-isto-para-uma-chave-secreta'

app.teardown_appcontext(close_db)

dias_da_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
meses_do_ano = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


@app.before_request
def ensure_db():
    if request.endpoint in ('login', 'static', 'logout'):
        return
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    init_db()


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
                set_db_config(config)
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
            save_evento(db, form, event_id)
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
        form[cat['id']] = {'id': ''}

    if request.method == 'POST':
        form['menu_id'] = request.form.get('menu_id', '').strip()
        form['menu_name'] = request.form.get('menu_name', '').strip()
        for cat in categorias_catering:
            form[cat['id']]['id'] = request.form.get(f"{cat['id']}_id", '').strip()

        if not form['menu_name']:
            message = 'Por favor, indique um nome para o menu.'
        else:
            db = get_db()
            save_menu(db, form)
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
                        'id': str(editing_menu[cat['id']].get('id', ''))
                    }

    if request.args.get('success'):
        message = 'Menu guardado com sucesso!'

    menus = get_menus()
    pratos = get_todos_pratos()
    bebidas = get_todas_bebidas()

    pratos_por_categoria = {}
    for p in pratos:
        cat = p['categoria']
        pratos_por_categoria.setdefault(cat, []).append(p)

    return render_template(
        'manage_menus.html',
        active_page='manage_menus',
        message=message,
        form=form,
        menus=menus,
        categorias_catering=categorias_catering,
        editing_menu=editing_menu,
        pratos_por_categoria=pratos_por_categoria,
        bebidas=bebidas
    )

@app.route('/manage-dishes', methods=['GET', 'POST'])
def manage_dishes():
    message = None
    form = {'id': '', 'tipo': 'prato', 'categoria': 'entradas', 'nome': '', 'receita': ''}

    if request.method == 'POST':
        form['id'] = request.form.get('id', '').strip()
        form['tipo'] = request.form.get('tipo', 'prato').strip()
        form['categoria'] = request.form.get('categoria', 'entradas').strip()
        form['nome'] = request.form.get('nome', '').strip()
        form['receita'] = request.form.get('receita', '').strip()

        if not form['nome']:
            message = 'Por favor, indique um nome para o prato ou bebida.'
        else:
            db = get_db()
            if form['tipo'] == 'bebida':
                save_bebida(db, form['id'], form['nome'], form['receita'])
            else:
                save_prato(db, form['id'], form['nome'], form['receita'], form['categoria'])
            return redirect(url_for('manage_dishes', success=1))

    if request.args.get('success'):
        message = 'Artigo de catering guardado com sucesso!'

    pratos = get_todos_pratos()
    bebidas = get_todas_bebidas()

    pratos_por_categoria = {}
    for p in pratos:
        cat = p['categoria']
        pratos_por_categoria.setdefault(cat, []).append(p)

    return render_template(
        'manage_dishes.html',
        active_page='manage_dishes',
        message=message,
        form=form,
        categorias_catering=categorias_catering,
        pratos_por_categoria=pratos_por_categoria,
        bebidas=bebidas
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
    events_list = []
    for event in get_events():
        if not event['data']:
            continue
        try:
            event_date = datetime.fromisoformat(event['data']).date()
        except ValueError:
            continue
        if event_date.year == year and event_date.month == month and event_date.day == day:
            events_list.append(event)

    return render_template(
        'day_events.html',
        active_page='events',
        year=year,
        month=month,
        day=day,
        events=events_list,
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
            success, err_msg = save_stock_item(db, item_id, input_id, form)
            if not success:
                message = err_msg
            else:
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
    delete_stock_item(db, item_id)
    return redirect(url_for('stock', success=1))


@app.route('/menus/delete/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    db = get_db()
    db_delete_menu(db, menu_id)
    return redirect(url_for('manage_menus', success=1))

@app.route('/dishes/delete/prato/<int:prato_id>', methods=['POST'])
def delete_prato(prato_id):
    db = get_db()
    db_delete_prato(db, prato_id)
    return redirect(url_for('manage_dishes', success=1))

@app.route('/dishes/delete/bebida/<int:bebida_id>', methods=['POST'])
def delete_bebida(bebida_id):
    db = get_db()
    db_delete_bebida(db, bebida_id)
    return redirect(url_for('manage_dishes', success=1))

@app.route('/events/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    db = get_db()
    db_delete_evento(db, event_id)
    return redirect(url_for('events'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
