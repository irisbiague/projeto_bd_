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

def get_fornecedores():
    db = get_db()
    cursor = db.execute('SELECT id_fornecedor, nome FROM DDL.Fornecedor WHERE isdeleted = 0 ORDER BY nome')
    return fetch_all(cursor)


def save_stock_item(db, form):
    quantity = int(form['quantidade']) if form['quantidade'].isdigit() else 0
    price = float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else None
    validade = form['data_validade'] if form['data_validade'] else None
    fornecedor_id = int(form['fornecedor_id']) if form.get('fornecedor_id') and form['fornecedor_id'].isdigit() else None

    if not form['nome']:
        return False, 'Por favor, indique o nome do ingrediente.'
    if fornecedor_id is None:
        return False, 'Por favor, selecione um fornecedor.'

    cursor = db.cursor()
    cursor.execute(
        '''
        INSERT INTO DDL.Ingrediente (id_fornecedor, nome, unidade, data_validade)
        OUTPUT INSERTED.id_ingrediente
        VALUES (?, ?, ?, ?)
        ''',
        (
            fornecedor_id,
            form['nome'],
            form['unidade'],
            validade
        )
    )
    row = cursor.fetchone()
    
    if not row or row[0] is None:
        db.rollback()
        return False, 'Erro interno: não foi possível criar o ingrediente.'

    ingredient_id = row[0]

    if quantity > 0:
        if price is None:
            db.rollback()
            return False, 'Por favor, indique um custo válido para criar o lote.'
        db.execute('EXEC SP.sp_NovoLote ?, ?, ?, ?', (ingredient_id, fornecedor_id, price, quantity))

    db.commit()
    return True, None


def update_stock_item(db, item_id, form):
    quantity = int(form['quantidade']) if form['quantidade'].isdigit() else 0
    price = float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else None
    validade = form['data_validade'] if form['data_validade'] else None
    fornecedor_id = int(form['fornecedor_id']) if form.get('fornecedor_id') and form['fornecedor_id'].isdigit() else None

    if not form['nome']:
        return False, 'Por favor, indique o nome do ingrediente.'
    if fornecedor_id is None:
        return False, 'Por favor, selecione um fornecedor.'

    cursor = db.execute('SELECT 1 FROM DDL.Ingrediente WHERE id_ingrediente = ?', (item_id,))
    
    if cursor.fetchone() is None:
        return False, f'Ingrediente com ID {item_id} não existe.'

    db.execute(
        '''
        UPDATE DDL.Ingrediente
        SET nome = ?, unidade = ?, data_validade = ?, id_fornecedor = ?
        WHERE id_ingrediente = ?
        ''',
        (
            form['nome'],
            form['unidade'],
            validade,
            fornecedor_id,
            item_id
        )
    )

    if quantity > 0:
        if price is None:
            db.rollback()
            return False, 'Por favor, indique um custo válido para criar o lote.'
        db.execute('EXEC SP.sp_NovoLote ?, ?, ?, ?', (item_id, fornecedor_id, price, quantity))

    db.commit()
    return True, None


def delete_stock_item(db, item_id):
    try:
        db.execute('UPDATE DDL.Ingrediente SET isdeleted = 1 WHERE id_ingrediente = ?', (item_id,))
        db.commit()
        return True, None
    except Exception as exc:
        return False, str(exc)


def add_lote_item(db, ingredient_id, fornecedor_id, preco, quantidade_deduzivel):
    cursor = db.execute('SELECT 1 FROM DDL.Ingrediente WHERE id_ingrediente = ?', (ingredient_id,))
    if cursor.fetchone() is None:
        return False, f'Ingrediente com ID {ingredient_id} não existe.'

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


