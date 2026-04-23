import { useState } from 'react';

export default function GestaoMenus({ menus, setMenus, colors, categoriasCatering }) {
  const [isAddingMenu, setIsAddingMenu] = useState(false);
  
  const estadoInicialMenu = {
    nome: '', entradas: { nome: '', ingredientes: '' }, pratoPrincipal: { nome: '', ingredientes: '' },
    acompanhamentos: { nome: '', ingredientes: '' }, sobremesa: { nome: '', ingredientes: '' },
    bebidas: { nome: '', ingredientes: '' }, ceia: { nome: '', ingredientes: '' }
  };
  const [newMenu, setNewMenu] = useState(estadoInicialMenu);

  const styles = {
    header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '30px' },
    title: { fontSize: '32px', margin: 0, fontWeight: '600', letterSpacing: '-0.5px' },
    card: { backgroundColor: colors.cardBg, padding: '25px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', marginBottom: '20px', border: `1px solid ${colors.border}` },
    sectionTitle: { fontSize: '12px', color: colors.textMuted, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '15px', fontWeight: '700' },
    input: { padding: '10px 12px', borderRadius: '4px', border: `1px solid ${colors.border}`, fontSize: '14px', outline: 'none', backgroundColor: '#FAFAFA', width: '100%', boxSizing: 'border-box' },
    label: { fontSize: '13px', fontWeight: '600', marginBottom: '6px', display: 'block', color: colors.textMain },
    button: { padding: '14px 28px', backgroundColor: colors.sidebarBg, color: '#FFFFFF', border: 'none', borderRadius: '4px', fontSize: '14px', fontWeight: '600', cursor: 'pointer', textTransform: 'uppercase', letterSpacing: '0.5px', transition: '0.2s' },
    buttonSecondary: { padding: '12px 24px', backgroundColor: 'transparent', color: colors.textMain, border: `1px solid ${colors.border}`, borderRadius: '4px', fontSize: '13px', fontWeight: '600', cursor: 'pointer', marginRight: '10px' },
    emptyState: { textAlign: 'center', padding: '80px 20px', color: colors.textMuted, fontSize: '16px' }
  };

  const handleSaveMenu = () => {
    if (!newMenu.nome) {
      alert("Por favor, dê um nome ao Menu principal.");
      return;
    }
    setMenus([...menus, { ...newMenu, id: Date.now() }]);
    setIsAddingMenu(false);
    setNewMenu(estadoInicialMenu);
  };

  return (
    <div>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Gestão de Menus & Catering</h1>
          <p style={{color: colors.textMuted, marginTop:'8px'}}>Configure os menus completos e os respetivos ingredientes.</p>
        </div>
        {!isAddingMenu && (
          <button style={{...styles.button, padding: '12px 24px'}} onClick={() => setIsAddingMenu(true)}>Adicionar Novo Menu</button>
        )}
      </div>

      {isAddingMenu ? (
        <div style={{maxWidth: '900px'}}>
          <div style={styles.card}>
            <h2 style={styles.sectionTitle}>Identificação Geral</h2>
            <input 
              style={styles.input} 
              placeholder="Nome do Menu Completo (ex: Menu Corporate Premium)" 
              value={newMenu.nome}
              onChange={(e) => setNewMenu({...newMenu, nome: e.target.value})}
            />
          </div>

          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
            {categoriasCatering.map((categoria) => (
              <div key={categoria.id} style={styles.card}>
                <h2 style={styles.sectionTitle}>{categoria.titulo}</h2>
                <label style={styles.label}>Descrição / Itens</label>
                <input 
                  style={{...styles.input, marginBottom: '12px'}} 
                  placeholder={categoria.placeholderNome}
                  value={newMenu[categoria.id].nome}
                  onChange={(e) => setNewMenu({ ...newMenu, [categoria.id]: { ...newMenu[categoria.id], nome: e.target.value } })}
                />
                <label style={styles.label}>Ingredientes (separados por vírgula)</label>
                <textarea 
                  style={{...styles.input, height: '60px', resize: 'vertical', fontFamily:'inherit'}} 
                  placeholder="Ex: Batata, Azeite, Sal, Alho..."
                  value={newMenu[categoria.id].ingredientes}
                  onChange={(e) => setNewMenu({ ...newMenu, [categoria.id]: { ...newMenu[categoria.id], ingredientes: e.target.value } })}
                />
              </div>
            ))}
          </div>

          <div style={{display:'flex', justifyContent:'flex-end', marginTop:'20px', paddingBottom:'40px'}}>
            <button style={styles.buttonSecondary} onClick={() => setIsAddingMenu(false)}>Cancelar</button>
            <button style={{...styles.button, backgroundColor: colors.accent}} onClick={handleSaveMenu}>Guardar Menu</button>
          </div>
        </div>
      ) : (
        menus.length === 0 ? (
          <div style={styles.emptyState}>
            Ainda não existem menus de catering configurados na plataforma.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '20px', maxWidth: '900px' }}>
            {menus.map(menu => (
              <div key={menu.id} style={{...styles.card, borderLeft: `4px solid ${colors.accent}`}}>
                <h3 style={{margin: '0 0 20px 0', fontSize: '18px', color: colors.textMain}}>{menu.nome}</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', fontSize: '13px' }}>
                  {categoriasCatering.map(cat => {
                    if (menu[cat.id].nome) {
                      return (
                        <div key={cat.id}>
                          <div style={{fontWeight: '600', color: colors.sidebarBg, marginBottom: '4px'}}>{cat.titulo}</div>
                          <div style={{color: colors.textMain}}>{menu[cat.id].nome}</div>
                          {menu[cat.id].ingredientes && (
                            <div style={{color: colors.textMuted, fontSize: '11px', marginTop: '4px'}}>
                              Ingredientes: {menu[cat.id].ingredientes}
                            </div>
                          )}
                        </div>
                      );
                    }
                    return null;
                  })}
                </div>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  );
}