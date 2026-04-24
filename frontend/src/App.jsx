import { useEffect, useState } from "react";
import AppLayout from "./components/AppLayout";
import HomePage from "./pages/HomePage";
import EmployeesPage from "./pages/EmployeesPage";
import ImportsPage from "./pages/ImportsPage";
import PlaceholderPage from "./pages/PlaceholderPage";
import StoresPage from "./pages/StoresPage";
import "./App.css";

const VALID_PAGES = [
  "home",
  "employees",
  "stores",
  "dismissals",
  "imports",
  "reports",
];

function getPageFromHash() {
  const rawHash = window.location.hash.replace(/^#\/?/, "").trim();

  if (VALID_PAGES.includes(rawHash)) {
    return rawHash;
  }

  return "home";
}

function App() {
  const [currentPage, setCurrentPage] = useState(getPageFromHash);

  useEffect(() => {
    function handleHashChange() {
      setCurrentPage(getPageFromHash());
    }

    window.addEventListener("hashchange", handleHashChange);
    handleHashChange();

    return () => {
      window.removeEventListener("hashchange", handleHashChange);
    };
  }, []);

  function changePage(page) {
    const targetPage = VALID_PAGES.includes(page) ? page : "home";
    window.location.hash = `/${targetPage}`;
  }

  function renderPage() {
    if (currentPage === "home") {
      return <HomePage onNavigate={changePage} />;
    }

    if (currentPage === "employees") {
      return <EmployeesPage />;
    }

    if (currentPage === "stores") {
      return <StoresPage />;
    }

    if (currentPage === "dismissals") {
      return (
        <PlaceholderPage
          title="Demissoes"
          description="Acompanhamento de colaboradores demitidos e divergencias de desligamento."
        />
      );
    }

    if (currentPage === "imports") {
      return <ImportsPage />;
    }

    if (currentPage === "reports") {
      return (
        <PlaceholderPage
          title="Relatorios"
          description="Area futura para indicadores, graficos e analises gerenciais."
        />
      );
    }

    return <HomePage />;
  }

  return (
    <AppLayout currentPage={currentPage} onChangePage={changePage}>
      {renderPage()}
    </AppLayout>
  );
}

export default App;
