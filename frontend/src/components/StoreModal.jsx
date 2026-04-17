import { useEffect } from "react";

function StoreModal({ store, employees, onClose }) {
  useEffect(() => {
    function handleEsc(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    if (store) {
      document.addEventListener("keydown", handleEsc);
    }

    return () => {
      document.removeEventListener("keydown", handleEsc);
    };
  }, [store, onClose]);

  if (!store) {
    return null;
  }

  const storeEmployees = employees.filter((employee) => {
    return (
      employee.is_active &&
      employee.counts_in_store_headcount &&
      employee.store_id === store.id
    );
  });

  return (
    <div
      className="modal-backdrop"
      onClick={onClose}
    >
      <div
        className="store-modal"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <div>
            <h2>{store.name}</h2>
            <p>Centro de custo: {store.cost_center}</p>
          </div>

          <button
            type="button"
            className="modal-close-button"
            onClick={onClose}
          >
            Fechar
          </button>
        </div>

        <div className="modal-section">
          <h3>Análise de quadro</h3>

          <div className="store-modal-numbers">
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

          <div className="store-modal-status">
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
        </div>

        <div className="modal-section">
          <h3>Responsáveis</h3>

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
              <span>{store.management_link_name || "-"}</span>
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
              <span>{store.is_active ? "Sim" : "Não"}</span>
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

        <div className="modal-section">
          <h3>Colaboradores ativos contabilizados</h3>

          {storeEmployees.length === 0 && (
            <p className="page-message">Nenhum colaborador ativo encontrado para esta loja.</p>
          )}

          {storeEmployees.length > 0 && (
            <div className="store-employees-list">
              {storeEmployees.map((employee) => (
                <div className="store-employee-row" key={employee.id}>
                  <div>
                    <strong>{employee.name}</strong>
                    <span>RE: {employee.employee_code}</span>
                  </div>

                  <span>{employee.totvs_job_title || "-"}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default StoreModal;