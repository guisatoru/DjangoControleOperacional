import { useEffect, useState } from "react";

import DismissalModal from "../components/DismissalModal";
import { fetchDismissals } from "../services/api";

function DismissalsPage() {
  const [loading, setLoading] = useState(true);
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [searchText, setSearchText] = useState("");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedDismissalId, setSelectedDismissalId] = useState(null);
  const [dismissalsResponse, setDismissalsResponse] = useState({
    results: [],
    total_items: 0,
    total_pages: 1,
    summary: {
      total_dismissals: 0,
      total_ok: 0,
      total_pending: 0,
      total_divergent: 0,
    },
  });

  useEffect(() => {
    let cancelled = false;

    async function loadDismissalsPage() {
      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchDismissals({
          page: currentPage,
          search: searchText,
          filter: selectedFilter,
        });

        if (!cancelled) {
          setDismissalsResponse(data);
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

    loadDismissalsPage();

    return () => {
      cancelled = true;
    };
  }, [currentPage, searchText, selectedFilter]);

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
    if (currentPage < (dismissalsResponse.total_pages || 1)) {
      setCurrentPage(currentPage + 1);
    }
  }

  if (loading && !hasLoadedOnce) {
    return (
      <div className="module-loading">
        <h2>Carregando demissoes...</h2>
        <p>Buscando desligamentos registrados.</p>
      </div>
    );
  }

  if (errorMessage) {
    return <p className="page-message">Erro: {errorMessage}</p>;
  }

  const dismissalsToShow = dismissalsResponse.results || [];
  const totalItems = dismissalsResponse.total_items || 0;
  const totalPages = dismissalsResponse.total_pages || 1;
  const summary = dismissalsResponse.summary || {};

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Demissoes</span>
          <h1>Demissoes</h1>
          <p>Consulte desligamentos e compare TOTVS com Gestao.</p>
        </div>

        <span className="total-badge">
          Total: {summary.total_dismissals || 0}
        </span>
      </div>

      <div className="summary-metric-grid">
        <article className="summary-metric-card danger">
          <span>Divergentes</span>
          <strong>{summary.total_divergent || 0}</strong>
          <p>Demissoes com diferenca entre as bases.</p>
        </article>

        <article className="summary-metric-card warning">
          <span>Pendentes</span>
          <strong>{summary.total_pending || 0}</strong>
          <p>Aguardando atualizacao ou validacao da gestao.</p>
        </article>

        <article className="summary-metric-card success">
          <span>Alinhadas</span>
          <strong>{summary.total_ok || 0}</strong>
          <p>Demissoes com status coerente nas duas bases.</p>
        </article>
      </div>

      <div className="filters">
        <button
          type="button"
          className={
            selectedFilter === "all" ? "filter-chip active" : "filter-chip"
          }
          onClick={() => changeFilter("all")}
        >
          Todas: {summary.total_dismissals || 0}
        </button>

        <button
          type="button"
          className={
            selectedFilter === "ok"
              ? "filter-chip info active"
              : "filter-chip info"
          }
          onClick={() => changeFilter("ok")}
        >
          Alinhadas: {summary.total_ok || 0}
        </button>

        <button
          type="button"
          className={
            selectedFilter === "pending"
              ? "filter-chip warning active"
              : "filter-chip warning"
          }
          onClick={() => changeFilter("pending")}
        >
          Pendentes: {summary.total_pending || 0}
        </button>

        <button
          type="button"
          className={
            selectedFilter === "divergent"
              ? "filter-chip danger active"
              : "filter-chip danger"
          }
          onClick={() => changeFilter("divergent")}
        >
          Divergentes: {summary.total_divergent || 0}
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
          placeholder="Pesquisar por RE, nome ou status..."
        />

        {searchText && (
          <button
            type="button"
            onClick={() => {
              setSearchText("");
              setCurrentPage(1);
            }}
          >
            Limpar
          </button>
        )}
      </div>

      <div className="list-summary">
        Exibindo {dismissalsToShow.length} de {totalItems} demissoes encontradas
      </div>

      <div className="employee-modal">
        <div className="dismissals-table-wrapper">
          <table className="dismissals-table">
            <thead>
              <tr>
                <th>RE</th>
                <th>Nome</th>
                <th>Data</th>
                <th>Status TOTVS</th>
                <th>Status Gestao</th>
                <th>Situacao</th>
              </tr>
            </thead>
            <tbody>
              {dismissalsToShow.map((dismissal) => (
                <tr
                  key={dismissal.id}
                  className="dismissal-row"
                  onClick={() => setSelectedDismissalId(dismissal.id)}
                >
                  <td>{dismissal.employee_code}</td>
                  <td>{dismissal.name}</td>
                  <td>{dismissal.dismissal_date || "-"}</td>
                  <td>{dismissal.payroll_status || "-"}</td>
                  <td>{dismissal.management_status || "-"}</td>
                  <td>
                    {dismissal.comparison_status === "ok" && (
                      <span className="alert success">Alinhada</span>
                    )}
                    {dismissal.comparison_status === "pending" && (
                      <span className="alert warning">Pendente</span>
                    )}
                    {dismissal.comparison_status === "divergent" && (
                      <span className="alert danger">Divergente</span>
                    )}
                  </td>
                </tr>
              ))}
              {dismissalsToShow.length === 0 && (
                <tr>
                  <td colSpan={6} className="dismissals-empty-cell">
                    Nenhuma demissao encontrada.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="pagination">
        <button
          type="button"
          onClick={goToPreviousPage}
          disabled={currentPage === 1}
        >
          Anterior
        </button>

        <span>
          Pagina {currentPage} de {totalPages}
        </span>

        <button
          type="button"
          onClick={goToNextPage}
          disabled={currentPage === totalPages}
        >
          Proxima
        </button>
      </div>

      <DismissalModal
        dismissalId={selectedDismissalId}
        onClose={() => setSelectedDismissalId(null)}
      />
    </div>
  );
}

export default DismissalsPage;
