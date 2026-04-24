function PlaceholderPage({ title, description }) {
  return (
    <div className="module-page">
      <div className="page-header">
        <div>
          <span className="breadcrumb">Plataforma / Modulo</span>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
      </div>

      <div className="empty-state">
        <h2>Modulo em construcao</h2>
        <p>Esta area ainda sera desenvolvida dentro do sistema.</p>
      </div>
    </div>
  );
}

export default PlaceholderPage;
