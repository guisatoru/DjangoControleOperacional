import { useEffect, useState } from "react";

import StoreModal from "../components/StoreModal";
import { fetchStores } from "../services/api";

function StoresPage() {
  const [searchText, setSearchText] = useState("");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedStoreId, setSelectedStoreId] = useState(null);
  const [storesResponse, setStoresResponse] = useState({
    results: [],
    total_items: 0,
    total_pages: 1,
    summary: {
      total_stores: 0,
      total_balanced: 0,
      total_deficit: 0,
      total_excess: 0,
    },
  });

  useEffect(() => {
    let cancelled = false;

    async function loadStoresPage() {
      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchStores({
          page: currentPage,
          search: searchText,
          filter: selectedFilter,
        });

        if (!cancelled) {
          setStoresResponse(data);
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

    loadStoresPage();

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
    if (currentPage < (storesResponse.total_pages || 1)) {
      setCurrentPage(currentPage + 1);
    }
  }

  if (loading && !hasLoadedOnce) {
    return (
      <div className="module-loading">
        <h2>Carregando lojas...</h2>
        <p>Sincronizando lojas com quadro contratado.</p>
      </div>
    );
  }

  if (errorMessage) {
    return <p className="page-message">Erro: {errorMessage}</p>;
  }

  const storesToShow = storesResponse.results || [];
  const totalItems = storesResponse.total_items || 0;
  const totalPages = storesResponse.total_pages || 1;
  const summary = storesResponse.summary || {};

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Lojas</span>
          <h1>Lojas</h1>
          <p>Analise quadro contratado, colaboradores ativos, excedentes e deficits.</p>
        </div>

        <span className="total-badge">Lojas com quadro: {summary.total_stores || 0}</span>
      </div>

      <div className="filters">
        <button
          type="button"
          className={selectedFilter === "all" ? "filter-chip active" : "filter-chip"}
          onClick={() => changeFilter("all")}
        >
          Todas: {summary.total_stores || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "deficit" ? "filter-chip danger active" : "filter-chip danger"}
          onClick={() => changeFilter("deficit")}
        >
          Deficit: {summary.total_deficit || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "excess" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => changeFilter("excess")}
        >
          Excedente: {summary.total_excess || 0}
        </button>

        <button
          type="button"
          className={selectedFilter === "balanced" ? "filter-chip info active" : "filter-chip info"}
          onClick={() => changeFilter("balanced")}
        >
          No quadro: {summary.total_balanced || 0}
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
          placeholder="Pesquisar por loja, centro de custo, supervisor ou coordenador..."
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
        Exibindo {storesToShow.length} de {totalItems} lojas encontradas
      </div>

      <div className="stores-grid">
        {storesToShow.map((store) => (
          <article className="store-card" key={store.id} onClick={() => setSelectedStoreId(store.id)}>
            <div className="store-card-header">
              <div>
                <h2>{store.name}</h2>
                <span>Centro de custo: {store.cost_center}</span>
              </div>

              {store.headcount_status === "deficit" && (
                <span className="store-status danger">Deficit</span>
              )}

              {store.headcount_status === "excess" && (
                <span className="store-status warning">Excedente</span>
              )}

              {store.headcount_status === "balanced" && (
                <span className="store-status success">No quadro</span>
              )}
            </div>

            <div className="store-numbers">
              <div>
                <span>Contratado</span>
                <strong>{store.contracted_headcount || 0}</strong>
              </div>

              <div>
                <span>Ativos</span>
                <strong>{store.management_headcount || 0}</strong>
              </div>

              <div>
                <span>Diferenca</span>
                <strong>{store.headcount_difference || 0}</strong>
              </div>
            </div>

            <div className="store-details">
              <p>
                <strong>Supervisor:</strong>
                <span>{store.supervisor || "-"}</span>
              </p>

              <p>
                <strong>Coordenador:</strong>
                <span>{store.coordinator || "-"}</span>
              </p>

              <p>
                <strong>Cidade/UF:</strong>
                <span>
                  {store.city || "-"} / {store.state || "-"}
                </span>
              </p>
            </div>
          </article>
        ))}
      </div>

      {storesToShow.length === 0 && (
        <p className="page-message">Nenhuma loja encontrada.</p>
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

      <StoreModal storeId={selectedStoreId} onClose={() => setSelectedStoreId(null)} />
    </div>
  );
}

export default StoresPage;
