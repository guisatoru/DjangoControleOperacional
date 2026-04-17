import { useState } from "react";
import StoreModal from "../components/StoreModal";

const ITEMS_PER_PAGE = 12;

function StoresPage({ stores, employees, loading, errorMessage }) {
  const [searchText, setSearchText] = useState("");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);

  const [selectedStore, setSelectedStore] = useState(null);

  function getActiveEmployeesCountByStore(storeId) {
    return employees.filter((employee) => {
      return (
        employee.is_active &&
        employee.counts_in_store_headcount &&
        employee.store_id === storeId
      );
    }).length;
  }

  function getStoreAnalysis(store) {
    const activeEmployees = getActiveEmployeesCountByStore(store.id);
    const contractedHeadcount = store.contracted_headcount || 0;
    const difference = activeEmployees - contractedHeadcount;

    let status = "balanced";

    if (difference > 0) {
      status = "excess";
    }

    if (difference < 0) {
      status = "deficit";
    }

    return {
      ...store,
      activeEmployees,
      contractedHeadcount,
      difference,
      status,
    };
  }

  function storeMatchesSearch(store) {
    const search = searchText.trim().toLowerCase();

    if (!search) {
      return true;
    }

    const name = store.name.toLowerCase();
    const costCenter = store.cost_center.toLowerCase();
    const supervisor = (store.supervisor || "").toLowerCase();
    const coordinator = (store.coordinator || "").toLowerCase();

    return (
      name.includes(search) ||
      costCenter.includes(search) ||
      supervisor.includes(search) ||
      coordinator.includes(search)
    );
  }

  function storeMatchesFilter(store) {
    if (selectedFilter === "excess") {
      return store.status === "excess";
    }

    if (selectedFilter === "deficit") {
      return store.status === "deficit";
    }

    if (selectedFilter === "balanced") {
      return store.status === "balanced";
    }

    return true;
  }

  const analyzedStores = stores.map((store) => getStoreAnalysis(store));

  const filteredStores = analyzedStores.filter((store) => {
    return (
      storeMatchesSearch(store) &&
      storeMatchesFilter(store)
    );
  });

  const totalItems = filteredStores.length;
  const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE) || 1;

  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;

  const storesToShow = filteredStores.slice(startIndex, endIndex);

  const totalExcess = analyzedStores.filter((store) => store.status === "excess").length;
  const totalDeficit = analyzedStores.filter((store) => store.status === "deficit").length;
  const totalBalanced = analyzedStores.filter((store) => store.status === "balanced").length;

  function handleSearchChange(event) {
    setSearchText(event.target.value);
    setCurrentPage(1);
  }

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
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  }

  if (loading) {
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

  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Lojas</span>
          <h1>Lojas</h1>
          <p>Analise quadro contratado, colaboradores ativos, excedentes e déficits.</p>
        </div>

        <span className="total-badge">
          Lojas com quadro: {stores.length}
        </span>
      </div>

      <div className="filters">
        <button
          type="button"
          className={selectedFilter === "all" ? "filter-chip active" : "filter-chip"}
          onClick={() => changeFilter("all")}
        >
          Todas: {analyzedStores.length}
        </button>

        <button
          type="button"
          className={selectedFilter === "deficit" ? "filter-chip danger active" : "filter-chip danger"}
          onClick={() => changeFilter("deficit")}
        >
          Déficit: {totalDeficit}
        </button>

        <button
          type="button"
          className={selectedFilter === "excess" ? "filter-chip warning active" : "filter-chip warning"}
          onClick={() => changeFilter("excess")}
        >
          Excedente: {totalExcess}
        </button>

        <button
          type="button"
          className={selectedFilter === "balanced" ? "filter-chip info active" : "filter-chip info"}
          onClick={() => changeFilter("balanced")}
        >
          No quadro: {totalBalanced}
        </button>
      </div>

      <div className="search-area">
        <input
          type="text"
          value={searchText}
          onChange={handleSearchChange}
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
            <article
                className="store-card"
                key={store.id}
                onClick={() => setSelectedStore(store)}
            >
            <div className="store-card-header">
              <div>
                <h2>{store.name}</h2>
                <span>Centro de custo: {store.cost_center}</span>
              </div>

              {store.status === "deficit" && (
                <span className="store-status danger">Déficit</span>
              )}

              {store.status === "excess" && (
                <span className="store-status warning">Excedente</span>
              )}

              {store.status === "balanced" && (
                <span className="store-status success">No quadro</span>
              )}
            </div>

            <div className="store-numbers">
              <div>
                <span>Contratado</span>
                <strong>{store.contractedHeadcount}</strong>
              </div>

              <div>
                <span>Ativos</span>
                <strong>{store.activeEmployees}</strong>
              </div>

              <div>
                <span>Diferença</span>
                <strong>{store.difference}</strong>
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
        <button
          type="button"
          onClick={goToPreviousPage}
          disabled={currentPage === 1}
        >
          Anterior
        </button>

        <span>
          Página {currentPage} de {totalPages}
        </span>

        <button
          type="button"
          onClick={goToNextPage}
          disabled={currentPage === totalPages}
        >
          Próxima
        </button>
      </div>
      <StoreModal
        store={selectedStore}
        employees={employees}
        onClose={() => setSelectedStore(null)}
      />
    </div>
  );
}

export default StoresPage;
