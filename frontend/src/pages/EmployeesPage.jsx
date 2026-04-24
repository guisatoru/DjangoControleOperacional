import { useEffect, useState } from "react";

import EmployeeCard from "../components/EmployeeCard";
import EmployeeModal from "../components/EmployeeModal";
import { fetchEmployees, fetchEmployeesSummary } from "../services/api";

function EmployeesPage() {
  const [loading, setLoading] = useState(true);
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [summaryErrorMessage, setSummaryErrorMessage] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [searchText, setSearchText] = useState("");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedEmployeeId, setSelectedEmployeeId] = useState(null);
  const [employeesResponse, setEmployeesResponse] = useState({
    results: [],
    total_items: 0,
    total_pages: 1,
  });
  const [summary, setSummary] = useState({
    total_employees: 0,
    total_store_divergences: 0,
    total_job_title_divergences: 0,
    total_status_divergences: 0,
    total_management_duplicates: 0,
    total_only_totvs: 0,
  });

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setSearchText(searchInput);
      setCurrentPage(1);
    }, 300);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [searchInput]);

  useEffect(() => {
    let cancelled = false;

    async function loadSummary() {
      setSummaryLoading(true);
      setSummaryErrorMessage("");

      try {
        const data = await fetchEmployeesSummary();

        if (!cancelled) {
          setSummary(data);
        }
      } catch (error) {
        if (!cancelled) {
          setSummaryErrorMessage(error.message);
        }
      } finally {
        if (!cancelled) {
          setSummaryLoading(false);
        }
      }
    }

    loadSummary();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadEmployeesPage() {
      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchEmployees({
          page: currentPage,
          search: searchText,
          filter: selectedFilter,
        });

        if (!cancelled) {
          setEmployeesResponse(data);
          setHasLoadedOnce(true);
        }
      } catch (error) {
        if (!cancelled) {
          setErrorMessage(error.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadEmployeesPage();

    return () => {
      cancelled = true;
    };
  }, [currentPage, searchText, selectedFilter]);

  function goToPreviousPage() {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  }

  function goToNextPage() {
    if (currentPage < (employeesResponse.total_pages || 1)) {
      setCurrentPage(currentPage + 1);
    }
  }

  if (loading && !hasLoadedOnce) {
    return (
      <div className="module-loading">
        <h2>Carregando colaboradores...</h2>
        <p>Sincronizando dados do modulo.</p>
      </div>
    );
  }

  if (errorMessage) {
    return <p className="page-message">Erro: {errorMessage}</p>;
  }

  const employeesToShow = employeesResponse.results || [];
  const totalItems = employeesResponse.total_items || 0;
  const totalPages = employeesResponse.total_pages || 1;

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Colaboradores</span>
          <h1>Base de Colaboradores</h1>
          <p>Compare TOTVS, Gestao e GeoVictoria no mesmo cadastro.</p>
        </div>

        <span className="total-badge">
          Total: {summaryLoading ? "..." : summary.total_employees || 0}
        </span>
      </div>

      {summaryErrorMessage && (
        <p className="page-message">Erro no resumo: {summaryErrorMessage}</p>
      )}

      <div className="filters">
        <button
          type="button"
          className={selectedFilter === "all" ? "filter-chip active" : "filter-chip"}
          onClick={() => {
            setSelectedFilter("all");
            setCurrentPage(1);
          }}
        >
          Todos: {summary.total_employees || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "store_divergence" ? "filter-chip danger active" : "filter-chip danger"}
          onClick={() => {
            setSelectedFilter("store_divergence");
            setCurrentPage(1);
          }}
        >
          Divergencia de lojas: {summary.total_store_divergences || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "job_title_divergence" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => {
            setSelectedFilter("job_title_divergence");
            setCurrentPage(1);
          }}
        >
          Divergencia de funcao: {summary.total_job_title_divergences || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "status_divergence" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => {
            setSelectedFilter("status_divergence");
            setCurrentPage(1);
          }}
        >
          Status divergente: {summary.total_status_divergences || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "management_duplicate" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => {
            setSelectedFilter("management_duplicate");
            setCurrentPage(1);
          }}
        >
          Duplicidade gestao: {summary.total_management_duplicates || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "only_totvs" ? "filter-chip info active" : "filter-chip info"}
          onClick={() => {
            setSelectedFilter("only_totvs");
            setCurrentPage(1);
          }}
        >
          So TOTVS: {summary.total_only_totvs || 0}
        </button>
      </div>

      <div className="search-area">
        <input
          type="text"
          value={searchInput}
          onChange={(event) => {
            setSearchInput(event.target.value);
          }}
          placeholder="Pesquisar por RE ou nome..."
        />

        {searchInput && (
          <button
            type="button"
            onClick={() => {
              setSearchInput("");
              setSearchText("");
              setCurrentPage(1);
            }}
          >
            Limpar
          </button>
        )}
      </div>

      <div className="list-summary">
        Exibindo {employeesToShow.length} de {totalItems} colaboradores encontrados
      </div>

      <div className="employees-grid">
        {employeesToShow.map((employee) => (
          <EmployeeCard
            key={employee.id}
            employee={employee}
            onClick={() => setSelectedEmployeeId(employee.id)}
          />
        ))}
      </div>

      {employeesToShow.length === 0 && (
        <p className="page-message">Nenhum colaborador encontrado.</p>
      )}

      <div className="pagination">
        <button type="button" onClick={goToPreviousPage} disabled={currentPage === 1}>
          Anterior
        </button>

        <span>Pagina {currentPage} de {totalPages}</span>

        <button type="button" onClick={goToNextPage} disabled={currentPage === totalPages}>
          Proxima
        </button>
      </div>

      <EmployeeModal employeeId={selectedEmployeeId} onClose={() => setSelectedEmployeeId(null)} />
    </div>
  );
}

export default EmployeesPage;
