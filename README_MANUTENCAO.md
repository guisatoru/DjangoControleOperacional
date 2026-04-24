# Guia Rapido De Manutencao

Este arquivo resume onde mexer nas partes principais do projeto sem precisar procurar o codigo inteiro.

## Fluxo principal

1. O usuario envia os arquivos na tela de importacao.
2. A API recebe os arquivos em `imports/api/views.py`.
3. Cada importador salva ou atualiza os dados principais:
   `imports/services/store_importer.py`
   `imports/services/employee_importer.py`
   `imports/services/management_employee_importer.py`
4. Depois da importacao, os campos derivados sao recalculados em `employees/services/derived_fields.py`.
5. As telas consultam os dados prontos pelas APIs de `employees/api` e `stores/api`.

## Onde alterar cada regra

`employees/models.py`
Regras de negocio de colaborador, como divergencia de loja e divergencia de status.

`employees/services/derived_fields.py`
Transforma regras em campos salvos no banco. Se quiser manter a tela leve, prefira mexer aqui.

`stores/services/headcount_recalculation.py`
Recalcula headcount das lojas com base nos colaboradores importados.

`employees/services/query_service.py`
Filtros e resumo da tela de colaboradores.

`stores/services/query_service.py`
Filtros e resumo da tela de lojas.

## Comandos uteis

Recalcular campos derivados:

```bash
venv\Scripts\python.exe manage.py refresh_derived_data
```

Validar o projeto Django:

```bash
venv\Scripts\python.exe manage.py check
```

## Regra pratica para manutencao

- Se a mudanca for sobre leitura de planilha, mexa nos `parsers`.
- Se a mudanca for sobre salvar dados, mexa nos `importers`.
- Se a mudanca for sobre comparacao e indicadores, mexa em `derived_fields.py`.
- Se a mudanca for sobre tela lenta, confira se a regra esta sendo feita no import e nao na consulta.
