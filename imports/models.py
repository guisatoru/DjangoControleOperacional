from django.db import models


class ImportBatch(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("processing", "Processando"),
        ("success", "Sucesso"),
        ("partial", "Parcial"),
        ("error", "Erro"),
    ]

    IMPORT_TYPE_CHOICES = [
        ("full", "Completa"),
        ("employees", "Colaboradores"),
        ("stores", "Lojas"),
    ]

    import_type = models.CharField(
        max_length=30,
        choices=IMPORT_TYPE_CHOICES,
        default="full"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    summary = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Importação {self.id} - {self.get_status_display()}"


class ImportFile(models.Model):
    FILE_TYPE_CHOICES = [
        ("mother_table", "Tabela Mãe"),
        ("people_management", "Gestão de Pessoas"),
        ("totvs", "TOTVS"),
    ]

    import_batch = models.ForeignKey(
        ImportBatch,
        on_delete=models.CASCADE,
        related_name="files"
    )

    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to="imports/")
    original_name = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name