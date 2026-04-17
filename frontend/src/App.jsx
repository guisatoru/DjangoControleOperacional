import { useEffect, useState } from "react";
import AppLayout from "./components/AppLayout";
import HomePage from "./pages/HomePage";
import EmployeesPage from "./pages/EmployeesPage";
import PlaceholderPage from "./pages/PlaceholderPage";
import StoresPage from "./pages/StoresPage";
import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  const [employees, setEmployees] = useState([]);
  const [employeesLoading, setEmployeesLoading] = useState(true);
  const [employeesError, setEmployeesError] = useState("");

  const [stores, setStores] = useState([]);
  const [storesLoading, setStoresLoading] = useState(true);
  const [storesError, setStoresError] = useState("");

  useEffect(() => {
    loadEmployees();
    loadStores();
  }, []);

  function loadEmployees() {
    setEmployeesLoading(true);
    setEmployeesError("");

    fetch("http://127.0.0.1:8000/api/employees/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar colaboradores.");
        }

        return response.json();
      })
      .then((data) => {
        setEmployees(data.results);
        setEmployeesLoading(false);
      })
      .catch((error) => {
        setEmployeesError(error.message);
        setEmployeesLoading(false);
      });
  }

  function loadStores() {
    setStoresLoading(true);
    setStoresError("");

    fetch("http://127.0.0.1:8000/api/stores/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar lojas.");
        }

        return response.json();
      })
      .then((data) => {
        setStores(data.results);
        setStoresLoading(false);
      })
      .catch((error) => {
        setStoresError(error.message);
        setStoresLoading(false);
      });
  }

  function renderPage() {
    if (currentPage === "home") {
      return (
        <HomePage
          employees={employees}
          employeesLoading={employeesLoading}
          stores={stores}
          storesLoading={storesLoading}
        />
      );
    }

    if (currentPage === "employees") {
      return (
        <EmployeesPage
          employees={employees}
          loading={employeesLoading}
          errorMessage={employeesError}
        />
      );
    }

    if (currentPage === "stores") {
      return (
        <StoresPage
          stores={stores}
          employees={employees}
          loading={storesLoading || employeesLoading}
          errorMessage={storesError || employeesError}
        />
      );
    }

    if (currentPage === "dismissals") {
      return (
        <PlaceholderPage
          title="Demissões"
          description="Acompanhamento de colaboradores demitidos e divergências de desligamento."
        />
      );
    }

    if (currentPage === "imports") {
      return (
        <PlaceholderPage
          title="Importações"
          description="Importação de arquivos da Tabela Mãe, TOTVS e Gestão de Pessoas."
        />
      );
    }

    if (currentPage === "reports") {
      return (
        <PlaceholderPage
          title="Relatórios"
          description="Área futura para indicadores, gráficos e análises gerenciais."
        />
      );
    }

    return (
      <HomePage
        employees={employees}
        employeesLoading={employeesLoading}
        stores={stores}
        storesLoading={storesLoading}
      />
    );
  }

  return (
    <AppLayout
      currentPage={currentPage}
      onChangePage={setCurrentPage}
    >
      {renderPage()}
    </AppLayout>
  );
}

export default App;
