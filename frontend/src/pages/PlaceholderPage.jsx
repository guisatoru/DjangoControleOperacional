function PlaceholderPage({ title, description }) {
  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Módulo</span>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
      </div>

      <div className="empty-state">
        <h2>Módulo em construção</h2>
        <p>Esta área ainda será desenvolvida dentro do sistema.</p>
      </div>
    </div>
  );
}

export default PlaceholderPage;