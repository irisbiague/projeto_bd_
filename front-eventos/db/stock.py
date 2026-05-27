from .database import get_db, fetch_all, fetch_one

def row_to_stock(row):
    return {
        'id': row['id_ingrediente'],
        'nome': row['nome'],
        'quantidade': row['quantidade'],
        'unidade': row['unidade'],
        'custo': row['custo'],
        'data_validade': row['data_validade']
    }

def get_stock_items():
    db = get_db()
    cursor = db.execute('SELECT * FROM VIEWS.V_Ingredientes_quantidade_custo ORDER BY id_ingrediente DESC')
    return [row_to_stock(row) for row in fetch_all(cursor)]

def get_stock_item(item_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM VIEWS.V_Ingredientes_quantidade_custo WHERE id_ingrediente = ?', (item_id,))
    row = fetch_one(cursor)
    return row_to_stock(row) if row else None

def save_stock_item(db, item_id, input_id, form):
    quantity = int(form['quantidade']) if form['quantidade'].isdigit() else 0
    price = float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else None
    validade = form['data_validade'] if form['data_validade'] else None

    if item_id and item_id.isdigit():
        ingredient_id = int(item_id)
        db.execute(
            '''
            UPDATE DDL.Ingrediente
            SET nome = ?, unidade = ?, data_validade = ?
            WHERE id_ingrediente = ?
            ''',
            (
                form['nome'],
                form['unidade'],
                validade,
                ingredient_id
            )
        )
        db.commit()
        return True, None

    elif input_id and input_id.isdigit():
        target_id = int(input_id)
        existing = get_stock_item(target_id)
        if not existing:
            return False, f'Erro: Não existe nenhum produto no stock com o ID {target_id}. Deixe o ID em branco para criar um novo.'

        new_nome = form['nome'] if form['nome'] else existing['nome']
        new_unidade = form['unidade'] if form['unidade'] else existing['unidade']
        new_validade = form['data_validade'] if form['data_validade'] else existing['data_validade']

        db.execute(
            '''
            UPDATE DDL.Ingrediente
            SET nome = ?, unidade = ?, data_validade = ?
            WHERE id_ingrediente = ?
            ''',
            (new_nome, new_unidade, new_validade, target_id)
        )

        if quantity > 0:
            if price is None:
                return False, 'Por favor, indique um custo válido para adicionar um lote.'
            db.execute('EXEC SP.sp_NovoLote ?, ?, ?, ?', (target_id, None, price, quantity))
        db.commit()
        return True, None
            
    else:
        cursor = db.execute(
            '''
            INSERT INTO DDL.Ingrediente (nome, unidade, data_validade)
            VALUES (?, ?, ?)
            ''',
            (
                form['nome'],
                form['unidade'],
                validade
            )
        )
        cursor = db.execute('SELECT CAST(SCOPE_IDENTITY() AS INT) AS id')
        ingredient_id = cursor.fetchone()[0]

        if quantity > 0:
            if price is None:
                return False, 'Por favor, indique um custo válido para criar o lote.'
            db.execute('EXEC SP.sp_NovoLote ?, ?, ?, ?', (ingredient_id, None, price, quantity))

        db.commit()
        return True, None


def add_lote_item(db, ingredient_id, fornecedor_id, preco, quantidade_deduzivel):
    try:
        db.execute('EXEC SP.sp_NovoLote ?, ?, ?, ?', (ingredient_id, fornecedor_id, preco, quantidade_deduzivel))
        db.commit()
        return True, None
    except Exception as exc:
        return False, str(exc)

def edit_lote_item(db, id_lote, fornecedor_id, preco, quantidade_deduzivel, quantidade_deduzida=0):
    try:
        db.execute(
            '''
            UPDATE DDL.Lote
            SET preco = ?, quantidade_deduzivel = ?, quantidade_deduzida = ?, id_fornecedor = ?
            WHERE id_lote = ?
            ''',
            (preco, quantidade_deduzivel, quantidade_deduzida, fornecedor_id, id_lote)
        )
        db.commit()
        return True, None
    except Exception as exc:
        return False, str(exc)

def delete_lote_item(db, id_lote):
    try:
        db.execute('UPDATE DDL.Lote SET isdeleted = 1 WHERE id_lote = ?', (id_lote,))
        db.commit()
        return True, None
    except Exception as exc:
        return False, str(exc)


def stock_lotes(ingredient_id):
    db = get_db()
    cursor = db.execute('''
        SELECT *
        FROM UDF.fn_LotesDetalhadosPorIngrediente(?)        
        ORDER BY id_lote DESC
    ''', (ingredient_id,))
    return fetch_all(cursor)


