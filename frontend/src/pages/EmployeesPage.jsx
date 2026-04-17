import { useState } from "react";
import EmployeeCard from "../components/EmployeeCard";
import EmployeeModal from "../components/EmployeeModal";

const ITEMS_PER_PAGE = 12;

function EmployeesPage({ employees, loading, errorMessage }) {

    const allEmployees = employees;  

    const [searchText, setSearchText] = useState("");
    const [selectedFilter, setSelectedFilter] = useState("all");
    const [currentPage, setCurrentPage] = useState(1);

    const [selectedEmployee, setSelectedEmployee] = useState(null);

    function employeeMatchesSearch(employee) {
        const search = searchText.trim().toLowerCase();

        if (!search) {
        return true;
        }

        const name = employee.name.toLowerCase();
        const employeeCode = employee.employee_code.toLowerCase();

        return name.includes(search) || employeeCode.includes(search);
    }

    function employeeMatchesFilter(employee) {
        if (selectedFilter === "store_divergence") {
        return employee.has_store_divergence;
        }

        if (selectedFilter === "status_divergence") {
        return employee.has_status_divergence;
        }

        if (selectedFilter === "management_duplicate") {
        return employee.has_management_duplicate_records;
        }

        if (selectedFilter === "only_totvs") {
        return !employee.has_management_data;
        }

        return true;
    }

    const filteredEmployees = allEmployees.filter((employee) => {
        return (
        employeeMatchesSearch(employee) &&
        employeeMatchesFilter(employee)
        );
    });

    const totalItems = filteredEmployees.length;
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE) || 1;

    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;

    const employeesToShow = filteredEmployees.slice(startIndex, endIndex);

    const totalStoreDivergences = allEmployees.filter(
        (employee) => employee.has_store_divergence
    ).length;

    const totalStatusDivergences = allEmployees.filter(
        (employee) => employee.has_status_divergence
    ).length;

    const totalManagementDuplicates = allEmployees.filter(
        (employee) => employee.has_management_duplicate_records
    ).length;

    const totalOnlyTotvs = allEmployees.filter(
        (employee) => !employee.has_management_data
    ).length;

    function goToPreviousPage() {
        if (currentPage > 1) {
        setCurrentPage(currentPage - 1);
        }
    }

    function goToNextPage() {
        if (currentPage < totalPages) {
        setCurrentPage(currentPage + 1);
        }
    }

    if (loading) {
        return (
        <div className="module-loading">
            <h2>Carregando colaboradores...</h2>
            <p>Sincronizando dados do módulo.</p>
        </div>
        );
    }

    if (errorMessage) {
        return <p className="page-message">Erro: {errorMessage}</p>;
    }

    return (
        <div className="module-page">
        <div className="page-header">
            <div>
            <span className="breadcrumb">Plataforma / Colaboradores</span>
            <h1>Base de Colaboradores</h1>
            <p>Compare TOTVS, Gestão e GeoVictoria no mesmo cadastro.</p>
            </div>

            <span className="total-badge">
            Total: {allEmployees.length}
            </span>
        </div>

        <div className="filters">
            <button
            type="button"
            className={selectedFilter === "all" ? "filter-chip active" : "filter-chip"}
            onClick={() => {
                setSelectedFilter("all");
                setCurrentPage(1);
            }}
            >
            Todos: {allEmployees.length}
            </button>

            <button
            type="button"
            className={selectedFilter === "store_divergence" ? "filter-chip danger active" : "filter-chip danger"}
            onClick={() => {
                setSelectedFilter("store_divergence");
                setCurrentPage(1);
            }}
            >
            Divergência de lojas: {totalStoreDivergences}
            </button>

            <button
            type="button"
            className={selectedFilter === "status_divergence" ? "filter-chip warning active" : "filter-chip warning"}
            onClick={() => {
                setSelectedFilter("status_divergence");
                setCurrentPage(1);
            }}
            >
            Status divergente: {totalStatusDivergences}
            </button>

            <button
            type="button"
            className={selectedFilter === "management_duplicate" ? "filter-chip warning active" : "filter-chip warning"}
            onClick={() => {
                setSelectedFilter("management_duplicate");
                setCurrentPage(1);
            }}
            >
            Duplicidade gestão: {totalManagementDuplicates}
            </button>

            <button
            type="button"
            className={selectedFilter === "only_totvs" ? "filter-chip info active" : "filter-chip info"}
            onClick={() => {
                setSelectedFilter("only_totvs");
                setCurrentPage(1);
            }}
            >
            Só TOTVS: {totalOnlyTotvs}
            </button>
        </div>

        <div className="search-area">
            <input
            type="text"
            value={searchText}
            onChange={(event) => {
                setSearchText(event.target.value);
                setCurrentPage(1);
            }}
            placeholder="Pesquisar por RE ou nome..."
            />

            {searchText && (
            <button
                type="button"
                onClick={() => {
                    setSearchText("");
                    setCurrentPage(1);
                }}
            >
                Limpar
            </button>
            )}
        </div>

        <div className="list-summary">
            Exibindo {employeesToShow.length} de {totalItems} colaboradores encontrados
        </div>

        <div className="employees-grid">
            {employeesToShow.map((employee) => (
            <EmployeeCard
                key={employee.id}
                employee={employee}
                onClick={() => setSelectedEmployee(employee)}
            />
            ))}
        </div>

        {employeesToShow.length === 0 && (
            <p className="page-message">Nenhum colaborador encontrado.</p>
        )}

        <div className="pagination">
            <button
            type="button"
            onClick={goToPreviousPage}
            disabled={currentPage === 1}
            >
            Anterior
            </button>

            <span>
            Página {currentPage} de {totalPages}
            </span>

            <button
            type="button"
            onClick={goToNextPage}
            disabled={currentPage === totalPages}
            >
            Próxima
            </button>
        </div>

        <EmployeeModal
            employee={selectedEmployee}
            onClose={() => setSelectedEmployee(null)}
        />
        </div>
    );
}

export default EmployeesPage;