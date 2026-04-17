import Sidebar from "./Sidebar";

function AppLayout({ children, currentPage, onChangePage }) {
  return (
    <div className="app-shell">
      <Sidebar
        currentPage={currentPage}
        onChangePage={onChangePage}
      />

      <main className="app-main">
        <header className="topbar">
          <div>
            <strong>Sistema interno</strong>
            <span>Ambiente de gestão operacional</span>
          </div>

          <div className="user-pill">
            Usuário
          </div>
        </header>

        <section className="app-content">
          {children}
        </section>
      </main>
    </div>
  );
}

export default AppLayout;
