from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from db.database import get_db
from services import DishesService, MenusService

dishes_bp = Blueprint('dishes', __name__)



@dishes_bp.route('/manage-dishes', methods=['GET', 'POST'], endpoint='manage_dishes')
def manage_dishes():
    message = None
    form = {
        'id': '',
        'tipo': 'prato',
        'categoria': 'entradas',
        'nome': '',
        'receita': '',
        'ingredientes': []
    }

    if request.method == 'POST':
        form['id'] = request.form.get('id', '').strip()
        form['tipo'] = request.form.get('tipo', 'prato').strip()
        form['categoria'] = request.form.get('categoria', 'entradas').strip()
        form['nome'] = request.form.get('nome', '').strip()
        form['receita'] = request.form.get('receita', '').strip()

        ingredient_ids = request.form.getlist('ingrediente_id')
        ingredient_quantities = request.form.getlist('ingrediente_quantidade')
        ingredientes = []
        max_rows = max(len(ingredient_ids), len(ingredient_quantities)) if ingredient_ids or ingredient_quantities else 0
        
        for idx in range(max_rows):
            ing_id = ingredient_ids[idx].strip() if idx < len(ingredient_ids) else ''
            qty = ingredient_quantities[idx].strip() if idx < len(ingredient_quantities) else ''
            if not ing_id or not qty:
                continue
            ingredientes.append({'id': ing_id, 'quantidade': qty})

        form['ingredientes'] = ingredientes

        if not form['nome']:
            message = 'Por favor, indique um nome para o prato ou bebida.'
        else:
            db = get_db()
            try:
                if form['tipo'] == 'bebida':
                    DishesService.save_bebida(db, form['id'], form['nome'], form['receita'], ingredientes)
                else:
                    DishesService.save_prato(db, form['id'], form['nome'], form['receita'], form['categoria'], ingredientes)
                return redirect(url_for('dishes.manage_dishes', success=1))
            except Exception as e:
                message = f'Erro ao guardar: {str(e)}'

    # Buscar dados para exibição
    pratos = MenusService.get_all_dishes()
    bebidas = MenusService.get_all_drinks()
    ingredients = MenusService.get_categorias_catering()
    
    pratos_por_categoria = {}
    for p in pratos:
        cat = MenusService.map_categoria_bd(p.get('categoria'))
        pratos_por_categoria.setdefault(cat, []).append(p)

    return render_template(
        'manage_dishes.html',
        active_page='manage_dishes',
        message=message,
        form=form,
        categorias_catering=MenusService.CATEGORIAS_CATERING,
        pratos_por_categoria=pratos_por_categoria,
        bebidas=bebidas,
        ingredients=ingredients
    )


@dishes_bp.route('/dishes/delete/prato/<int:prato_id>', methods=['POST'], endpoint='delete_prato')
def delete_prato(prato_id):
    db = get_db()
    DishesService.delete_prato(db, prato_id)
    return redirect(url_for('dishes.manage_dishes', success=1))


@dishes_bp.route('/dishes/delete/bebida/<int:bebida_id>', methods=['POST'], endpoint='delete_bebida')
def delete_bebida(bebida_id):
    db = get_db()
    DishesService.delete_bebida(db, bebida_id)
    return redirect(url_for('dishes.manage_dishes', success=1))


@dishes_bp.route('/api/dish/<tipo>/<int:item_id>', methods=['GET'], endpoint='api_dish_details')
def api_dish_details(tipo, item_id):
    if tipo == 'prato':
        details = DishesService.get_prato_details(item_id)
    elif tipo == 'bebida':
        details = DishesService.get_bebida_details(item_id)
    else:
        return jsonify({'success': False, 'error': 'Tipo inválido'}), 400

    if details:
        return jsonify({'success': True, 'data': details})
    return jsonify({'success': False, 'error': 'Artigo não encontrado'}), 404
