from datetime import datetime
from .database import get_db, fetch_all, fetch_one

def get_events():
    db = get_db()
    cursor = db.execute('''
        SELECT E.*, C.nome as cliente_nome, TE.descricao as tipo_evento
        FROM Evento E
        JOIN Cliente C ON E.id_cliente = C.id_cliente
        JOIN Tipo_evento TE ON E.id_tipo_evento = TE.id_tipo_evento
        WHERE E.isdeleted = 0
        ORDER BY E.id_evento DESC
    ''')
    events = fetch_all(cursor)
    res = []
    for e in events:
        s_cursor = db.execute('''
            SELECT S.descricao 
            FROM Servico_Evento SE
            JOIN Servico S ON SE.id_servico = S.id_servico
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
        SELECT E.*, C.nome as cliente_nome, C.NIF as cliente_nif, C.tipo_cliente as cliente_tipo, TE.descricao as tipo_evento
        FROM Evento E
        JOIN Cliente C ON E.id_cliente = C.id_cliente
        JOIN Tipo_evento TE ON E.id_tipo_evento = TE.id_tipo_evento
        WHERE E.id_evento = ? AND E.isdeleted = 0
    ''', (event_id,))
    e = fetch_one(cursor)
    if not e:
        return None
    s_cursor = db.execute('''
        SELECT S.descricao 
        FROM Servico_Evento SE
        JOIN Servico S ON SE.id_servico = S.id_servico
        WHERE SE.id_evento = ? AND SE.isdeleted = 0 AND S.isdeleted = 0
    ''', (event_id,))
    servs = [row['descricao'] for row in fetch_all(s_cursor)]
    return {
        'id': e['id_evento'],
        'cliente': e['cliente_nome'],
        'cliente_nif': e['cliente_nif'],
        'cliente_tipo': e['cliente_tipo'],
        'tipo': e['tipo_evento'],
        'data': e['data_evento'].isoformat() if isinstance(e['data_evento'], datetime) else str(e['data_evento']),
        'pessoas': e['nr_pessoas'],
        'local': e['morada'],
        'menuId': e['id_menu'],
        'servicos': servs
    }

def get_tipos_evento():
    db = get_db()
    cursor = db.execute('SELECT descricao FROM Tipo_evento WHERE isdeleted = 0')
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
    cursor = db.execute('SELECT descricao FROM Servico WHERE isdeleted = 0')
    servs = fetch_all(cursor)
    return [(row['descricao'], row['descricao']) for row in servs]

def get_or_create_cliente(db, nome, nif, tipo):
    cursor = db.execute('SELECT id_cliente FROM Cliente WHERE NIF = ?', (nif,))
    row = fetch_one(cursor)
    if row:
        db.execute('UPDATE Cliente SET nome = ?, tipo_cliente = ? WHERE NIF = ?', (nome, tipo, nif))
        db.commit()
        return row['id_cliente']
    db.execute('INSERT INTO Cliente (nome, NIF, tipo_cliente) VALUES (?, ?, ?)', (nome, nif, tipo))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def get_or_create_tipo_evento(db, descricao):
    cursor = db.execute('SELECT id_tipo_evento FROM Tipo_evento WHERE descricao = ?', (descricao,))
    row = fetch_one(cursor)
    if row:
        return row['id_tipo_evento']
    db.execute('INSERT INTO Tipo_evento (descricao) VALUES (?)', (descricao,))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def get_or_create_servico(db, descricao):
    cursor = db.execute('SELECT id_servico FROM Servico WHERE descricao = ?', (descricao,))
    row = fetch_one(cursor)
    if row:
        return row['id_servico']
    db.execute('INSERT INTO Servico (descricao, custo) VALUES (?, 0)', (descricao,))
    db.commit()
    return fetch_one(db.execute('SELECT @@IDENTITY AS id'))['id']

def save_evento(db, form, event_id=None):
    id_cliente = get_or_create_cliente(db, form['cliente'], form['cliente_nif'], form['cliente_tipo'])
    id_tipo_evento = get_or_create_tipo_evento(db, form['tipo'])
    nr_pessoas = int(form['pessoas']) if form['pessoas'].isdigit() else 1
    
    data_sql = form['data'].replace('T', ' ')
    if len(data_sql) == 16:
        data_sql += ':00'
    
    if event_id:
        db.execute(
            '''
            UPDATE Evento
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
        db.execute('UPDATE Servico_Evento SET isdeleted = 1 WHERE id_evento = ?', (int(event_id),))
        db.commit()
        e_id = int(event_id)
    else:
        db.execute(
            '''
            INSERT INTO Evento (id_cliente, id_menu, id_tipo_evento, morada, data_evento, nr_pessoas, duracao, custo, margem)
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
        cursor = db.execute('SELECT * FROM Servico_Evento WHERE id_evento = ? AND id_servico = ?', (e_id, id_serv))
        if fetch_one(cursor):
            db.execute('UPDATE Servico_Evento SET isdeleted = 0 WHERE id_evento = ? AND id_servico = ?', (e_id, id_serv))
        else:
            db.execute('INSERT INTO Servico_Evento (id_evento, id_servico) VALUES (?, ?)', (e_id, id_serv))
    db.commit()

def delete_evento(db, event_id):
    db.execute('UPDATE Evento SET isdeleted = 1 WHERE id_evento = ?', (event_id,))
    db.commit()
