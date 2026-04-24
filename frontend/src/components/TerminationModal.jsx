import { useEffect, useState } from "react";

import {
  fetchTerminationDetail,
  fetchTerminationTimeOffSummary,
  saveTerminationControl,
} from "../services/api";

function getActionLabel(action) {
  if (action === "prorrogado") {
    return "Prorrogado";
  }

  if (action === "manter") {
    return "Manter";
  }

  if (action === "termino") {
    return "Dar termino";
  }

  return action || "-";
}

function TerminationModal({ terminationId, onClose, onSaved }) {
  const [termination, setTermination] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedAction, setSelectedAction] = useState("");
  const [observation, setObservation] = useState("");
  const [saving, setSaving] = useState(false);
  const [timeOffSummary, setTimeOffSummary] = useState(null);
  const [timeOffLoading, setTimeOffLoading] = useState(false);
  const [timeOffErrorMessage, setTimeOffErrorMessage] = useState("");

  useEffect(() => {
    function handleEsc(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    if (terminationId) {
      document.addEventListener("keydown", handleEsc);
    }

    return () => {
      document.removeEventListener("keydown", handleEsc);
    };
  }, [terminationId, onClose]);

  useEffect(() => {
    let cancelled = false;

    async function loadTermination() {
      if (!terminationId) {
        setTermination(null);
        setSelectedAction("");
        setObservation("");
        setTimeOffSummary(null);
        setTimeOffErrorMessage("");
        setErrorMessage("");
        return;
      }

      setLoading(true);
      setErrorMessage("");

      try {
        const data = await fetchTerminationDetail(terminationId);

        if (!cancelled) {
          setTermination(data);
          setSelectedAction("");
          setObservation("");
          setTimeOffSummary(null);
          setTimeOffErrorMessage("");
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

    loadTermination();

    return () => {
      cancelled = true;
    };
  }, [terminationId]);

  useEffect(() => {
    let cancelled = false;

    async function loadTimeOffSummary() {
      if (!terminationId || !termination?.geo_user_id || !termination?.admission_date) {
        setTimeOffSummary(null);
        setTimeOffErrorMessage("");
        setTimeOffLoading(false);
        return;
      }

      setTimeOffLoading(true);
      setTimeOffErrorMessage("");

      try {
        const data = await fetchTerminationTimeOffSummary(terminationId);

        if (!cancelled) {
          setTimeOffSummary(data);
        }
      } catch (error) {
        if (!cancelled) {
          setTimeOffErrorMessage(error.message);
        }
      } finally {
        if (!cancelled) {
          setTimeOffLoading(false);
        }
      }
    }

    loadTimeOffSummary();

    return () => {
      cancelled = true;
    };
  }, [terminationId, termination?.geo_user_id, termination?.admission_date]);

  async function handleSave() {
    if (!termination) {
      return;
    }

    if (!selectedAction) {
      setErrorMessage("Escolha uma acao para continuar.");
      return;
    }

    if (!observation.trim()) {
      setErrorMessage("A observacao e obrigatoria para registrar a decisao.");
      return;
    }

    setSaving(true);
    setErrorMessage("");

    try {
      const response = await saveTerminationControl(termination.employee_id, {
        stage: termination.current_stage,
        action: selectedAction,
        observation: observation.trim(),
        responded_by: "Usuario",
      });

      setTermination(response.termination);
      setSelectedAction("");
      setObservation("");

      if (onSaved) {
        onSaved(response.termination);
      }
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setSaving(false);
    }
  }

  if (!terminationId) {
    return null;
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="employee-modal" onClick={(event) => event.stopPropagation()}>
        {loading && (
          <div className="module-loading">
            <h2>Carregando termino...</h2>
            <p>Buscando detalhes atualizados no servidor.</p>
          </div>
        )}

        {!loading && errorMessage && <p className="page-message">Erro: {errorMessage}</p>}

        {!loading && termination && (
          <>
            <div className="modal-header">
              <div>
                <h2>{termination.name}</h2>
                <p>
                  RE: {termination.employee_code} - {termination.termination_type || "-"}
                </p>
              </div>

              <button type="button" className="modal-close-button" onClick={onClose}>
                Fechar
              </button>
            </div>

            <div className="modal-section">
              <h3>Acompanhamento</h3>

              <div className="modal-grid">
                <p>
                  <strong>Loja:</strong>
                  <span>{termination.store_name || "-"}</span>
                </p>

                <p>
                  <strong>Coordenacao:</strong>
                  <span>{termination.coordinator || "-"}</span>
                </p>

                <p>
                  <strong>Status do controle:</strong>
                  <span>{termination.control_status || "-"}</span>
                </p>

                <p>
                  <strong>Status Gestao:</strong>
                  <span>{termination.management_status || "-"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>Datas</h3>

              <div className="modal-grid">
                <p>
                  <strong>Data admissao:</strong>
                  <span>{termination.admission_date || "-"}</span>
                </p>

                <p>
                  <strong>Termino 1:</strong>
                  <span>{termination.first_contract_end_date || "-"}</span>
                </p>

                <p>
                  <strong>Termino 2:</strong>
                  <span>{termination.second_contract_end_date || "-"}</span>
                </p>
              </div>
            </div>

            <div className="modal-section">
              <h3>GeoVictoria</h3>

              <div className="modal-grid">
                <p>
                  <strong>Identifier Geo:</strong>
                  <span>{termination.geo_user_id || "-"}</span>
                </p>

                <p>
                  <strong>Dias de atestado:</strong>
                  <span>{timeOffLoading ? "..." : String(timeOffSummary?.medical_certificate_days ?? 0)}</span>
                </p>

                <p>
                  <strong>Faltas:</strong>
                  <span>{timeOffLoading ? "..." : String(timeOffSummary?.absences ?? 0)}</span>
                </p>
              </div>

              {!termination.geo_user_id && (
                <p className="page-message">Este colaborador ainda nao possui Identifier salvo da GeoVictoria.</p>
              )}

              {timeOffErrorMessage && (
                <p className="page-message">Erro GeoVictoria: {timeOffErrorMessage}</p>
              )}
            </div>

            {!termination.closed && (
              <div className="modal-section">
                <h3>Registrar decisao</h3>

                <div className="filters">
                  {termination.available_actions.map((action) => (
                    <button
                      key={action.value}
                      type="button"
                      className={selectedAction === action.value ? "filter-chip active" : "filter-chip"}
                      onClick={() => setSelectedAction(action.value)}
                    >
                      {action.label}
                    </button>
                  ))}
                </div>

                <div className="search-area">
                  <textarea
                    value={observation}
                    onChange={(event) => setObservation(event.target.value)}
                    rows={4}
                    placeholder="Descreva o motivo da decisao..."
                    style={{ width: "100%", resize: "vertical" }}
                  />
                </div>

                <div className="pagination" style={{ justifyContent: "flex-end" }}>
                  <button type="button" onClick={handleSave} disabled={saving}>
                    {saving ? "Salvando..." : "Salvar decisao"}
                  </button>
                </div>
              </div>
            )}

            {termination.closed && (
              <div className="modal-section">
                <p className="page-message">
                  Este acompanhamento ja foi encerrado. O historico continua disponivel abaixo.
                </p>
              </div>
            )}

            <div className="modal-section">
              <h3>Historico</h3>

              <div className="modal-grid">
                {termination.history.length === 0 && (
                  <p>
                    <strong>Sem registros</strong>
                    <span>Nenhuma decisao registrada ainda.</span>
                  </p>
                )}

                {termination.history.map((entry) => (
                  <p key={entry.id}>
                    <strong>
                      {entry.stage}o termino - {getActionLabel(entry.action)}
                    </strong>
                    <span>
                      {entry.observation || "Sem observacao."}
                      {" | "}
                      {entry.responded_by || "Usuario"}
                      {" | "}
                      {entry.responded_at || "-"}
                    </span>
                  </p>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default TerminationModal;
