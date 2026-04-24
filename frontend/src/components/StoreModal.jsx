import { useEffect, useState } from "react";

import { fetchStoreDetail } from "../services/api";

function normalizeText(value) {
  if (!value) {
    return "";
  }

  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toUpperCase();
}

function StoreModal({ storeId, onClose }) {
  const [store, setStore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [employeeSearch, setEmployeeSearch] = useState("");

  useEffect(() => {
    function handleEsc(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    if (storeId) {
      document.addEventListener("keydown", handleEsc);
    }

    return () => {
      document.removeEventListener("keydown", handleEsc);
    };
  }, [storeId, onClose]);

  useEffect(() => {
    let cancelled = false;

    async function loadStore() {
      if (!storeId) {
        setStore(null);
        setEmployeeSearch("");
        setErrorMessage("");
        return;
      }

      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchStoreDetail(storeId);

        if (!cancelled) {
          setStore(data);
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

    loadStore();

    return () => {
      cancelled = true;
    };
  }, [storeId]);

  if (!storeId) {
    return null;
  }

  const filteredStoreEmployees = (store?.counted_employees || []).filter((employee) => {
    const search = normalizeText(employeeSearch);

    if (!search) {
      return true;
    }

    return (
      normalizeText(employee.name).includes(search) ||
      normalizeText(employee.employee_code).includes(search) ||
      normalizeText(employee.management_job_title).includes(search) ||
      normalizeText(employee.management_status).includes(search)
    );
  });

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="store-modal" onClick={(event) => event.stopPropagation()}>
        {loading && (
          <div className="module-loading">
            <h2>Carregando loja...</h2>
            <p>Buscando quadro e colaboradores contabilizados.</p>
          </div>
        )}

        {!loading && errorMessage && <p className="page-message">Erro: {errorMessage}</p>}

        {!loading && !errorMessage && store && (
          <>
            <div className="modal-header">
              <div>
                <h2>{store.name}</h2>
                <p>Centro de custo: {store.cost_center}</p>
              </div>

              <button type="button" className="modal-close-button" onClick={onClose}>
                Fechar
              </button>
            </div>

            <div className="modal-section">
              <h3>Analise de quadro</h3>

              <div className="store-modal-numbers">
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

              <div className="store-modal-status">
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
            </div>

            <div className="modal-section">
              <h3>Responsaveis</h3>

              <div className="modal-grid">
                <p>
                  <strong>Supervisor:</strong>
                  <span>{store.supervisor || "-"}</span>
                </p>

                <p>
                  <strong>Coordenador:</strong>
                  <span>{store.coordinator || "-"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>Identificação</h3>

              <div className="modal-grid">
                <p>
                  <strong>Nome Gestão:</strong>
                  <span>{store.management_store_name || "-"}</span>
                </p>

                <p>
                  <strong>Nome Geo:</strong>
                  <span>{store.geo_name || "-"}</span>
                </p>

                <p>
                  <strong>Cliente:</strong>
                  <span>{store.client || "-"}</span>
                </p>

                <p>
                  <strong>Ativa:</strong>
                  <span>{store.is_active ? "Sim" : "Nao"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>Endereço</h3>

              <div className="modal-grid">
                <p>
                  <strong>Rua:</strong>
                  <span>{store.street || "-"}</span>
                </p>

                <p>
                  <strong>Bairro:</strong>
                  <span>{store.neighborhood || "-"}</span>
                </p>

                <p>
                  <strong>Cidade/UF:</strong>
                  <span>
                    {store.city || "-"} / {store.state || "-"}
                  </span>
                </p>

                <p>
                  <strong>CEP:</strong>
                  <span>{store.zip_code || "-"}</span>
                </p>
              </div>
            </div>

            <div className="store-modal-search">
              <input
                type="text"
                value={employeeSearch}
                onChange={(event) => setEmployeeSearch(event.target.value)}
                placeholder="Pesquisar colaborador por nome, RE, funcao ou status..."
              />
            </div>

            <div className="modal-section">
              <h3>Colaboradores ativos contabilizados</h3>

              {filteredStoreEmployees.length === 0 && (
                <p className="page-message">Nenhum colaborador ativo encontrado para esta loja.</p>
              )}

              {filteredStoreEmployees.length > 0 && (
                <div className="store-employees-list">
                  {filteredStoreEmployees.map((employee) => (
                    <div className="store-employee-row" key={employee.id}>
                      <div>
                        <strong>{employee.name}</strong>
                        <span>RE: {employee.employee_code}</span>
                      </div>

                      <span>{employee.management_job_title || employee.totvs_job_title || "-"}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default StoreModal;
