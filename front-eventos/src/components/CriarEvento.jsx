import { useState } from 'react';

export default function CriarEvento({ menus, colors, categoriasCatering, Icons }) {
  const [novoEvento, setNovoEvento] = useState({
    cliente: '', data: '', pessoas: '', local: '', menuId: '', servicos: []
  });

  const styles = {
    header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '30px' },
    title: { fontSize: '32px', margin: 0, fontWeight: '600', letterSpacing: '-0.5px' },
    card: { backgroundColor: colors.cardBg, padding: '25px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', marginBottom: '20px', border: `1px solid ${colors.border}` },
    sectionTitle: { fontSize: '12px', color: colors.textMuted, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '15px', fontWeight: '700' },
    input: { padding: '10px 12px', borderRadius: '4px', border: `1px solid ${colors.border}`, fontSize: '14px', outline: 'none', backgroundColor: '#FAFAFA', width: '100%', boxSizing: 'border-box' },
    label: { fontSize: '13px', fontWeight: '600', marginBottom: '6px', display: 'block', color: colors.textMain },
    button: { padding: '14px 28px', backgroundColor: colors.sidebarBg, color: '#FFFFFF', border: 'none', borderRadius: '4px', fontSize: '14px', fontWeight: '600', cursor: 'pointer', textTransform: 'uppercase', letterSpacing: '0.5px', transition: '0.2s' },
    serviceCard: { padding: '15px', borderRadius: '6px', border: `2px solid ${colors.border}`, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px', transition: 'all 0.2s' },
    serviceCardActive: { borderColor: colors.accent, backgroundColor: '#FDFBF4' }
  };

  const toggleServico = (servicoId) => {
    if (novoEvento.servicos.includes(servicoId)) {
      setNovoEvento({ ...novoEvento, servicos: novoEvento.servicos.filter(id => id !== servicoId) });
    } else {
      setNovoEvento({ ...novoEvento, servicos: [...novoEvento.servicos, servicoId] });
    }
  };

  const menuSelecionadoInfo = menus.find(m => m.id.toString() === novoEvento.menuId);

  return (
    <div style={{ maxWidth: '900px' }}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Planear Novo Evento</h1>
          <p style={{color: colors.textMuted, marginTop:'8px'}}>Preencha a ficha técnica para agendar a organização.</p>
        </div>
      </div>

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>1. Informações do Cliente e Local</h2>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div>
            <label style={styles.label}>Cliente / Empresa</label>
            <input style={styles.input} placeholder="Nome do cliente" value={novoEvento.cliente} onChange={e => setNovoEvento({...novoEvento, cliente: e.target.value})} />
          </div>
          <div>
            <label style={styles.label}>Data e Hora do Evento</label>
            <input style={styles.input} type="datetime-local" value={novoEvento.data} onChange={e => setNovoEvento({...novoEvento, data: e.target.value})} />
          </div>
          <div>
            <label style={styles.label}>Nº de Pessoas (Estimativa)</label>
            <input style={styles.input} type="number" placeholder="Ex: 150" value={novoEvento.pessoas} onChange={e => setNovoEvento({...novoEvento, pessoas: e.target.value})} />
          </div>
          <div>
            <label style={styles.label}>Morada do Evento</label>
            <input style={styles.input} placeholder="Localização exata" value={novoEvento.local} onChange={e => setNovoEvento({...novoEvento, local: e.target.value})} />
          </div>
        </div>
      </div>

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>2. Alimentação & Catering</h2>
        <label style={styles.label}>Menu Selecionado</label>
        <select 
          style={{...styles.input, cursor: 'pointer', backgroundColor: novoEvento.menuId ? '#FDFBF4' : '#FAFAFA', borderColor: novoEvento.menuId ? colors.accent : colors.border}}
          value={novoEvento.menuId}
          onChange={e => setNovoEvento({...novoEvento, menuId: e.target.value})}
        >
          <option value="">Sem menu atribuído (Selecione um menu...)</option>
          {menus.map(m => <option key={m.id} value={m.id}>{m.nome}</option>)}
        </select>
        
        {menus.length === 0 && <p style={{fontSize:'12px', color:'#e74c3c', marginTop:'8px'}}>Não existem menus criados. Vá a "Gestão de Menus" primeiro.</p>}

        {menuSelecionadoInfo && (
          <div style={{marginTop: '20px', padding: '15px', backgroundColor: colors.bg, borderRadius: '6px', borderLeft: `3px solid ${colors.accent}`}}>
            <div style={{fontSize: '12px', fontWeight: 'bold', color: colors.textMuted, marginBottom: '10px'}}>RESUMO DO MENU:</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '13px' }}>
              {categoriasCatering.map(cat => menuSelecionadoInfo[cat.id]?.nome ? (
                <div key={cat.id}><span style={{fontWeight: '600'}}>{cat.titulo}:</span> {menuSelecionadoInfo[cat.id].nome}</div>
              ) : null)}
            </div>
          </div>
        )}
      </div>

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>3. Logística e Serviços Extra</h2>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '15px'}}>
          {['bar', 'limpeza', 'staff'].map((servico, index) => {
            const nomes = ['Serviço de Bar Aberto', 'Equipa de Limpeza', 'Staff de Bengaleiro'];
            const isAtivo = novoEvento.servicos.includes(servico);
            return (
              <div key={servico} style={{...styles.serviceCard, ...(isAtivo ? styles.serviceCardActive : {})}} onClick={() => toggleServico(servico)}>
                <div style={{width: '20px', height: '20px', borderRadius: '4px', border: `1px solid ${isAtivo ? colors.accent : colors.border}`, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: isAtivo ? colors.accent : 'transparent', color: 'white'}}>
                  {isAtivo && Icons.check}
                </div>
                <span style={{fontSize: '14px', fontWeight: '500'}}>{nomes[index]}</span>
              </div>
            );
          })}
        </div>
      </div>

      <div style={{display: 'flex', justifyContent: 'flex-end', marginTop: '20px', paddingBottom: '40px'}}>
        <button style={styles.button} onClick={() => alert('Evento guardado!')}>Confirmar e Agendar Evento</button>
      </div>
    </div>
  );
}