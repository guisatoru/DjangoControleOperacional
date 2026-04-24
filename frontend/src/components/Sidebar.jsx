const NAV_SECTIONS = [
  {
    title: "Inicio",
    icon: "home",
    items: [
      { key: "home", label: "Painel Geral" },
    ],
  },
  {
    title: "Gestao",
    icon: "grid",
    items: [
      { key: "stores", label: "Lojas" },
      { key: "employees", label: "Colaboradores" },
      { key: "dismissals", label: "Demissoes" },
      { key: "terminations", label: "Terminos" },
    ],
  },
  {
    title: "Sistema",
    icon: "settings",
    items: [
      { key: "imports", label: "Importacoes" },
      { key: "reports", label: "Relatorios" },
    ],
  },
];

function BrandIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <rect x="4" y="4" width="16" height="16" rx="4" />
      <path d="M8 9h8" />
      <path d="M8 12h8" />
      <path d="M8 15h5" />
    </svg>
  );
}

function SectionIcon({ type }) {
  if (type === "home") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 11.5 12 5l8 6.5" />
        <path d="M7 10.5V19h10v-8.5" />
      </svg>
    );
  }

  if (type === "settings") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z" />
        <path d="M4.5 12h2.2" />
        <path d="M17.3 12h2.2" />
        <path d="M12 4.5v2.2" />
        <path d="M12 17.3v2.2" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <rect x="4" y="4" width="6" height="6" rx="1.5" />
      <rect x="14" y="4" width="6" height="6" rx="1.5" />
      <rect x="4" y="14" width="6" height="6" rx="1.5" />
      <rect x="14" y="14" width="6" height="6" rx="1.5" />
    </svg>
  );
}

function ChevronIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="m9 6 6 6-6 6" />
    </svg>
  );
}

function Sidebar({ currentPage, onChangePage }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <BrandIcon />
          </div>

          <div className="sidebar-brand-copy">
            <strong>Suporte Operacional</strong>
            <span>Atividades Diarias</span>
          </div>

          <div className="sidebar-brand-chevron">
            <ChevronIcon />
          </div>
        </div>

        <span className="sidebar-section-label">Plataforma</span>

        <nav className="sidebar-nav">
          {NAV_SECTIONS.map((section) => (
            <div className="sidebar-group" key={section.title}>
              <button
                className={
                  section.items.some((item) => item.key === currentPage)
                    ? "nav-section active"
                    : "nav-section"
                }
                type="button"
                onClick={() => onChangePage(section.items[0].key)}
              >
                <span className="nav-section-main">
                  <span className="nav-section-icon">
                    <SectionIcon type={section.icon} />
                  </span>
                  <span>{section.title}</span>
                </span>
                <span className="nav-section-arrow">
                  <ChevronIcon />
                </span>
              </button>

              <div className="sidebar-subnav">
                {section.items.map((item) => (
                  <button
                    key={item.key}
                    className={currentPage === item.key ? "nav-item active" : "nav-item"}
                    type="button"
                    onClick={() => onChangePage(item.key)}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </nav>
      </div>

      <div className="sidebar-user-card">
        <div className="sidebar-user-avatar">AL</div>

        <div>
          <strong>Administrador Local</strong>
          <span>admin@empresa.local</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
