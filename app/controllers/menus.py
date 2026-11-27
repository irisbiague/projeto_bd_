from flask import Blueprint, redirect, render_template, request, url_for
from db.database import get_db
from services import MenusService

menus_bp = Blueprint('menus', __name__)


@menus_bp.route('/manage-menus', methods=['GET', 'POST'], endpoint='manage_menus')
def manage_menus():
    message = None
    editing_menu = None
    categorias = MenusService.CATEGORIAS_CATERING
    form = {'menu_id': '', 'menu_name': ''}
    for cat in categorias:
        form[cat['id']] = {'id': []}

    if request.method == 'POST':
        form['menu_id'] = request.form.get('menu_id', '').strip()
        form['menu_name'] = request.form.get('menu_name', '').strip()
        for cat in categorias:
            form[cat['id']]['id'] = request.form.getlist(f"{cat['id']}_id")

        if not form['menu_name']:
            message = 'Por favor, indique um nome para o menu.'
        else:
            db = get_db()
            try:
                MenusService.save_menu(db, form)
                return redirect(url_for('menus.manage_menus', success=1))
            except Exception as e:
                message = f'Erro ao guardar menu: {str(e)}'

    else:
        edit_id = request.args.get('edit_id')
        if edit_id and str(edit_id).isdigit():
            editing_menu = MenusService.get_menu_by_id(int(edit_id))
            if editing_menu:
                form = {
                    'menu_id': str(editing_menu['id']),
                    'menu_name': editing_menu['nome']
                }
                for cat in categorias:
                    form[cat['id']] = {
                        'id': [str(item['id']) for item in editing_menu[cat['id']]]
                    }

    if request.args.get('success'):
        message = 'Menu guardado com sucesso!'

    menus = MenusService.get_all_menus()
    pratos = MenusService.get_all_dishes()
    bebidas = MenusService.get_all_drinks()

    pratos_por_categoria = {}
    for p in pratos:
        cat = MenusService.map_categoria_bd(p.get('categoria'))
        pratos_por_categoria.setdefault(cat, []).append(p)

    return render_template(
        'manage_menus.html',
        active_page='manage_menus',
        message=message,
        form=form,
        menus=menus,
        categorias_catering=categorias,
        editing_menu=editing_menu,
        pratos_por_categoria=pratos_por_categoria,
        bebidas=bebidas
    )


@menus_bp.route('/menus/delete/<int:menu_id>', methods=['POST'], endpoint='delete_menu')
def delete_menu(menu_id):
    db = get_db()
    MenusService.delete_menu(db, menu_id)
    return redirect(url_for('menus.manage_menus', success=1))
