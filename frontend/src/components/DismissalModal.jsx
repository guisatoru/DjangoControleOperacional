import { useEffect, useState } from "react";

import { fetchDismissalDetail } from "../services/api";

function DismissalModal({ dismissalId, onClose }) {
  const [dismissal, setDismissal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadDismissal() {
      if (!dismissalId) {
        setDismissal(null);
        setErrorMessage("");
        return;
      }

      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchDismissalDetail(dismissalId);

        if (!cancelled) {
          setDismissal(data);
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

    loadDismissal();

    return () => {
      cancelled = true;
    };
  }, [dismissalId]);

  if (!dismissalId) {
    return null;
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="employee-modal" onClick={(event) => event.stopPropagation()}>
        {loading && (
          <div className="module-loading">
            <h2>Carregando demissao...</h2>
            <p>Buscando detalhes atualizados no servidor.</p>
          </div>
        )}

        {!loading && errorMessage && <p className="page-message">Erro: {errorMessage}</p>}

        {!loading && dismissal && (
          <>
            <div className="modal-header">
              <div>
                <h2>{dismissal.name}</h2>
                <p>RE: {dismissal.employee_code}</p>
              </div>

              <button type="button" className="modal-close-button" onClick={onClose}>
                Fechar
              </button>
            </div>

            <div className="modal-section">
              <h3>TOTVS</h3>

              <div className="modal-grid">
                <p>
                  <strong>Status TOTVS:</strong>
                  <span>{dismissal.payroll_status || "-"}</span>
                </p>

                <p>
                  <strong>Funcao TOTVS:</strong>
                  <span>{dismissal.totvs_job_title || "-"}</span>
                </p>

                <p>
                  <strong>Data admissao:</strong>
                  <span>{dismissal.admission_date || "-"}</span>
                </p>

                <p>
                  <strong>Data demissao:</strong>
                  <span>{dismissal.dismissal_date || "-"}</span>
                </p>

                <p>
                  <strong>Termino 1:</strong>
                  <span>{dismissal.first_contract_end_date || "-"}</span>
                </p>

                <p>
                  <strong>Termino 2:</strong>
                  <span>{dismissal.second_contract_end_date || "-"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>Gestao</h3>

              <div className="modal-grid">
                <p>
                  <strong>Status Gestao:</strong>
                  <span>{dismissal.management_status || "-"}</span>
                </p>

                <p>
                  <strong>Loja Gestao:</strong>
                  <span>{dismissal.management_store_name || "-"}</span>
                </p>

                <p>
                  <strong>Funcao Gestao:</strong>
                  <span>{dismissal.management_job_title || "-"}</span>
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default DismissalModal;
