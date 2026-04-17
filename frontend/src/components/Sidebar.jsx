function Sidebar({ currentPage, onChangePage }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">CO</div>

        <div>
          <strong>Controle</strong>
          <span>Operacional</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button
          className={currentPage === "home" ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChangePage("home")}
        >
          Início
        </button>

        <button
          className={currentPage === "employees" ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChangePage("employees")}
        >
          Colaboradores
        </button>

        <button
          className={currentPage === "stores" ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChangePage("stores")}
        >
          Lojas
        </button>

        <button
          className={currentPage === "dismissals" ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChangePage("dismissals")}
        >
          Demissões
        </button>

        <button
          className={currentPage === "imports" ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChangePage("imports")}
        >
          Importações
        </button>

        <button
          className={currentPage === "reports" ? "nav-item active" : "nav-item"}
          type="button"
          onClick={() => onChangePage("reports")}
        >
          Relatórios
        </button>
      </nav>
    </aside>
  );
}

export default Sidebar;