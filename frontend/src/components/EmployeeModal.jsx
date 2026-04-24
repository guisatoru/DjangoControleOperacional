import { useEffect, useState } from "react";

import { fetchEmployeeDetail } from "../services/api";

function EmployeeModal({ employeeId, onClose }) {
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    function handleEsc(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    if (employeeId) {
      document.addEventListener("keydown", handleEsc);
    }

    return () => {
      document.removeEventListener("keydown", handleEsc);
    };
  }, [employeeId, onClose]);

  useEffect(() => {
    let cancelled = false;

    async function loadEmployee() {
      if (!employeeId) {
        setEmployee(null);
        setErrorMessage("");
        return;
      }

      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchEmployeeDetail(employeeId);

        if (!cancelled) {
          setEmployee(data);
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

    loadEmployee();

    return () => {
      cancelled = true;
    };
  }, [employeeId]);

  if (!employeeId) {
    return null;
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="employee-modal" onClick={(event) => event.stopPropagation()}>
        {loading && (
          <div className="module-loading">
            <h2>Carregando colaborador...</h2>
            <p>Buscando detalhes atualizados no servidor.</p>
          </div>
        )}

        {!loading && errorMessage && <p className="page-message">Erro: {errorMessage}</p>}

        {!loading && !errorMessage && employee && (
          <>
            <div className="modal-header">
              <div>
                <h2>{employee.name}</h2>
                <p>RE: {employee.employee_code}</p>
              </div>

              <button type="button" className="modal-close-button" onClick={onClose}>
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
                  <strong>Centro de custo TOTVS:</strong>
                  <span>{employee.cost_center || "-"}</span>
                </p>

                <p>
                  <strong>Supervisor:</strong>
                  <span>{employee.supervisor || "-"}</span>
                </p>

                <p>
                  <strong>Conta no quadro:</strong>
                  <span>{employee.counts_in_store_headcount ? "Sim" : "Nao"}</span>
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
                  <strong>Funcao TOTVS:</strong>
                  <span>{employee.totvs_job_title || "-"}</span>
                </p>

                <p>
                  <strong>Admissao:</strong>
                  <span>{employee.admission_date || "-"}</span>
                </p>

                <p>
                  <strong>Demissao:</strong>
                  <span>{employee.dismissal_date || "-"}</span>
                </p>

                <p>
                  <strong>Fim 1o contrato:</strong>
                  <span>{employee.first_contract_end_date || "-"}</span>
                </p>

                <p>
                  <strong>Fim 2o contrato:</strong>
                  <span>{employee.second_contract_end_date || "-"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>Gestao de Pessoas</h3>

              <div className="modal-grid">
                <p>
                  <strong>Loja Gestao:</strong>
                  <span>{employee.management_store_name || "-"}</span>
                </p>

                <p>
                  <strong>Status Gestao:</strong>
                  <span>{employee.management_status || "-"}</span>
                </p>

                <p>
                  <strong>Funcao Gestao:</strong>
                  <span>{employee.management_job_title || "-"}</span>
                </p>

                <p>
                  <strong>Registros na Gestao:</strong>
                  <span>{employee.management_records_count}</span>
                </p>

                <p>
                  <strong>Registros nao transferidos:</strong>
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
                  <strong>Centro de custo Geo:</strong>
                  <span>{employee.geo_cost_center_code || "-"}</span>
                </p>

                <p>
                  <strong>Funcao Geo:</strong>
                  <span>{employee.geo_job_title || "-"}</span>
                </p>

                <p>
                  <strong>ID Geo:</strong>
                  <span>{employee.geo_user_id || "-"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>Divergencias</h3>

              <div className="employee-card-alerts">
                {employee.has_store_divergence && (
                  <span className="alert danger">Divergencia de loja</span>
                )}

                {employee.has_job_title_divergence && (
                  <span className="alert warning">Funcao divergente</span>
                )}

                {employee.has_status_divergence && (
                  <span className="alert warning">Status divergente</span>
                )}

                {employee.has_management_duplicate_records && (
                  <span className="alert warning">Duplicidade na Gestao</span>
                )}

                {!employee.has_management_data && (
                  <span className="alert info">Sem dados da Gestao</span>
                )}

                {!employee.geo_user_id && (
                  <span className="alert info">Sem dados do Geo</span>
                )}

                {!employee.counts_in_store_headcount && (
                  <span className="alert neutral">Nao conta no quadro</span>
                )}

                {!employee.has_store_divergence &&
                  !employee.has_job_title_divergence &&
                  !employee.has_status_divergence &&
                  !employee.has_management_duplicate_records &&
                  employee.has_management_data &&
                  employee.counts_in_store_headcount && (
                    <span className="alert success">Sem divergencias principais</span>
                  )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default EmployeeModal;
