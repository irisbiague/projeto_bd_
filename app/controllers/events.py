import pyodbc
from datetime import date, datetime
from flask import Blueprint, redirect, render_template, request, url_for
from db.database import get_db
from db.eventos import (
    get_events,
    get_event_by_id,
    get_tipos_evento,
    get_servicos,
    get_empregados,
    save_evento,
    delete_evento as db_delete_evento,
    get_event_inventory
)
from db.menus import get_menus, get_menu_by_id, categorias_catering


events_bp = Blueprint('events', __name__)

dias_da_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
meses_do_ano = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


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


@events_bp.route('/create-event', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    message = None
    editing_event = None
    form = {
        'tipo': 'Corporate / Empresa',
        'cliente': '',
        'cliente_nif': '',
        'cliente_tipo': 'Empresa',
        'cliente_cp': '',
        'cliente_localidade': '',
        'data': '',
        'pessoas': '',
        'local': '',
        'menu_id': '',
        'servicos': [],
        'empregados': []
    }

    if request.method == 'POST':
        form = {
            'tipo': request.form.get('tipo', 'Corporate / Empresa').strip(),
            'cliente': request.form.get('cliente', '').strip(),
            'cliente_nif': request.form.get('cliente_nif', '').strip(),
            'cliente_tipo': request.form.get('cliente_tipo', 'Empresa').strip(),
            'cliente_cp': request.form.get('cliente_cp', '').strip(),
            'cliente_localidade': request.form.get('cliente_localidade', '').strip(),
            'data': request.form.get('data', '').strip(),
            'pessoas': request.form.get('pessoas', '').strip(),
            'local': request.form.get('local', '').strip(),
            'menu_id': request.form.get('menu_id', '').strip(),
            'servicos': request.form.getlist('servicos'),
            'empregados': request.form.getlist('empregados')
        }
        event_id = request.form.get('event_id')

        if not form['cliente'] or not form['cliente_nif'] or not form['data'] or not form['local'] or not form['menu_id']:
            message = 'Por favor, preencha o cliente, NIF, data, local e escolha um menu.'
        elif not form['cliente_nif'].isdigit() or len(form['cliente_nif']) != 9:
            message = 'O NIF deve conter exactamente 9 dígitos numéricos.'
        else:
            try:
                db = get_db()
                save_evento(db, form, event_id)
                return redirect(url_for('events.create_event', success=1))
            except pyodbc.IntegrityError as e:
                if 'CHK_Cliente_NIF' in str(e):
                    message = 'NIF inválido: o NIF introduzido não é válido. Verifique o valor e tente novamente.'
                else:
                    raise

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
                    'servicos': [str(s_id) for s_id in editing_event['servicos_ids']] if 'servicos_ids' in editing_event else [],
                    'empregados': [str(e['id']) for e in editing_event['empregados']] if editing_event.get('empregados') else []
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
        empregados_list=get_empregados(),
        tipos_evento=get_tipos_evento(),
        editing_event=editing_event
    )


@events_bp.route('/events', endpoint='events')
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
        month_name=meses_do_ano[month - 1],
        month=month,
        year=year,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month_value,
        tipos_evento=get_tipos_evento()
    )


@events_bp.route('/events/day/<int:year>/<int:month>/<int:day>', endpoint='events_by_day')
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
            detailed_event = get_event_by_id(event['id'])
            if detailed_event:
                if detailed_event['menuId']:
                    detailed_event['menu'] = get_menu_by_id(detailed_event['menuId'])
                events_list.append(detailed_event)

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


@events_bp.route('/events/inventory/<int:event_id>', endpoint='event_inventory')
def event_inventory(event_id):
    event = get_event_by_id(event_id)
    if not event:
        return redirect(url_for('events.events'))

    inventory = get_event_inventory(event_id)
    return render_template(
        'event_inventory.html',
        active_page='events',
        event=event,
        inventory=inventory
    )


@events_bp.route('/events/delete/<int:event_id>', methods=['POST'], endpoint='delete_event')
def delete_event(event_id):
    db = get_db()
    db_delete_evento(db, event_id)
    return redirect(url_for('events.events'))
