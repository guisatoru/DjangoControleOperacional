function HomePage() {
  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Início</span>
          <h1>Painel Geral</h1>
          <p>Visão inicial dos módulos do Controle Operacional.</p>
        </div>
      </div>

      <div className="home-grid">
        <div className="home-card">
          <span>Colaboradores</span>
          <strong>Base operacional</strong>
          <p>Consulta, filtros e divergências entre TOTVS, Gestão e GeoVictoria.</p>
        </div>

        <div className="home-card">
          <span>Lojas</span>
          <strong>Estrutura de unidades</strong>
          <p>Acompanhe lojas, centros de custo, supervisores e quadro contratado.</p>
        </div>

        <div className="home-card">
          <span>Importações</span>
          <strong>Atualização de dados</strong>
          <p>Importe arquivos da Tabela Mãe, TOTVS e Gestão de Pessoas.</p>
        </div>

        <div className="home-card">
          <span>Relatórios</span>
          <strong>Análises operacionais</strong>
          <p>Área futura para indicadores, gráficos e painéis gerenciais.</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
