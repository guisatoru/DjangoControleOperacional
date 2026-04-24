import { useMemo, useState } from "react";

import { syncGeoVictoria } from "../services/api";
import Sidebar from "./Sidebar";

const PAGE_LABELS = {
  home: {
    breadcrumb: "Plataforma / Inicio",
    title: "Painel Geral",
  },
  employees: {
    breadcrumb: "Plataforma / Gestao",
    title: "Colaboradores",
  },
  stores: {
    breadcrumb: "Plataforma / Gestao",
    title: "Lojas",
  },
  dismissals: {
    breadcrumb: "Plataforma / Gestao",
    title: "Demissoes",
  },
  terminations: {
    breadcrumb: "Plataforma / Gestao",
    title: "Terminos de Experiencia",
  },
  imports: {
    breadcrumb: "Plataforma / Sistema",
    title: "Importacoes",
  },
  reports: {
    breadcrumb: "Plataforma / Gestao",
    title: "Relatorios",
  },
};

function formatCurrentDate() {
  return new Intl.DateTimeFormat("pt-BR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date());
}

function PanelIcon() {
  return (
    <span className="topbar-page-icon" aria-hidden="true">
      <span />
      <span />
    </span>
  );
}

function SyncIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="M20 12a8 8 0 0 0-14.23-4.88"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M5 4v4h4"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M4 12a8 8 0 0 0 14.23 4.88"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M19 20v-4h-4"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function AppLayout({ children, currentPage, onChangePage }) {
  const [geoLoading, setGeoLoading] = useState(false);
  const [geoMessage, setGeoMessage] = useState("");
  const [geoMessageType, setGeoMessageType] = useState("");
  const pageInfo = PAGE_LABELS[currentPage] || PAGE_LABELS.home;
  const formattedDate = useMemo(() => formatCurrentDate(), []);

  async function handleGeoSync() {
    setGeoLoading(true);
    setGeoMessage("");
    setGeoMessageType("");

    try {
      const response = await syncGeoVictoria();
      setGeoMessage(response.message || "Sincronizacao com GeoVictoria concluida com sucesso.");
      setGeoMessageType("success");
    } catch (error) {
      setGeoMessage(error.message);
      setGeoMessageType("error");
    } finally {
      setGeoLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <Sidebar currentPage={currentPage} onChangePage={onChangePage} />

      <main className="app-main">
        <header className="topbar">
          <div className="topbar-page">
            <PanelIcon />

            <div className="topbar-title">
              <span>{pageInfo.breadcrumb}</span>
              <strong>{pageInfo.title}</strong>
            </div>
          </div>

          <div className="topbar-actions">
            {geoMessage && (
              <div className={geoMessageType === "error" ? "topbar-message error" : "topbar-message success"}>
                {geoMessage}
              </div>
            )}

            <button
              type="button"
              className="topbar-sync-button"
              onClick={handleGeoSync}
              disabled={geoLoading}
            >
              <SyncIcon />
              {geoLoading ? "Sincronizando Geo..." : "Sincronizar Geo"}
            </button>

            <div className="topbar-status">
              <span>Status rede</span>
              <strong>
                <i />
                Pendente
              </strong>
            </div>

            <div className="user-pill">{formattedDate}</div>
          </div>
        </header>

        <section className="app-content">{children}</section>
      </main>
    </div>
  );
}

export default AppLayout;
