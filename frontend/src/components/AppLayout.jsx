import { useState } from "react";

import { syncGeoVictoria } from "../services/api";
import Sidebar from "./Sidebar";

function AppLayout({ children, currentPage, onChangePage }) {
  const [geoLoading, setGeoLoading] = useState(false);
  const [geoMessage, setGeoMessage] = useState("");
  const [geoMessageType, setGeoMessageType] = useState("");

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
          <div className="topbar-title">
            <strong>Sistema interno</strong>
            <span>Ambiente de gestao operacional</span>
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
              {geoLoading ? "Sincronizando Geo..." : "Sincronizar Geo"}
            </button>

            <div className="user-pill">Usuario</div>
          </div>
        </header>

        <section className="app-content">{children}</section>
      </main>
    </div>
  );
}

export default AppLayout;
