import { useState } from 'react';

export default function EventosMarcados({ colors }) {
  // Estado para controlar o mês e ano atuais que estamos a visualizar
  // Começa no mês atual (ex: Maio 2026)
  const [dataAtual, setDataAtual] = useState(new Date(2026, 4, 1)); // Mês 4 é Maio (Janeiro = 0)

  const tiposEvento = {
    casamento: { label: 'Casamento', emoji: '💍', corFundo: '#FDF2F8', corBorda: '#FBCFE8', corTexto: '#9D174D' },
    batizado: { label: 'Batizado', emoji: '🕊️', corFundo: '#F0FDF4', corBorda: '#BBF7D0', corTexto: '#166534' },
    corporate: { label: 'Corporate / Empresa', emoji: '💼', corFundo: '#EFF6FF', corBorda: '#BFDBFE', corTexto: '#1E3A8A' },
    jantar: { label: 'Jantar / Festa', emoji: '🥂', corFundo: '#FFFBEB', corBorda: '#FEF08A', corTexto: '#854D0E' }
  };

  // Base de dados simulada com datas completas (Ano-Mês-Dia)
  const eventos = [
    { id: 1, data: '2026-05-04', tipo: 'corporate', titulo: 'Conferência Tech UA' },
    { id: 2, data: '2026-05-12', tipo: 'casamento', titulo: 'Casamento Joana & Rui' },
    { id: 3, data: '2026-05-28', tipo: 'corporate', titulo: 'Team Building' },
    { id: 4, data: '2026-05-28', tipo: 'jantar', titulo: 'Gala de Beneficência' },
    { id: 5, data: '2026-06-15', tipo: 'jantar', titulo: 'Aniversário 50 Anos' }, // Evento no mês seguinte
    { id: 6, data: '2026-04-20', tipo: 'batizado', titulo: 'Batizado do Tomás' }  // Evento no mês anterior
  ];

  const diasDaSemana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  const mesesDoAno = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

  // Lógica de cálculo do Calendário Dinâmico
  const ano = dataAtual.getFullYear();
  const mes = dataAtual.getMonth();

  // Descobre quantos dias tem este mês (ao pedir o dia 0 do mês seguinte, ele dá o último dia deste mês)
  const totalDiasNoMes = new Date(ano, mes + 1, 0).getDate();
  
  // Descobre em que dia da semana (0=Dom, 6=Sáb) o mês começa
  const primeiroDiaDaSemana = new Date(ano, mes, 1).getDay();

  // Arrays para renderizar a grelha
  const diasDoMes = Array.from({ length: totalDiasNoMes }, (_, i) => i + 1);
  const espacosVaziosInicio = Array.from({ length: primeiroDiaDaSemana }, (_, i) => i);

  // Funções para navegar nos meses
  const mesAnterior = () => setDataAtual(new Date(ano, mes - 1, 1));
  const mesSeguinte = () => setDataAtual(new Date(ano, mes + 1, 1));
  const irParaHoje = () => setDataAtual(new Date());

  const styles = {
    header: { marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' },
    title: { fontSize: '32px', margin: 0, fontWeight: '600', letterSpacing: '-0.5px', color: colors.textMain },
    subtitle: { color: colors.textMuted, marginTop: '8px' },
    calendarContainer: { backgroundColor: colors.cardBg, borderRadius: '12px', border: `1px solid ${colors.border}`, padding: '25px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' },
    monthHeaderContainer: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' },
    monthTitle: { fontSize: '22px', fontWeight: 'bold', color: colors.textMain, textTransform: 'uppercase', letterSpacing: '1px' },
    navButton: { display: 'flex', alignItems: 'center', justifyContent: 'center', width: '36px', height: '36px', borderRadius: '50%', border: `1px solid ${colors.border}`, backgroundColor: '#FFFFFF', cursor: 'pointer', color: colors.textMain, transition: '0.2s' },
    todayButton: { padding: '8px 16px', borderRadius: '6px', border: `1px solid ${colors.border}`, backgroundColor: '#FFFFFF', cursor: 'pointer', fontSize: '13px', fontWeight: '600', color: colors.textMain },
    gridConfig: { display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '10px' },
    dayHeader: { textAlign: 'center', fontWeight: '700', color: colors.sidebarBg, fontSize: '13px', paddingBottom: '10px', textTransform: 'uppercase' },
    dayCell: { minHeight: '120px', padding: '8px', border: `1px solid ${colors.border}`, borderRadius: '6px', backgroundColor: '#FAFAFA', display: 'flex', flexDirection: 'column', gap: '4px', transition: 'border-color 0.2s' },
    dayCellEmpty: { minHeight: '120px', padding: '8px', borderRadius: '6px', backgroundColor: 'transparent' },
    dayNumber: { fontSize: '14px', fontWeight: '600', color: colors.textMuted, alignSelf: 'flex-end', marginBottom: '5px' },
    eventBadge: { fontSize: '11px', padding: '4px 6px', borderRadius: '4px', border: '1px solid', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', fontWeight: '600', cursor: 'pointer', boxShadow: '0 1px 2px rgba(0,0,0,0.05)' },
    legendContainer: { display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '30px', padding: '20px', backgroundColor: colors.bg, borderRadius: '8px', border: `1px solid ${colors.border}` },
    legendItem: { display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', fontWeight: '500', color: colors.textMain }
  };

  return (
    <div style={{ maxWidth: '1100px' }}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Calendário de Eventos</h1>
          <p style={styles.subtitle}>Visão geral dos eventos agendados.</p>
        </div>
      </div>

      <div style={styles.calendarContainer}>
        {/* CABEÇALHO DO MÊS COM NAVEGAÇÃO */}
        <div style={styles.monthHeaderContainer}>
          <button style={styles.todayButton} onClick={irParaHoje} onMouseOver={(e) => e.currentTarget.style.backgroundColor = colors.bg} onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#FFFFFF'}>
            Ir para Hoje
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <button style={styles.navButton} onClick={mesAnterior} onMouseOver={(e) => e.currentTarget.style.backgroundColor = colors.bg} onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#FFFFFF'}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>
            
            <div style={styles.monthTitle}>
              {mesesDoAno[mes]} <span style={{ color: colors.accent }}>{ano}</span>
            </div>
            
            <button style={styles.navButton} onClick={mesSeguinte} onMouseOver={(e) => e.currentTarget.style.backgroundColor = colors.bg} onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#FFFFFF'}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>
          
          {/* Espaçador invisível para centrar o título perfeitamente */}
          <div style={{ width: '100px' }}></div> 
        </div>

        {/* GRELHA DO CALENDÁRIO */}
        <div style={styles.gridConfig}>
          {/* Dias da Semana */}
          {diasDaSemana.map(dia => (
            <div key={dia} style={styles.dayHeader}>{dia}</div>
          ))}

          {/* Células Vazias (Offset do início do mês) */}
          {espacosVaziosInicio.map(index => (
            <div key={`empty-${index}`} style={styles.dayCellEmpty}></div>
          ))}

          {/* Células dos Dias */}
          {diasDoMes.map(dia => {
            // Cria a string da data atual (ex: "2026-05-04") para comparar com a base de dados
            // O padStart(2, '0') garante que o dia 4 fica '04' para o formato bater certo
            const dataString = `${ano}-${String(mes + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;
            
            // Filtra os eventos que correspondem exatamente a este dia, mês e ano
            const eventosHoje = eventos.filter(e => e.data === dataString);
            
            return (
              <div key={dia} style={styles.dayCell} onMouseOver={(e) => e.currentTarget.style.borderColor = colors.accent} onMouseOut={(e) => e.currentTarget.style.borderColor = colors.border}>
                <div style={styles.dayNumber}>{dia}</div>
                
                {/* Renderiza os emblemas dos eventos */}
                {eventosHoje.map(evento => {
                  const config = tiposEvento[evento.tipo];
                  return (
                    <div 
                      key={evento.id} 
                      style={{
                        ...styles.eventBadge, 
                        backgroundColor: config.corFundo, 
                        borderColor: config.corBorda, 
                        color: config.corTexto 
                      }}
                      title={evento.titulo}
                    >
                      {config.emoji} {evento.titulo}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>

      {/* LEGENDA EXPLICATIVA */}
      <div style={styles.legendContainer}>
        <span style={{ fontWeight: 'bold', color: colors.textMuted, textTransform: 'uppercase', fontSize: '12px', display: 'flex', alignItems: 'center' }}>
          Legenda:
        </span>
        {Object.keys(tiposEvento).map(chave => {
          const config = tiposEvento[chave];
          return (
            <div key={chave} style={styles.legendItem}>
              <div style={{ width: '18px', height: '18px', borderRadius: '4px', backgroundColor: config.corFundo, border: `1px solid ${config.corBorda}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px' }}>
                {config.emoji}
              </div>
              {config.label}
            </div>
          );
        })}
      </div>

    </div>
  );
}