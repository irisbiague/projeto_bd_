from datetime import datetime
from .database import get_db, fetch_all, fetch_one

def get_events():
    db = get_db()
    cursor = db.execute('''
        SELECT E.*, C.nome as cliente_nome, TE.descricao as tipo_evento
        FROM DDL.Evento E
        JOIN DDL.Cliente C ON E.id_cliente = C.id_cliente
        JOIN DDL.Tipo_evento TE ON E.id_tipo_evento = TE.id_tipo_evento
        WHERE E.isdeleted = 0
        ORDER BY E.id_evento DESC
    ''')
    events = fetch_all(cursor)
    res = []
    for e in events:
        s_cursor = db.execute('''
            SELECT S.descricao 
            FROM DDL.Servico_Evento SE
            JOIN DDL.Servico S ON SE.id_servico = S.id_servico
            WHERE SE.id_evento = ? AND SE.isdeleted = 0 AND S.isdeleted = 0
        ''', (e['id_evento'],))
        servs = [row['descricao'] for row in fetch_all(s_cursor)]
        res.append({
            'id': e['id_evento'],
            'cliente': e['cliente_nome'],
            'tipo': e['tipo_evento'],
            'data': e['data_evento'].isoformat() if isinstance(e['data_evento'], datetime) else str(e['data_evento']),
            'pessoas': e['nr_pessoas'],
            'local': e['morada'],
            'menuId': e['id_menu'],
            'servicos': servs
        })
    return res

def get_event_by_id(event_id):
    db = get_db()
    cursor = db.execute('''
        SELECT E.*, C.nome as cliente_nome, C.NIF as cliente_nif, C.tipo_cliente as cliente_tipo, C.codigo_postal as cliente_cp, C.localidade as cliente_localidade, TE.descricao as tipo_evento
        FROM DDL.Evento E
        JOIN DDL.Cliente C ON E.id_cliente = C.id_cliente
        JOIN DDL.Tipo_evento TE ON E.id_tipo_evento = TE.id_tipo_evento
        WHERE E.id_evento = ? AND E.isdeleted = 0
    ''', (event_id,))
    e = fetch_one(cursor)
    if not e:
        return None
    s_cursor = db.execute('''
        SELECT S.descricao 
        FROM DDL.Servico_Evento SE
        JOIN DDL.Servico S ON SE.id_servico = S.id_servico
        WHERE SE.id_evento = ? AND SE.isdeleted = 0 AND S.isdeleted = 0
    ''', (event_id,))
    servs = [row['descricao'] for row in fetch_all(s_cursor)]
    emp_cursor = db.execute('''
        SELECT EM.nome, FE.designacao
        FROM DDL.Trabalha_Em TE
        JOIN DDL.Empregado EM ON TE.id_empregado = EM.id_empregado
        JOIN DDL.Funcao_Empregado FE ON EM.id_funcao_empregado = FE.id_funcao_empregado
        WHERE TE.id_evento = ?
    ''', (event_id,))
    empregados = [{'nome': r['nome'], 'funcao': r['designacao']} for r in fetch_all(emp_cursor)]

    return {
        'id': e['id_evento'],
        'cliente': e['cliente_nome'],
        'cliente_nif': e['cliente_nif'],
        'cliente_tipo': e['cliente_tipo'],
        'cliente_cp': e['cliente_cp'],
        'cliente_localidade': e['cliente_localidade'],
        'tipo': e['tipo_evento'],
        'data': e['data_evento'].isoformat() if isinstance(e['data_evento'], datetime) else str(e['data_evento']),
        'pessoas': e['nr_pessoas'],
        'local': e['morada'],
        'menuId': e['id_menu'],
        'servicos': servs,
        'empregados': empregados
    }

def get_tipos_evento():
    db = get_db()
    cursor = db.execute('SELECT descricao FROM DDL.Tipo_evento WHERE isdeleted = 0')
    tipos_db = fetch_all(cursor)
    
    configs = {
        'casamento': {'emoji': '💍', 'corFundo': '#FDF2F8', 'corBorda': '#FBCFE8', 'corTexto': '#9D174D'},
        'batizado': {'emoji': '🕊️', 'corFundo': '#F0FDF4', 'corBorda': '#BBF7D0', 'corTexto': '#166534'},
        'evento empresarial': {'emoji': '💼', 'corFundo': '#EFF6FF', 'corBorda': '#BFDBFE', 'corTexto': '#1E3A8A'},
        'aniversário': {'emoji': '🎂', 'corFundo': '#FFFBEB', 'corBorda': '#FEF08A', 'corTexto': '#854D0E'},
        'conferência': {'emoji': '🎤', 'corFundo': '#F3E8FF', 'corBorda': '#D8B4FE', 'corTexto': '#6B21A8'},
        'jantar de gala': {'emoji': '🥂', 'corFundo': '#FEF2F2', 'corBorda': '#FECACA', 'corTexto': '#991B1B'},
        'workshop': {'emoji': '🛠️', 'corFundo': '#ECFEFF', 'corBorda': '#A5F3FC', 'corTexto': '#155E75'}
    }
    
    res = {}
    for t in tipos_db:
        desc = t['descricao']
        desc_lower = desc.lower().replace('á', 'a').replace('â', 'a').replace('é', 'e').replace('ê', 'e')
        # Simple fuzzy match for "empresarial", "aniversário"
        matched = False
        for k, v in configs.items():
            if k.replace('á', 'a') in desc_lower:
                res[desc] = v.copy()
                res[desc]['label'] = desc
                matched = True
                break
        
        if not matched:
            res[desc] = {
                'label': desc, 
                'emoji': '📅', 
                'corFundo': '#F3F4F6', 
                'corBorda': '#D1D5DB', 
                'corTexto': '#374151'
            }
    
    # If db is empty, return a default so it doesn't break
    if not res:
        res['Corporate / Empresa'] = {'label': 'Corporate / Empresa', 'emoji': '💼', 'corFundo': '#EFF6FF', 'corBorda': '#BFDBFE', 'corTexto': '#1E3A8A'}
    return res

def get_servicos():
    db = get_db()
    cursor = db.execute('SELECT descricao FROM DDL.Servico WHERE isdeleted = 0')
    servs = fetch_all(cursor)
    return [(row['descricao'], row['descricao']) for row in servs]

def get_or_create_cliente(db, nome, nif, tipo, cp, localidade):
    cursor = db.execute('SELECT id_cliente FROM DDL.Cliente WHERE NIF = ?', (nif,))
    row = fetch_one(cursor)
    if row:
        db.execute('UPDATE DDL.Cliente SET nome = ?, tipo_cliente = ?, codigo_postal = ?, localidade = ? WHERE NIF = ?', (nome, tipo, cp, localidade, nif))
        db.commit()
        return row['id_cliente']
    db.execute('INSERT INTO DDL.Cliente (nome, NIF, tipo_cliente, codigo_postal, localidade) VALUES (?, ?, ?, ?, ?)', (nome, nif, tipo, cp, localidade))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def get_or_create_tipo_evento(db, descricao):
    cursor = db.execute('SELECT id_tipo_evento FROM DDL.Tipo_evento WHERE descricao = ?', (descricao,))
    row = fetch_one(cursor)
    if row:
        return row['id_tipo_evento']
    db.execute('INSERT INTO DDL.Tipo_evento (descricao) VALUES (?)', (descricao,))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def get_or_create_servico(db, descricao):
    cursor = db.execute('SELECT id_servico FROM DDL.Servico WHERE descricao = ?', (descricao,))
    row = fetch_one(cursor)
    if row:
        return row['id_servico']
    db.execute('INSERT INTO DDL.Servico (descricao, custo) VALUES (?, 0)', (descricao,))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def save_evento(db, form, event_id=None):
    id_cliente = get_or_create_cliente(db, form['cliente'], form['cliente_nif'], form['cliente_tipo'], form['cliente_cp'], form['cliente_localidade'])
    id_tipo_evento = get_or_create_tipo_evento(db, form['tipo'])
    nr_pessoas = int(form['pessoas']) if form['pessoas'].isdigit() else 1
    
    data_sql = form['data'].replace('T', ' ')
    if len(data_sql) == 16:
        data_sql += ':00'
    
    if event_id:
        db.execute(
            '''
            UPDATE DDL.Evento
            SET id_cliente = ?, id_menu = ?, id_tipo_evento = ?, morada = ?, data_evento = ?, nr_pessoas = ?
            WHERE id_evento = ?
            ''',
            (
                id_cliente,
                int(form['menu_id']),
                id_tipo_evento,
                form['local'],
                data_sql,
                nr_pessoas,
                int(event_id)
            )
        )
        db.execute('UPDATE DDL.Servico_Evento SET isdeleted = 1 WHERE id_evento = ?', (int(event_id),))
        db.commit()
        e_id = int(event_id)
    else:
        db.execute(
            '''
            INSERT INTO DDL.Evento (id_cliente, id_menu, id_tipo_evento, morada, data_evento, nr_pessoas, duracao, custo, margem)
            VALUES (?, ?, ?, ?, ?, ?, 1, 0, 0)
            ''',
            (
                id_cliente,
                int(form['menu_id']),
                id_tipo_evento,
                form['local'],
                data_sql,
                nr_pessoas
            )
        )
        db.commit()
        e_id = fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

    for serv in form['servicos']:
        id_serv = get_or_create_servico(db, serv)
        cursor = db.execute('SELECT * FROM DDL.Servico_Evento WHERE id_evento = ? AND id_servico = ?', (e_id, id_serv))
        if fetch_one(cursor):
            db.execute('UPDATE DDL.Servico_Evento SET isdeleted = 0 WHERE id_evento = ? AND id_servico = ?', (e_id, id_serv))
        else:
            db.execute('INSERT INTO DDL.Servico_Evento (id_evento, id_servico) VALUES (?, ?)', (e_id, id_serv))
    db.commit()

def get_event_inventory(event_id):
    db = get_db()
    cursor = db.execute('SELECT nr_pessoas, id_menu FROM DDL.Evento WHERE id_evento = ? AND isdeleted = 0', (event_id,))
    evento = fetch_one(cursor)
    if not evento:
        return []

    nr_pessoas = evento['nr_pessoas'] or 1
    menu_id = evento['id_menu']

    pratos_cursor = db.execute('''
        SELECT I.id_ingrediente, I.nome as ingrediente_nome, CP.quantidade
        FROM DDL.Constituicao_Menu_Pratos CMP
        JOIN DDL.Constituicao_Prato CP ON CMP.id_prato = CP.id_prato
        JOIN DDL.Ingrediente I ON CP.id_ingrediente = I.id_ingrediente
        WHERE CMP.id_menu = ? AND CMP.isdeleted = 0
    ''', (menu_id,))
    pratos_resultados = fetch_all(pratos_cursor)
    
    bebidas_cursor = db.execute('''
        SELECT I.id_ingrediente, I.nome as ingrediente_nome, CB.quantidade
        FROM DDL.Constituicao_Menu_Bebidas CMB
        JOIN DDL.Constituicao_Bebida CB ON CMB.id_bebida = CB.id_bebida
        JOIN DDL.Ingrediente I ON CB.id_ingrediente = I.id_ingrediente
        WHERE CMB.id_menu = ? AND CMB.isdeleted = 0
    ''', (menu_id,))
    bebidas_resultados = fetch_all(bebidas_cursor)

    ingredientes = {}
    
    for r in pratos_resultados:
        i_id = r['id_ingrediente']
        if i_id not in ingredientes:
            ingredientes[i_id] = {'nome': r['ingrediente_nome'], 'qtd_unitaria': 0}
        ingredientes[i_id]['qtd_unitaria'] += (r['quantidade'] or 0)
        
    for r in bebidas_resultados:
        i_id = r['id_ingrediente']
        if i_id not in ingredientes:
            ingredientes[i_id] = {'nome': r['ingrediente_nome'], 'qtd_unitaria': 0}
        ingredientes[i_id]['qtd_unitaria'] += (r['quantidade'] or 0)
        
    res = []
    for k, v in ingredientes.items():
        total = v['qtd_unitaria'] * nr_pessoas
        res.append({
            'id': k,
            'nome': v['nome'],
            'qtd_unitaria': v['qtd_unitaria'],
            'total': total
        })
        
    res.sort(key=lambda x: x['nome'])
    return res

def delete_evento(db, event_id):
    db.execute('UPDATE DDL.Evento SET isdeleted = 1 WHERE id_evento = ?', (event_id,))
    db.commit()
