import { useEffect } from "react";

function EmployeeModal({ employee, onClose }) {
  useEffect(() => {
    function handleEsc(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    if (employee) {
      document.addEventListener("keydown", handleEsc);
    }

    return () => {
      document.removeEventListener("keydown", handleEsc);
    };
  }, [employee, onClose]);

  if (!employee) {
    return null;
  }

  return (
    <div
      className="modal-backdrop"
      onClick={onClose}
    >
      <div
        className="employee-modal"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <div>
            <h2>{employee.name}</h2>
            <p>RE: {employee.employee_code}</p>
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
          <h3>Dados principais</h3>

          <div className="modal-grid">
            <p>
              <strong>Loja TOTVS:</strong>
              <span>{employee.store_name || "-"}</span>
            </p>

            <p>
              <strong>Centro de custo:</strong>
              <span>{employee.cost_center || "-"}</span>
            </p>

            <p>
              <strong>Supervisor:</strong>
              <span>{employee.supervisor || "-"}</span>
            </p>

            <p>
              <strong>Conta no quadro:</strong>
              <span>{employee.counts_in_store_headcount ? "Sim" : "Não"}</span>
            </p>
          </div>
        </div>

        <div className="modal-section">
          <h3>TOTVS</h3>

          <div className="modal-grid">
            <p>
              <strong>Status TOTVS:</strong>
              <span>{employee.payroll_status || "Em branco"}</span>
            </p>

            <p>
              <strong>Função TOTVS:</strong>
              <span>{employee.totvs_job_title || "-"}</span>
            </p>

            <p>
              <strong>Admissão:</strong>
              <span>{employee.admission_date || "-"}</span>
            </p>

            <p>
              <strong>Demissão:</strong>
              <span>{employee.dismissal_date || "-"}</span>
            </p>

            <p>
              <strong>Fim 1º contrato:</strong>
              <span>{employee.first_contract_end_date || "-"}</span>
            </p>

            <p>
              <strong>Fim 2º contrato:</strong>
              <span>{employee.second_contract_end_date || "-"}</span>
            </p>
          </div>
        </div>

        <div className="modal-section">
          <h3>Gestão de Pessoas</h3>

          <div className="modal-grid">
            <p>
              <strong>Loja Gestão:</strong>
              <span>{employee.management_store_name || "-"}</span>
            </p>

            <p>
              <strong>Status Gestão:</strong>
              <span>{employee.management_status || "-"}</span>
            </p>

            <p>
              <strong>Função Gestão:</strong>
              <span>{employee.management_job_title || "-"}</span>
            </p>

            <p>
              <strong>Registros na Gestão:</strong>
              <span>{employee.management_records_count}</span>
            </p>

            <p>
              <strong>Registros não transferidos:</strong>
              <span>{employee.management_non_transferred_records_count}</span>
            </p>
          </div>
        </div>

        <div className="modal-section">
          <h3>GeoVictoria</h3>

          <div className="modal-grid">
            <p>
              <strong>Loja Geo:</strong>
              <span>{employee.geo_store_name || "-"}</span>
            </p>

            <p>
              <strong>ID Geo:</strong>
              <span>{employee.geo_user_id || "-"}</span>
            </p>
          </div>
        </div>

        <div className="modal-section">
          <h3>Divergências</h3>

          <div className="employee-card-alerts">
            {employee.has_store_divergence && (
              <span className="alert danger">Divergência de loja</span>
            )}

            {employee.has_status_divergence && (
              <span className="alert warning">Status divergente</span>
            )}

            {employee.has_management_duplicate_records && (
              <span className="alert warning">Duplicidade na Gestão</span>
            )}

            {!employee.has_management_data && (
              <span className="alert info">Sem dados da Gestão</span>
            )}

            {!employee.counts_in_store_headcount && (
              <span className="alert neutral">Não conta no quadro</span>
            )}

            {!employee.has_store_divergence &&
              !employee.has_status_divergence &&
              !employee.has_management_duplicate_records &&
              employee.has_management_data &&
              employee.counts_in_store_headcount && (
                <span className="alert success">Sem divergências principais</span>
              )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default EmployeeModal;