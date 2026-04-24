function ModuleIcon({ type }) {
  if (type === "stores") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M5 10h14" />
        <path d="M7 10V19h10v-9" />
        <path d="M4 7.5 6 4h12l2 3.5" />
      </svg>
    );
  }

  if (type === "employees") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="9" cy="9" r="3" />
        <path d="M4.5 18a4.5 4.5 0 0 1 9 0" />
        <circle cx="17" cy="10" r="2.5" />
        <path d="M14.5 18a3.6 3.6 0 0 1 5 0" />
      </svg>
    );
  }

  if (type === "dismissals") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M6 5h12" />
        <path d="M8 5v14h8V5" />
        <path d="M10 10h4" />
      </svg>
    );
  }

  if (type === "terminations") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M7 4h10" />
        <path d="M12 4v8" />
        <path d="M8.5 12a4 4 0 1 0 7 0" />
        <path d="M6 20h12" />
      </svg>
    );
  }

  if (type === "imports") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 5v9" />
        <path d="m8.5 10.5 3.5 3.5 3.5-3.5" />
        <path d="M5 18h14" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M6 6h12v12H6z" />
      <path d="M9 9h6" />
      <path d="M9 12h6" />
      <path d="M9 15h4" />
    </svg>
  );
}

function HomePage({ onNavigate }) {
  const moduleSections = [
    {
      title: "Gestao",
      accentClass: "blue",
      items: [
        {
          key: "stores",
          title: "Lojas",
          description: "Quadro contratado, headcount e comparacao por unidade.",
        },
        {
          key: "employees",
          title: "Colaboradores",
          description: "Compare TOTVS, Gestao e GeoVictoria no mesmo cadastro.",
        },
        {
          key: "dismissals",
          title: "Demissoes",
          description: "Consulte desligamentos e veja alinhamento entre bases.",
        },
        {
          key: "terminations",
          title: "Terminos",
          description: "Acompanhe prorrogar, manter e dar termino com historico.",
        },
      ],
    },
    {
      title: "Sistema",
      accentClass: "orange",
      items: [
        {
          key: "imports",
          title: "Importacoes",
          description: "Envie Tabela Mae, TOTVS e Gestao de Pessoas.",
        },
        {
          key: "reports",
          title: "Relatorios",
          description: "Area futura para consolidacoes e indicadores.",
        },
      ],
    },
  ];

  return (
    <div className="module-page">
      <section className="home-hero">
        <span className="home-hero-tag">Sistema de gestao</span>
        <h1>Ola, Administrador Local</h1>
        <p>Selecione um servico para gerenciar a operacao de forma simples e direta.</p>
      </section>

      {moduleSections.map((section) => (
        <section className="home-section" key={section.title}>
          <div className={`home-section-header ${section.accentClass}`}>
            <span>{section.title}</span>
          </div>

          <div className="home-module-grid">
            {section.items.map((module) => (
              <article className="home-module-card" key={module.key}>
                <div className="home-module-icon">
                  <ModuleIcon type={module.key} />
                </div>

                <div className="home-module-copy">
                  <h2>{module.title}</h2>
                  <p>{module.description}</p>
                </div>

                <button
                  type="button"
                  className="home-module-button"
                  onClick={() => onNavigate(module.key)}
                  aria-label={`Abrir ${module.title}`}
                >
                  <span />
                </button>
              </article>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}

export default HomePage;
