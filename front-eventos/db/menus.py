from .database import get_db, fetch_all, fetch_one

categorias_catering = [
    {'id': 'entradas', 'titulo': 'Entradas e Aperitivos', 'placeholderNome': 'Ex: Tábua de Queijos...'},
    {'id': 'pratoPrincipal', 'titulo': 'Prato Principal', 'placeholderNome': 'Ex: Lombo Assado...'},
    {'id': 'acompanhamentos', 'titulo': 'Acompanhamentos', 'placeholderNome': 'Ex: Arroz Árabe...'},
    {'id': 'sobremesa', 'titulo': 'Sobremesa', 'placeholderNome': 'Ex: Buffet de Doces...'},
    {'id': 'bebidas', 'titulo': 'Serviço de Bebidas', 'placeholderNome': 'Ex: Vinhos do Douro...'},
    {'id': 'ceia', 'titulo': 'Ceia / Snacks Extra', 'placeholderNome': 'Ex: Caldo Verde...'}
]

def get_or_create_tipo_prato(db, designacao):
    cursor = db.execute('SELECT id_tipo_prato FROM Tipo_Prato WHERE designacao = ?', (designacao,))
    row = fetch_one(cursor)
    if row:
        return row['id_tipo_prato']
    db.execute('INSERT INTO Tipo_Prato (designacao) VALUES (?)', (designacao,))
    db.commit()
    cursor = db.execute('SELECT id_tipo_prato FROM Tipo_Prato WHERE designacao = ?', (designacao,))
    return fetch_one(cursor)['id_tipo_prato']

def get_menu_details(menu_row, db):
    cursor = db.execute('''
        SELECT P.id_prato, P.nome, P.receita, TP.designacao as cat
        FROM Constituicao_Menu_Pratos CMP
        JOIN Prato P ON CMP.id_prato = P.id_prato
        LEFT JOIN Tipo_Prato TP ON P.id_tipo_prato = TP.id_tipo_prato
        WHERE CMP.id_menu = ? AND CMP.isdeleted = 0 AND P.isdeleted = 0
    ''', (menu_row['id_menu'],))
    pratos = fetch_all(cursor)
    
    cursor = db.execute('''
        SELECT B.id_bebida, B.nome, B.receita
        FROM Constituicao_Menu_Bebidas CMB
        JOIN Bebida B ON CMB.id_bebida = B.id_bebida
        WHERE CMB.id_menu = ? AND CMB.isdeleted = 0 AND B.isdeleted = 0
    ''', (menu_row['id_menu'],))
    bebidas = fetch_all(cursor)

    res = {
        'id': menu_row['id_menu'],
        'nome': menu_row['descricao'],
        'entradas': {'id': '', 'nome': '', 'ingredientes': ''},
        'pratoPrincipal': {'id': '', 'nome': '', 'ingredientes': ''},
        'acompanhamentos': {'id': '', 'nome': '', 'ingredientes': ''},
        'sobremesa': {'id': '', 'nome': '', 'ingredientes': ''},
        'bebidas': {'id': '', 'nome': '', 'ingredientes': ''},
        'ceia': {'id': '', 'nome': '', 'ingredientes': ''}
    }
    
    for p in pratos:
        cat = p['cat']
        if cat in res:
            res[cat] = {'id': p['id_prato'], 'nome': p['nome'] or '', 'ingredientes': p['receita'] or ''}
            
    for b in bebidas:
        res['bebidas'] = {'id': b['id_bebida'], 'nome': b['nome'] or '', 'ingredientes': b['receita'] or ''}
        
    return res

def get_menus():
    db = get_db()
    cursor = db.execute('SELECT * FROM Menu WHERE isdeleted = 0 ORDER BY id_menu DESC')
    return [get_menu_details(row, db) for row in fetch_all(cursor)]

def get_menu_by_id(menu_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM Menu WHERE id_menu = ? AND isdeleted = 0', (menu_id,))
    row = fetch_one(cursor)
    return get_menu_details(row, db) if row else None

def save_menu(db, form):
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
        selected_id = form.get(f'{cat_id}_id')
        if selected_id and selected_id.isdigit():
            if cat_id == 'bebidas':
                db.execute('INSERT INTO Constituicao_Menu_Bebidas (id_menu, id_bebida) VALUES (?, ?)', (menu_id, int(selected_id)))
            else:
                db.execute('INSERT INTO Constituicao_Menu_Pratos (id_menu, id_prato) VALUES (?, ?)', (menu_id, int(selected_id)))
                
    db.commit()

def delete_menu(db, menu_id):
    db.execute('UPDATE Menu SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
    db.commit()

def get_todos_pratos():
    db = get_db()
    cursor = db.execute('''
        SELECT P.id_prato, P.nome, P.receita, TP.designacao as categoria
        FROM Prato P
        JOIN Tipo_Prato TP ON P.id_tipo_prato = TP.id_tipo_prato
        WHERE P.isdeleted = 0
        ORDER BY P.id_prato DESC
    ''')
    return fetch_all(cursor)

def get_todas_bebidas():
    db = get_db()
    cursor = db.execute('''
        SELECT id_bebida, nome, receita
        FROM Bebida
        WHERE isdeleted = 0
        ORDER BY id_bebida DESC
    ''')
    return fetch_all(cursor)

def save_prato(db, prato_id, nome, receita, categoria):
    tp_id = get_or_create_tipo_prato(db, categoria)
    if prato_id and prato_id.isdigit():
        db.execute('UPDATE Prato SET nome = ?, receita = ?, id_tipo_prato = ? WHERE id_prato = ?', (nome, receita, tp_id, int(prato_id)))
    else:
        db.execute('INSERT INTO Prato (id_tipo_prato, nome, receita) VALUES (?, ?, ?)', (tp_id, nome, receita))
    db.commit()

def save_bebida(db, bebida_id, nome, receita):
    if bebida_id and bebida_id.isdigit():
        db.execute('UPDATE Bebida SET nome = ?, receita = ? WHERE id_bebida = ?', (nome, receita, int(bebida_id)))
    else:
        db.execute('INSERT INTO Bebida (nome, receita) VALUES (?, ?)', (nome, receita))
    db.commit()

def delete_prato(db, prato_id):
    db.execute('UPDATE Prato SET isdeleted = 1 WHERE id_prato = ?', (prato_id,))
    db.commit()

def delete_bebida(db, bebida_id):
    db.execute('UPDATE Bebida SET isdeleted = 1 WHERE id_bebida = ?', (bebida_id,))
    db.commit()
