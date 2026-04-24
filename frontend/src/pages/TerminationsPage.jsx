import { useEffect, useState } from "react";

import TerminationModal from "../components/TerminationModal";
import { fetchTerminations } from "../services/api";

function getStatusBadge(controlStatus) {
  if (controlStatus === "Termino registrado") {
    return <span className="alert danger">Termino registrado</span>;
  }

  if (controlStatus === "Mantido") {
    return <span className="alert success">Mantido</span>;
  }

  if (controlStatus === "Prorrogado") {
    return <span className="alert warning">Prorrogado</span>;
  }

  if (controlStatus === "Pendente 2o Termino") {
    return <span className="alert warning">Pendente 2o</span>;
  }

  return <span className="alert info">Pendente 1o</span>;
}

function TerminationsPage() {
  const [loading, setLoading] = useState(true);
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [searchText, setSearchText] = useState("");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [selectedDateFrom, setSelectedDateFrom] = useState("");
  const [selectedCoordinator, setSelectedCoordinator] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedTerminationId, setSelectedTerminationId] = useState(null);
  const [reloadCounter, setReloadCounter] = useState(0);
  const [terminationsResponse, setTerminationsResponse] = useState({
    results: [],
    total_items: 0,
    total_pages: 1,
    coordinators: [],
    summary: {
      total_terminations: 0,
      total_pending_first: 0,
      total_pending_second: 0,
      total_prorrogado: 0,
      total_mantido: 0,
      total_terminated: 0,
    },
  });

  useEffect(() => {
    let cancelled = false;

    async function loadTerminationsPage() {
      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchTerminations({
          page: currentPage,
          search: searchText,
          filter: selectedFilter,
          dateFrom: selectedDateFrom,
          coordinator: selectedCoordinator,
        });

        if (!cancelled) {
          setTerminationsResponse(data);
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

    loadTerminationsPage();

    return () => {
      cancelled = true;
    };
  }, [currentPage, searchText, selectedFilter, selectedDateFrom, selectedCoordinator, reloadCounter]);

  function changeFilter(filter) {
    setSelectedFilter(filter);
    setCurrentPage(1);
  }

  function goToPreviousPage() {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  }

  function goToNextPage() {
    if (currentPage < (terminationsResponse.total_pages || 1)) {
      setCurrentPage(currentPage + 1);
    }
  }

  if (loading && !hasLoadedOnce) {
    return (
      <div className="module-loading">
        <h2>Carregando terminos...</h2>
        <p>Buscando acompanhamentos de experiencia.</p>
      </div>
    );
  }

  if (errorMessage) {
    return <p className="page-message">Erro: {errorMessage}</p>;
  }

  const terminationsToShow = terminationsResponse.results || [];
  const totalItems = terminationsResponse.total_items || 0;
  const totalPages = terminationsResponse.total_pages || 1;
  const summary = terminationsResponse.summary || {};
  const coordinators = terminationsResponse.coordinators || [];

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Terminos</span>
          <h1>Terminos de experiencia</h1>
          <p>Acompanhe prorrogar, manter e dar termino com historico de decisao.</p>
        </div>

        <span className="total-badge">
          Total: {summary.total_terminations || 0}
        </span>
      </div>

      <div className="summary-metric-grid">
        <article className="summary-metric-card info">
          <span>Pendente 1o</span>
          <strong>{summary.total_pending_first || 0}</strong>
          <p>Primeira etapa ainda sem decisao registrada.</p>
        </article>

        <article className="summary-metric-card warning">
          <span>Pendente 2o</span>
          <strong>{summary.total_pending_second || 0}</strong>
          <p>Prorrogados que aguardam a segunda decisao.</p>
        </article>

        <article className="summary-metric-card success">
          <span>Mantidos</span>
          <strong>{summary.total_mantido || 0}</strong>
          <p>Colaboradores efetivados no fluxo de experiencia.</p>
        </article>

        <article className="summary-metric-card danger">
          <span>Termino registrado</span>
          <strong>{summary.total_terminated || 0}</strong>
          <p>Historico fechado com desligamento registrado.</p>
        </article>
      </div>

      <div className="filters">
        <button
          type="button"
          className={selectedFilter === "all" ? "filter-chip active" : "filter-chip"}
          onClick={() => changeFilter("all")}
        >
          Todos: {summary.total_terminations || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "pending_first" ? "filter-chip info active" : "filter-chip info"}
          onClick={() => changeFilter("pending_first")}
        >
          Pendente 1o: {summary.total_pending_first || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "pending_second" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => changeFilter("pending_second")}
        >
          Pendente 2o: {summary.total_pending_second || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "prorrogado" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => changeFilter("prorrogado")}
        >
          Prorrogado: {summary.total_prorrogado || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "mantido" ? "filter-chip info active" : "filter-chip info"}
          onClick={() => changeFilter("mantido")}
        >
          Mantido: {summary.total_mantido || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "terminated" ? "filter-chip danger active" : "filter-chip danger"}
          onClick={() => changeFilter("terminated")}
        >
          Termino registrado: {summary.total_terminated || 0}
        </button>
      </div>

      <div className="search-area">
        <input
          type="text"
          value={searchText}
          onChange={(event) => {
            setSearchText(event.target.value);
            setCurrentPage(1);
          }}
          placeholder="Pesquisar por nome ou RE..."
        />

        <input
          type="date"
          value={selectedDateFrom}
          onChange={(event) => {
            setSelectedDateFrom(event.target.value);
            setCurrentPage(1);
          }}
        />

        <select
          value={selectedCoordinator}
          onChange={(event) => {
            setSelectedCoordinator(event.target.value);
            setCurrentPage(1);
          }}
        >
          <option value="all">Todos os coordenadores</option>
          {coordinators.map((coordinator) => (
            <option key={coordinator} value={coordinator}>
              {coordinator}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={() => {
            setSearchText("");
            setSelectedDateFrom("");
            setSelectedCoordinator("all");
            setSelectedFilter("all");
            setCurrentPage(1);
          }}
        >
          Limpar
        </button>
      </div>

      <div className="list-summary">
        Exibindo {terminationsToShow.length} de {totalItems} terminos encontrados
      </div>

      <div className="employee-modal">
        <div className="dismissals-table-wrapper">
          <table className="dismissals-table">
            <thead>
              <tr>
                <th>Loja</th>
                <th>RE</th>
                <th>Nome</th>
                <th>Admissao</th>
                <th>Termino 1</th>
                <th>Termino 2</th>
                <th>Tipo atual</th>
                <th>Status controle</th>
                <th>Coordenacao</th>
              </tr>
            </thead>
            <tbody>
              {terminationsToShow.map((termination) => (
                <tr
                  key={termination.id}
                  className="dismissal-row"
                  onClick={() => setSelectedTerminationId(termination.employee_id)}
                >
                  <td>{termination.store_name || "-"}</td>
                  <td>{termination.employee_code}</td>
                  <td>{termination.name}</td>
                  <td>{termination.admission_date || "-"}</td>
                  <td>{termination.first_contract_end_date || "-"}</td>
                  <td>{termination.second_contract_end_date || "-"}</td>
                  <td>{termination.termination_type || "-"}</td>
                  <td>{getStatusBadge(termination.control_status)}</td>
                  <td>{termination.coordinator || "-"}</td>
                </tr>
              ))}
              {terminationsToShow.length === 0 && (
                <tr>
                  <td colSpan={9} className="dismissals-empty-cell">
                    Nenhum termino encontrado.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="pagination">
        <button type="button" onClick={goToPreviousPage} disabled={currentPage === 1}>
          Anterior
        </button>

        <span>
          Pagina {currentPage} de {totalPages}
        </span>

        <button type="button" onClick={goToNextPage} disabled={currentPage === totalPages}>
          Proxima
        </button>
      </div>

      <TerminationModal
        terminationId={selectedTerminationId}
        onClose={() => setSelectedTerminationId(null)}
        onSaved={() => setReloadCounter((currentValue) => currentValue + 1)}
      />
    </div>
  );
}

export default TerminationsPage;
