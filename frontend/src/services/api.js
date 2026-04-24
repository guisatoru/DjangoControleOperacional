async function parseJsonResponse(response, fallbackMessage) {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.error || fallbackMessage);
  }

  return data;
}

export async function fetchEmployees({ page = 1, search = "", filter = "all" } = {}) {
  const params = new URLSearchParams({
    page: String(page),
    search,
    filter,
  });

  const response = await fetch(`/api/employees/?${params.toString()}`);
  return parseJsonResponse(response, "Erro ao buscar colaboradores.");
}

export async function fetchEmployeesSummary() {
  const response = await fetch("/api/employees/summary/");
  return parseJsonResponse(response, "Erro ao buscar resumo dos colaboradores.");
}

export async function fetchEmployeeDetail(employeeId) {
  const response = await fetch(`/api/employees/${employeeId}/`);
  return parseJsonResponse(response, "Erro ao buscar colaborador.");
}

export async function fetchStores({ page = 1, search = "", filter = "all" } = {}) {
  const params = new URLSearchParams({
    page: String(page),
    search,
    filter,
  });

  const response = await fetch(`/api/stores/?${params.toString()}`);
  return parseJsonResponse(response, "Erro ao buscar lojas.");
}

export async function fetchStoreDetail(storeId) {
  const response = await fetch(`/api/stores/${storeId}/`);
  return parseJsonResponse(response, "Erro ao buscar loja.");
}

export async function fetchDismissals({ page = 1, search = "", filter = "all" } = {}) {
  const params = new URLSearchParams({
    page: String(page),
    search,
    filter,
  });

  const response = await fetch(`/api/dismissals/?${params.toString()}`);
  return parseJsonResponse(response, "Erro ao buscar demissoes.");
}

export async function fetchDismissalDetail(dismissalId) {
  const response = await fetch(`/api/dismissals/${dismissalId}/`);
  return parseJsonResponse(response, "Erro ao buscar demissao.");
}

export async function fetchTerminations({
  page = 1,
  search = "",
  filter = "all",
  dateFrom = "",
  coordinator = "all",
} = {}) {
  const params = new URLSearchParams({
    page: String(page),
    search,
    filter,
    date_from: dateFrom,
    coordinator,
  });

  const response = await fetch(`/api/terminations/?${params.toString()}`);
  return parseJsonResponse(response, "Erro ao buscar terminos.");
}

export async function fetchTerminationDetail(terminationId) {
  const response = await fetch(`/api/terminations/${terminationId}/`);
  return parseJsonResponse(response, "Erro ao buscar termino.");
}

export async function fetchTerminationTimeOffSummary(terminationId) {
  const response = await fetch(`/api/terminations/${terminationId}/timeoff/`);
  return parseJsonResponse(response, "Erro ao buscar faltas e atestados na GeoVictoria.");
}

export async function saveTerminationControl(terminationId, payload) {
  const response = await fetch(`/api/terminations/${terminationId}/control/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return parseJsonResponse(response, "Erro ao salvar controle de termino.");
}

export async function runImport(files) {
  const formData = new FormData();

  if (files.motherTableFile) {
    formData.append("mother_table_file", files.motherTableFile);
  }

  if (files.totvsFile) {
    formData.append("totvs_file", files.totvsFile);
  }

  if (files.managementFile) {
    formData.append("management_file", files.managementFile);
  }

  const response = await fetch("/api/imports/run/", {
    method: "POST",
    body: formData,
  });

  return parseJsonResponse(response, "Erro ao importar arquivo.");
}

export async function syncGeoVictoria() {
  const response = await fetch("/api/imports/geovictoria/sync/", {
    method: "POST",
  });

  return parseJsonResponse(response, "Erro ao sincronizar GeoVictoria.");
}
