function HomePage({ employees, employeesLoading, stores, storesLoading }) {
  function getActiveEmployeesCountByStore(storeId) {
    return employees.filter((employee) => {
      return (
        employee.is_active &&
        employee.counts_in_store_headcount &&
        employee.store_id === storeId
      );
    }).length;
  }

  const analyzedStores = stores.map((store) => {
    const activeEmployees = getActiveEmployeesCountByStore(store.id);
    const contractedHeadcount = store.contracted_headcount || 0;
    const difference = activeEmployees - contractedHeadcount;

    let status = "balanced";

    if (difference > 0) {
      status = "excess";
    }

    if (difference < 0) {
      status = "deficit";
    }

    return {
      ...store,
      activeEmployees,
      contractedHeadcount,
      difference,
      status,
    };
  });

  const totalEmployees = employees.length;
  const totalStores = stores.length;

  const totalDeficitStores = analyzedStores.filter(
    (store) => store.status === "deficit"
  ).length;

  const totalExcessStores = analyzedStores.filter(
    (store) => store.status === "excess"
  ).length;

  const totalBalancedStores = analyzedStores.filter(
    (store) => store.status === "balanced"
  ).length;

  const totalContractedHeadcount = analyzedStores.reduce((total, store) => {
    return total + store.contractedHeadcount;
  }, 0);

  const totalActiveEmployeesInStores = analyzedStores.reduce((total, store) => {
    return total + store.activeEmployees;
  }, 0);

  const generalDifference = totalActiveEmployeesInStores - totalContractedHeadcount;

  if (employeesLoading || storesLoading) {
    return (
      <div className="module-loading">
        <h2>Carregando painel...</h2>
        <p>Sincronizando dados iniciais do sistema.</p>
      </div>
    );
  }

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Início</span>
          <h1>Painel Geral</h1>
          <p>Visão inicial dos módulos do Controle Operacional.</p>
        </div>
      </div>

      <div className="home-kpi-grid">
        <div className="home-kpi-card">
          <span>Colaboradores</span>
          <strong>{totalEmployees}</strong>
          <p>Colaboradores ativos na base operacional.</p>
        </div>

        <div className="home-kpi-card">
          <span>Lojas com quadro</span>
          <strong>{totalStores}</strong>
          <p>Lojas com headcount contratado maior que zero.</p>
        </div>

        <div className="home-kpi-card danger">
          <span>Lojas com déficit</span>
          <strong>{totalDeficitStores}</strong>
          <p>Abaixo do quadro contratado.</p>
        </div>

        <div className="home-kpi-card warning">
          <span>Lojas com excedente</span>
          <strong>{totalExcessStores}</strong>
          <p>Acima do quadro contratado.</p>
        </div>
      </div>

      <div className="home-section-grid">
        <div className="home-panel">
          <h2>Resumo de quadro</h2>

          <div className="home-summary-row">
            <span>Quadro contratado</span>
            <strong>{totalContractedHeadcount}</strong>
          </div>

          <div className="home-summary-row">
            <span>Ativos contabilizados</span>
            <strong>{totalActiveEmployeesInStores}</strong>
          </div>

          <div className="home-summary-row">
            <span>Diferença geral</span>
            <strong>{generalDifference}</strong>
          </div>
        </div>

        <div className="home-panel">
          <h2>Status das lojas</h2>

          <div className="home-summary-row">
            <span>No quadro</span>
            <strong>{totalBalancedStores}</strong>
          </div>

          <div className="home-summary-row">
            <span>Com déficit</span>
            <strong>{totalDeficitStores}</strong>
          </div>

          <div className="home-summary-row">
            <span>Com excedente</span>
            <strong>{totalExcessStores}</strong>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;