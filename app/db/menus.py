from .database import get_db, fetch_all, fetch_one

categorias_catering = [
    {'id': 'entradas', 'titulo': 'Entradas e Aperitivos', 'placeholderNome': 'Ex: Tábua de Queijos...'},
    {'id': 'pratoPrincipal', 'titulo': 'Prato Principal', 'placeholderNome': 'Ex: Lombo Assado...'},
    {'id': 'acompanhamentos', 'titulo': 'Acompanhamentos', 'placeholderNome': 'Ex: Arroz Árabe...'},
    {'id': 'sobremesa', 'titulo': 'Sobremesa', 'placeholderNome': 'Ex: Buffet de Doces...'},
    {'id': 'bebidas', 'titulo': 'Serviço de Bebidas', 'placeholderNome': 'Ex: Vinhos do Douro...'},
    {'id': 'ceia', 'titulo': 'Ceia / Snacks Extra', 'placeholderNome': 'Ex: Caldo Verde...'}
]

def map_categoria_bd(designacao):
    if not designacao:
        return 'entradas'
    cn = designacao.lower()
    if 'entrada' in cn: return 'entradas'
    if 'principal' in cn: return 'pratoPrincipal'
    if 'acompanha' in cn: return 'acompanhamentos'
    if 'sobremesa' in cn or 'doce' in cn: return 'sobremesa'
    if 'bebida' in cn: return 'bebidas'
    if 'ceia' in cn or 'snack' in cn: return 'ceia'
    for c in categorias_catering:
        if cn == c['id'].lower() or cn == c['titulo'].lower():
            return c['id']
    return designacao

def get_or_create_tipo_prato(db, designacao):
    cursor = db.execute('SELECT id_tipo_prato FROM DDL.Tipo_Prato WHERE designacao = ?', (designacao,))
    row = fetch_one(cursor)
    if row:
        return row['id_tipo_prato']
    db.execute('INSERT INTO DDL.Tipo_Prato (designacao) VALUES (?)', (designacao,))
    db.commit()
    cursor = db.execute('SELECT id_tipo_prato FROM DDL.Tipo_Prato WHERE designacao = ?', (designacao,))
    return fetch_one(cursor)['id_tipo_prato']

def get_menu_details(menu_row, db):
    cursor = db.execute('''
        SELECT P.id_prato, P.nome, P.receita, TP.designacao as cat
        FROM DDL.Constituicao_Menu_Pratos CMP
        JOIN DDL.Prato P ON CMP.id_prato = P.id_prato
        LEFT JOIN DDL.Tipo_Prato TP ON P.id_tipo_prato = TP.id_tipo_prato
        WHERE CMP.id_menu = ? AND CMP.isdeleted = 0 AND P.isdeleted = 0
    ''', (menu_row['id_menu'],))
    pratos = fetch_all(cursor)
    
    cursor = db.execute('''
        SELECT B.id_bebida, B.nome, B.receita
        FROM DDL.Constituicao_Menu_Bebidas CMB
        JOIN DDL.Bebida B ON CMB.id_bebida = B.id_bebida
        WHERE CMB.id_menu = ? AND CMB.isdeleted = 0 AND B.isdeleted = 0
    ''', (menu_row['id_menu'],))
    bebidas = fetch_all(cursor)

    res = {
        'id': menu_row['id_menu'],
        'nome': menu_row['descricao'],
        'entradas': [],
        'pratoPrincipal': [],
        'acompanhamentos': [],
        'sobremesa': [],
        'bebidas': [],
        'ceia': []
    }

    for p in pratos:
        cat_mapped = map_categoria_bd(p['cat'])
        if cat_mapped in res:
            res[cat_mapped].append({'id': p['id_prato'], 'nome': p['nome'] or '', 'ingredientes': p['receita'] or ''})
            
    for b in bebidas:
        res['bebidas'].append({'id': b['id_bebida'], 'nome': b['nome'] or '', 'ingredientes': b['receita'] or ''})
        
    return res

def get_menus():
    db = get_db()
    cursor = db.execute('SELECT * FROM DDL.Menu WHERE isdeleted = 0 ORDER BY id_menu DESC')
    return [get_menu_details(row, db) for row in fetch_all(cursor)]

def get_menu_by_id(menu_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM DDL.Menu WHERE id_menu = ? AND isdeleted = 0', (menu_id,))
    row = fetch_one(cursor)
    return get_menu_details(row, db) if row else None

def save_menu(db, form):
    if form['menu_id'] and form['menu_id'].isdigit():
        menu_id = int(form['menu_id'])
        db.execute('UPDATE DDL.Menu SET descricao = ? WHERE id_menu = ?', (form['menu_name'], menu_id))
        db.execute('UPDATE DDL.Constituicao_Menu_Pratos SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
        db.execute('UPDATE DDL.Constituicao_Menu_Bebidas SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
    else:
        db.execute('INSERT INTO DDL.Menu (descricao) VALUES (?)', (form['menu_name'],))
        db.commit()
        cursor = db.execute('SELECT @@IDENTITY AS id')
        menu_id = fetch_one(cursor)['id']
    
    for cat in categorias_catering:
        cat_id = cat['id']
        selected_ids = form[cat_id].get('id', [])
        if isinstance(selected_ids, str):
            selected_ids = [selected_ids]
            
        for sid in selected_ids:
            if sid and sid.isdigit():
                if cat_id == 'bebidas':
                    db.execute('INSERT INTO DDL.Constituicao_Menu_Bebidas (id_menu, id_bebida) VALUES (?, ?)', (menu_id, int(sid)))
                else:
                    db.execute('INSERT INTO DDL.Constituicao_Menu_Pratos (id_menu, id_prato) VALUES (?, ?)', (menu_id, int(sid)))
                
    db.commit()

def delete_menu(db, menu_id):
    db.execute('UPDATE DDL.Menu SET isdeleted = 1 WHERE id_menu = ?', (menu_id,))
    db.commit()

def get_todos_pratos():
    db = get_db()
    cursor = db.execute('''
        SELECT P.id_prato, P.nome, P.receita, TP.designacao as categoria
        FROM DDL.Prato P
        JOIN DDL.Tipo_Prato TP ON P.id_tipo_prato = TP.id_tipo_prato
        WHERE P.isdeleted = 0
        ORDER BY P.id_prato DESC
    ''')
    return fetch_all(cursor)

def get_todas_bebidas():
    db = get_db()
    cursor = db.execute('''
        SELECT id_bebida, nome, receita
        FROM DDL.Bebida
        WHERE isdeleted = 0
        ORDER BY id_bebida DESC
    ''')
    return fetch_all(cursor)


def get_ingredientes():
    db = get_db()
    cursor = db.execute('''
        SELECT id_ingrediente, nome, unidade
        FROM DDL.Ingrediente
        WHERE isdeleted = 0
        ORDER BY nome
    ''')
    return fetch_all(cursor)


def _normalize_ingredientes(ingredientes):
    normalized = {}
    if isinstance(ingredientes, str):
        values = [value.strip() for value in ingredientes.split(',') if value.strip()]
        for value in values:
            if not value.isdigit():
                continue
            ingrediente_id = int(value)
            normalized[ingrediente_id] = normalized.get(ingrediente_id, 0) + 1

    elif isinstance(ingredientes, list):
        for item in ingredientes:
            if not item:
                continue

            if isinstance(item, dict):
                raw_id = item.get('id') or item.get('id_ingrediente') or item.get('ingrediente_id')
                raw_qty = item.get('quantidade') or item.get('quantidade_necessaria')
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                raw_id, raw_qty = item[0], item[1]
            else:
                continue

            if raw_id is None or raw_qty is None:
                continue

            ingrediente_id = str(raw_id).strip()
            quantidade = str(raw_qty).strip()
            if not ingrediente_id.isdigit() or not quantidade.isdigit():
                continue

            ingrediente_id = int(ingrediente_id)
            quantidade = int(quantidade)
            if quantidade <= 0:
                continue

            normalized[ingrediente_id] = normalized.get(ingrediente_id, 0) + quantidade

    return [{'id': ingrediente_id, 'quantidade': quantidade} for ingrediente_id, quantidade in normalized.items()]


def save_prato(db, prato_id, nome, receita, categoria, ingredientes=None):
    tp_id = get_or_create_tipo_prato(db, categoria)
    if prato_id and prato_id.isdigit():
        db.execute('UPDATE DDL.Prato SET nome = ?, receita = ?, id_tipo_prato = ? WHERE id_prato = ?', (nome, receita, tp_id, int(prato_id)))
        prato_id = int(prato_id)
    else:
        db.execute('INSERT INTO DDL.Prato (id_tipo_prato, nome, receita) VALUES (?, ?, ?)', (tp_id, nome, receita))
        db.commit()
        cursor = db.execute('SELECT @@IDENTITY AS id')
        prato_id = fetch_one(cursor)['id']

    if ingredientes is not None:
        db.execute('UPDATE DDL.Constituicao_Prato SET isdeleted = 1 WHERE id_prato = ?', (prato_id,))
        normalized_ingredientes = _normalize_ingredientes(ingredientes)
        for item in normalized_ingredientes:
            db.execute(
                'INSERT INTO DDL.Constituicao_Prato (id_prato, id_ingrediente, quantidade) VALUES (?, ?, ?)',
                (prato_id, item['id'], item['quantidade'])
            )

    db.commit()


def save_bebida(db, bebida_id, nome, receita, ingredientes=None):
    if bebida_id and bebida_id.isdigit():
        db.execute('UPDATE DDL.Bebida SET nome = ?, receita = ? WHERE id_bebida = ?', (nome, receita, int(bebida_id)))
        bebida_id = int(bebida_id)
    else:
        db.execute('INSERT INTO DDL.Bebida (nome, receita) VALUES (?, ?)', (nome, receita))
        db.commit()
        cursor = db.execute('SELECT @@IDENTITY AS id')
        bebida_id = fetch_one(cursor)['id']

    if ingredientes is not None:
        db.execute('UPDATE DDL.Constituicao_Bebida SET isdeleted = 1 WHERE id_bebida = ?', (bebida_id,))
        for item in ingredientes:
            if not item.get('id') or not item.get('quantidade'):
                continue
            db.execute(
                'INSERT INTO DDL.Constituicao_Bebida (id_bebida, id_ingrediente, quantidade) VALUES (?, ?, ?)',
                (bebida_id, int(item['id']), int(item['quantidade']))
            )

    db.commit()

def delete_prato(db, prato_id):
    db.execute('UPDATE DDL.Prato SET isdeleted = 1 WHERE id_prato = ?', (prato_id,))
    db.execute('UPDATE DDL.Constituicao_Prato SET isdeleted = 1 WHERE id_prato = ?', (prato_id,))
    db.commit()

def delete_bebida(db, bebida_id):
    db.execute('UPDATE DDL.Bebida SET isdeleted = 1 WHERE id_bebida = ?', (bebida_id,))
    db.execute('UPDATE DDL.Constituicao_Bebida SET isdeleted = 1 WHERE id_bebida = ?', (bebida_id,))
    db.commit()

def get_prato_details(prato_id):
    db = get_db()
    cursor = db.execute('''
        SELECT P.nome, P.receita, TP.designacao as categoria
        FROM DDL.Prato P
        JOIN DDL.Tipo_Prato TP ON P.id_tipo_prato = TP.id_tipo_prato
        WHERE P.id_prato = ? AND P.isdeleted = 0
    ''', (prato_id,))
    prato = fetch_one(cursor)
    if not prato:
        return None
        
    cursor = db.execute('''
        SELECT I.nome, I.unidade, CP.quantidade
        FROM DDL.Constituicao_Prato CP
        JOIN DDL.Ingrediente I ON CP.id_ingrediente = I.id_ingrediente
        WHERE CP.id_prato = ? AND CP.isdeleted = 0 AND I.isdeleted = 0
    ''', (prato_id,))
    ingredientes = fetch_all(cursor)
    
    return {
        'nome': prato['nome'],
        'receita': prato['receita'],
        'categoria': prato['categoria'],
        'ingredientes': [{'nome': i['nome'], 'unidade': i['unidade'], 'quantidade': i['quantidade']} for i in ingredientes]
    }

def get_bebida_details(bebida_id):
    db = get_db()
    cursor = db.execute('''
        SELECT B.nome, B.receita
        FROM DDL.Bebida B
        WHERE B.id_bebida = ? AND B.isdeleted = 0
    ''', (bebida_id,))
    bebida = fetch_one(cursor)
    if not bebida:
        return None
        
    cursor = db.execute('''
        SELECT I.nome, I.unidade, CB.quantidade
        FROM DDL.Constituicao_Bebida CB
        JOIN DDL.Ingrediente I ON CB.id_ingrediente = I.id_ingrediente
        WHERE CB.id_bebida = ? AND CB.isdeleted = 0 AND I.isdeleted = 0
    ''', (bebida_id,))
    ingredientes = fetch_all(cursor)
    
    return {
        'nome': bebida['nome'],
        'receita': bebida['receita'],
        'categoria': 'Bebida',
        'ingredientes': [{'nome': i['nome'], 'unidade': i['unidade'], 'quantidade': i['quantidade']} for i in ingredientes]
    }
