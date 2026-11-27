from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from db.database import get_db
from services import StockService

stock_bp = Blueprint('stock', __name__)


@stock_bp.route('/stock/lotes/<int:ingredient_id>', methods=['GET'], endpoint='stock_lotes_route')
def stock_lotes_route(ingredient_id):
    rows = StockService.get_stock_lotes(ingredient_id)
    return jsonify(rows)


@stock_bp.route('/stock/lote/edit', methods=['POST'], endpoint='stock_edit_lote')
def stock_edit_lote():
    id_lote = request.form.get('id_lote') or (request.get_json() or {}).get('id_lote')
    if not id_lote or not str(id_lote).isdigit():
        return jsonify({'success': False, 'error': 'ID de lote inválido'}), 400
    
    preco = request.form.get('preco') or (request.get_json() or {}).get('preco')
    quantidade_deduzivel = request.form.get('quantidade_deduzivel') or (request.get_json() or {}).get('quantidade_deduzivel')
    quantidade_deduzida = request.form.get('quantidade_deduzida') or (request.get_json() or {}).get('quantidade_deduzida', '0')
    fornecedor_id = request.form.get('fornecedor_id') or (request.get_json() or {}).get('fornecedor_id')

    if not preco or not str(preco).replace('.', '', 1).isdigit():
        return jsonify({'success': False, 'error': 'Preço inválido'}), 400
    if not quantidade_deduzivel or not str(quantidade_deduzivel).isdigit():
        return jsonify({'success': False, 'error': 'Quantidade inválida'}), 400

    fornecedor = int(fornecedor_id) if fornecedor_id and str(fornecedor_id).isdigit() else None
    db = get_db()
    success, err = StockService.update_lote(db, int(id_lote), fornecedor, float(preco), int(quantidade_deduzivel), int(quantidade_deduzida))
    if not success:
        return jsonify({'success': False, 'error': err}), 500
    return jsonify({'success': True})


@stock_bp.route('/stock/lote/delete', methods=['POST'], endpoint='stock_delete_lote')
def stock_delete_lote():
    id_lote = request.form.get('id_lote') or (request.get_json() or {}).get('id_lote')
    if not id_lote or not str(id_lote).isdigit():
        return jsonify({'success': False, 'error': 'ID de lote inválido'}), 400
    db = get_db()
    success, err = StockService.delete_lote(db, int(id_lote))
    if not success:
        return jsonify({'success': False, 'error': err}), 500
    return jsonify({'success': True})


@stock_bp.route('/stock', methods=['GET', 'POST'], endpoint='stock')
def stock():
    message = None
    editing_item = None
    form = {
        'nome': '',
        'quantidade': '',
        'unidade': '',
        'custo': '',
        'data_validade': '',
        'fornecedor_id': ''
    }

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_lote':
            ingredient_id = request.form.get('ingredient_id', '').strip()
            fornecedor_id = request.form.get('fornecedor_id', '').strip()
            preco = request.form.get('preco', '').strip()
            quantidade_deduzivel = request.form.get('quantidade_deduzivel', '').strip()

            if not ingredient_id.isdigit():
                message = 'ID de ingrediente inválido.'
            elif not quantidade_deduzivel.isdigit():
                message = 'Por favor, indique uma quantidade válida para o lote.'
            elif not preco or not preco.replace('.', '', 1).isdigit():
                message = 'Por favor, indique um preço válido para o lote.'
            else:
                fornecedor = int(fornecedor_id) if fornecedor_id.isdigit() else None
                db = get_db()
                success, err_msg = StockService.add_lote(db, int(ingredient_id), fornecedor, float(preco), int(quantidade_deduzivel))
                if not success:
                    message = err_msg
                else:
                    return redirect(url_for('stock.stock', success=1))
        else:
            item_id = request.form.get('item_id')
            form['nome'] = request.form.get('nome', '').strip()
            form['quantidade'] = request.form.get('quantidade', '').strip()
            form['unidade'] = request.form.get('unidade', '').strip()
            form['custo'] = request.form.get('custo', '').strip()
            form['data_validade'] = request.form.get('data_validade', '').strip()
            form['fornecedor_id'] = request.form.get('fornecedor_id', '').strip()

            db = get_db()
            if item_id and item_id.isdigit():
                success, err_msg = StockService.update_stock_item(db, int(item_id), form)
            else:
                success, err_msg = StockService.save_stock_item(db, form)
            if not success:
                message = err_msg
            else:
                return redirect(url_for('stock.stock', success=1))

    edit_id = request.args.get('edit_id')
    if edit_id and str(edit_id).isdigit():
        editing_item = StockService.get_stock_item(int(edit_id))
        if editing_item:
            form = {
                'nome': editing_item['nome'],
                'quantidade': editing_item['quantidade'],
                'unidade': editing_item['unidade'],
                'custo': editing_item['custo'],
                'data_validade': editing_item['data_validade'],
                'fornecedor_id': editing_item.get('fornecedor_id', '')
            }

    if request.args.get('success'):
        message = 'Stock atualizado com sucesso!'

    stock_items = StockService.get_all_stock_items()
    fornecedores = StockService.get_fornecedores()
    return render_template(
        'stock.html',
        active_page='stock',
        message=message,
        stock_items=stock_items,
        stock_form=form,
        fornecedores=fornecedores,
        editing_item=editing_item
    )


@stock_bp.route('/stock/delete/<int:item_id>', methods=['POST'], endpoint='delete_stock')
def delete_stock(item_id):
    db = get_db()
    StockService.delete_stock_item(db, item_id)
    return redirect(url_for('stock.stock', success=1))
