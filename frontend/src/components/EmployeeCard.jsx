function getInitials(name) {
  if (!name) {
    return "?";
  }

  const words = name.trim().split(" ");

  if (words.length === 1) {
    return words[0].slice(0, 2).toUpperCase();
  }

  const firstLetter = words[0].slice(0, 1);
  const secondLetter = words[1].slice(0, 1);

  return `${firstLetter}${secondLetter}`.toUpperCase();
}

function EmployeeCard({ employee, onClick }) {
  return (
    <article
      className="employee-card"
      onClick={onClick}
    >
      <div className="employee-card-top">
        <div className="employee-avatar">
          {getInitials(employee.name)}
        </div>

        <div className="employee-main-info">
          <h2>{employee.name}</h2>
          <span>RE: {employee.employee_code}</span>
        </div>
      </div>

      <div className="employee-status-line">
        {employee.has_store_divergence ? (
          <span className="mini-badge danger">Divergência de loja</span>
        ) : (
          <span className="mini-badge success">Loja consistente</span>
        )}

        {employee.has_status_divergence && (
          <span className="mini-badge warning">Status divergente</span>
        )}

        {employee.has_management_duplicate_records && (
          <span className="mini-badge warning">Duplicidade Gestão</span>
        )}

        {!employee.has_management_data && (
          <span className="mini-badge info">Só TOTVS</span>
        )}
      </div>

      <div className="employee-card-divider" />

      <div className="employee-details-grid">
        <div className="detail-item">
          <span>Loja TOTVS</span>
          <strong>{employee.store_name || "-"}</strong>
        </div>

        <div className="detail-item">
          <span>Loja Gestão</span>
          <strong>{employee.management_store_name || "-"}</strong>
        </div>

        <div className="detail-item">
          <span>Status TOTVS</span>
          <strong>{employee.payroll_status || "Em branco"}</strong>
        </div>

        <div className="detail-item">
          <span>Status Gestão</span>
          <strong>{employee.management_status || "-"}</strong>
        </div>

        <div className="detail-item">
          <span>Função TOTVS</span>
          <strong>{employee.totvs_job_title || "-"}</strong>
        </div>

        <div className="detail-item">
          <span>Função Gestão</span>
          <strong>{employee.management_job_title || "-"}</strong>
        </div>
      </div>
    </article>
  );
}

export default EmployeeCard;