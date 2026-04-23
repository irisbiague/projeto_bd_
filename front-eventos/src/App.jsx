import { useState } from 'react';
import GestaoMenus from './components/GestaoMenus';
import CriarEvento from './components/CriarEvento';
import EventosMarcados from './components/EventosMarcados'; 
function App() {
  const [activeTab, setActiveTab] = useState('criar_evento'); 
  
  // O App.jsx guarda a lista de menus para poder passá-la a ambas as abas
  const [menus, setMenus] = useState([]);

  const colors = {
    sidebarBg: '#111827', sidebarText: '#9CA3AF', sidebarActiveBg: '#1F2937',
    accent: '#D4AF37', bg: '#F3F4F6', cardBg: '#FFFFFF',
    textMain: '#111827', textMuted: '#6B7280', border: '#E5E7EB',
  };

  const Icons = {
    dashboard: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>,
    calendar: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>,
    plus: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>,
    restaurant: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path><path d="M7 2v20"></path><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path></svg>,
    services: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20"></path><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>,
    box: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>,
    check: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
  };

  const categoriasCatering = [
    { id: 'entradas', titulo: 'Entradas e Aperitivos', placeholderNome: 'Ex: Tábua de Queijos...' }, 
    { id: 'pratoPrincipal', titulo: 'Prato Principal', placeholderNome: 'Ex: Lombo Assado...' },
    { id: 'acompanhamentos', titulo: 'Acompanhamentos', placeholderNome: 'Ex: Arroz Árabe...' }, 
    { id: 'sobremesa', titulo: 'Sobremesa', placeholderNome: 'Ex: Buffet de Doces...' },
    { id: 'bebidas', titulo: 'Serviço de Bebidas', placeholderNome: 'Ex: Vinhos do Douro...' }, 
    { id: 'ceia', titulo: 'Ceia / Snacks Extra', placeholderNome: 'Ex: Caldo Verde...' }
  ];

  const styles = {
    app: { display: 'flex', height: '100vh', fontFamily: '"Inter", sans-serif', backgroundColor: colors.bg, color: colors.textMain },
    sidebar: { width: '260px', backgroundColor: colors.sidebarBg, color: colors.sidebarText, display: 'flex', flexDirection: 'column' },
    logoContainer: { padding: '30px 20px', borderBottom: `1px solid ${colors.sidebarActiveBg}`, marginBottom: '20px' },
    logo: { fontSize: '22px', fontWeight: '300', color: '#FFFFFF', letterSpacing: '2px', textTransform: 'uppercase' },
    navItem: { display: 'flex', alignItems: 'center', gap: '12px', padding: '14px 24px', cursor: 'pointer', transition: '0.2s', fontWeight: '500', fontSize: '14px', borderLeft: '4px solid transparent' },
    navItemActive: { backgroundColor: colors.sidebarActiveBg, color: '#FFFFFF', borderLeft: `4px solid ${colors.accent}` },
    mainContent: { flex: 1, padding: '40px', overflowY: 'auto' }
  };

  const NavButton = ({ id, label, icon }) => (
    <div style={{ ...styles.navItem, ...(activeTab === id ? styles.navItemActive : {}) }} onClick={() => setActiveTab(id)}>
      {icon} <span>{label}</span>
    </div>
  );

  return (
    <div style={styles.app}>
      {/* MENU LATERAL */}
      <div style={styles.sidebar}>
        <div style={styles.logoContainer}>
          <div style={styles.logo}>Event<span style={{fontWeight:'700', color:colors.accent}}>Pro</span></div>
        </div>
        <NavButton id="dashboard" label="Visão Geral" icon={Icons.dashboard} />
        <NavButton id="eventos_marcados" label="Eventos Marcados" icon={Icons.calendar} />
        <NavButton id="criar_evento" label="Criar Evento" icon={Icons.plus} />
        <NavButton id="menus" label="Gestão de Menus" icon={Icons.restaurant} />
        <NavButton id="servicos" label="Serviços Associados" icon={Icons.services} />
        <NavButton id="stock" label="Gestão de Stock" icon={Icons.box} />
      </div>

      {/* ÁREA PRINCIPAL (Faz render do componente escolhido) */}
      <div style={styles.mainContent}>
        
        
        {activeTab === 'eventos_marcados' && (
          <EventosMarcados colors={colors} />
        )}
        {activeTab === 'menus' && (
          <GestaoMenus menus={menus} setMenus={setMenus} colors={colors} categoriasCatering={categoriasCatering} />
        )}

        {activeTab === 'criar_evento' && (
          <CriarEvento menus={menus} colors={colors} categoriasCatering={categoriasCatering} Icons={Icons} />
        )}

        {/* Placeholder para outras secções */}
        {activeTab !== 'menus' && activeTab !== 'criar_evento' && (
          <div style={{ textAlign: 'center', padding: '80px 20px', color: colors.textMuted, fontSize: '16px' }}>
            Módulo de {activeTab.replace('_', ' ')} em desenvolvimento...
          </div>
        )}

      </div>
    </div>
  );
}

export default App;