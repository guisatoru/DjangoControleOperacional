import { useEffect, useState } from "react";

import { runImport } from "../services/api";

const EMPTY_FILES = {
  motherTableFile: null,
  totvsFile: null,
  managementFile: null,
};

function ImportField({ title, description, file, inputKey, onChange }) {
  return (
    <div className="import-card">
      <div className="import-card-header">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
      </div>

      <label className="import-upload">
        <span>{file ? "Trocar arquivo" : "Selecionar arquivo"}</span>
        <input
          key={inputKey}
          type="file"
          onChange={(event) => onChange(event.target.files?.[0] || null)}
        />
      </label>

      <div className="import-file-name">
        {file ? file.name : "Nenhum arquivo selecionado."}
      </div>
    </div>
  );
}

function ImportsPage() {
  const [files, setFiles] = useState(EMPTY_FILES);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [toastMessage, setToastMessage] = useState("");
  const [inputResetVersion, setInputResetVersion] = useState(0);

  useEffect(() => {
    if (!toastMessage) {
      return undefined;
    }

    const timeoutId = window.setTimeout(() => {
      setToastMessage("");
    }, 3200);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [toastMessage]);

  function updateFile(fieldName, file) {
    setFiles((currentFiles) => ({
      ...currentFiles,
      [fieldName]: file,
    }));
  }

  function clearAll() {
    setFiles(EMPTY_FILES);
    setErrorMessage("");
    setInputResetVersion((current) => current + 1);
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!files.motherTableFile && !files.totvsFile && !files.managementFile) {
      setErrorMessage("Selecione pelo menos um arquivo para importar.");
      return;
    }

    setLoading(true);
    setErrorMessage("");

    try {
      const response = await runImport(files);
      clearAll();
      setToastMessage(response.message || "Importacoes concluidas com sucesso.");
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="module-page">
      {toastMessage && (
        <div className="page-toast success">
          {toastMessage}
        </div>
      )}

      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Importacoes</span>
          <h1>Importacoes</h1>
          <p>Voce pode importar qualquer combinacao entre Tabela Mae, TOTVS e Gestao.</p>
        </div>
      </div>

      <form className="imports-layout" onSubmit={handleSubmit}>
        <ImportField
          title="Tabela Mae"
          description="Atualiza lojas, quadro contratado e dados cadastrais."
          file={files.motherTableFile}
          inputKey={`mother-table-${inputResetVersion}`}
          onChange={(file) => updateFile("motherTableFile", file)}
        />

        <ImportField
          title="TOTVS"
          description="Atualiza colaboradores, centro de custo e dados da folha."
          file={files.totvsFile}
          inputKey={`totvs-${inputResetVersion}`}
          onChange={(file) => updateFile("totvsFile", file)}
        />

        <ImportField
          title="Gestao de Pessoas"
          description="Atualiza dados de gestao, supervisao e coordenacao."
          file={files.managementFile}
          inputKey={`management-${inputResetVersion}`}
          onChange={(file) => updateFile("managementFile", file)}
        />

        <div className="imports-actions">
          <button className="filter-chip active" type="submit" disabled={loading}>
            {loading ? "Importando..." : "Executar importacoes"}
          </button>

          <button className="filter-chip" type="button" onClick={clearAll} disabled={loading}>
            Limpar selecao
          </button>
        </div>

        {errorMessage && <p className="page-message">Erro: {errorMessage}</p>}
      </form>
    </div>
  );
}

export default ImportsPage;
