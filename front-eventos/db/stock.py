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
    cursor = db.execute('SELECT * FROM DDL.Ingrediente WHERE isdeleted = 0 ORDER BY id_ingrediente DESC')
    return [row_to_stock(row) for row in fetch_all(cursor)]

def get_stock_item(item_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM DDL.Ingrediente WHERE id_ingrediente = ? AND isdeleted = 0', (item_id,))
    row = fetch_one(cursor)
    return row_to_stock(row) if row else None

def save_stock_item(db, item_id, input_id, form):
    if item_id and item_id.isdigit():
        db.execute(
            '''
            UPDATE DDL.Ingrediente
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
        return True, None
        
    elif input_id and input_id.isdigit():
        target_id = int(input_id)
        existing = get_stock_item(target_id)
        if not existing:
            return False, f'Erro: Não existe nenhum produto no stock com o ID {target_id}. Deixe o ID em branco para criar um novo.'
        else:
            add_qtd = int(form['quantidade']) if form['quantidade'].isdigit() else 0
            new_qtd = existing['quantidade'] + add_qtd
            
            new_nome = form['nome'] if form['nome'] else existing['nome']
            new_unidade = form['unidade'] if form['unidade'] else existing['unidade']
            new_custo = float(form['custo']) if form['custo'].replace('.', '', 1).isdigit() else existing['custo']
            new_validade = form['data_validade'] if form['data_validade'] else existing['data_validade']

            db.execute(
                '''
                UPDATE DDL.Ingrediente
                SET nome = ?, quantidade = ?, unidade = ?, custo = ?, data_validade = ?
                WHERE id_ingrediente = ?
                ''',
                (new_nome, new_qtd, new_unidade, new_custo, new_validade, target_id)
            )
            db.commit()
            return True, None
            
    else:
        db.execute(
            '''
            INSERT INTO DDL.Ingrediente (nome, quantidade, unidade, custo, data_validade)
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
        return True, None

def delete_stock_item(db, item_id):
    db.execute('UPDATE DDL.Ingrediente SET isdeleted = 1 WHERE id_ingrediente = ?', (item_id,))
    db.commit()
