function HomePage({ onNavigate }) {
  const modules = [
    {
      key: "employees",
      title: "Colaboradores",
      description: "Consulte a base, filtros e divergencias entre sistemas.",
      buttonLabel: "Abrir colaboradores",
    },
    {
      key: "stores",
      title: "Lojas",
      description: "Veja quadro contratado, headcount e detalhes por unidade.",
      buttonLabel: "Abrir lojas",
    },
    {
      key: "imports",
      title: "Importacoes",
      description: "Envie planilhas de Tabela Mae, TOTVS e Gestao de Pessoas.",
      buttonLabel: "Abrir importacoes",
    },
    {
      key: "dismissals",
      title: "Demissoes",
      description: "Espaco reservado para o modulo de desligamentos.",
      buttonLabel: "Abrir demissoes",
    },
    {
      key: "reports",
      title: "Relatorios",
      description: "Area futura para analises e consolidacoes gerenciais.",
      buttonLabel: "Abrir relatorios",
    },
  ];

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Inicio</span>
          <h1>Central de modulos</h1>
          <p>Escolha abaixo para qual area do sistema voce quer ir.</p>
        </div>
      </div>

      <div className="home-module-grid">
        {modules.map((module) => (
          <article className="home-module-card" key={module.key}>
            <h2>{module.title}</h2>
            <p>{module.description}</p>

            <button
              type="button"
              className="home-module-button"
              onClick={() => onNavigate(module.key)}
            >
              {module.buttonLabel}
            </button>
          </article>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
