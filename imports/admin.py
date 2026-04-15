from django.contrib import admin
from .models import ImportBatch, ImportFile


class ImportFileInline(admin.TabularInline):
    model = ImportFile
    extra = 0


@admin.register(ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "import_type",
        "status",
        "started_at",
        "finished_at",
    ]

    list_filter = [
        "status",
        "import_type",
    ]

    inlines = [ImportFileInline]


@admin.register(ImportFile)
class ImportFileAdmin(admin.ModelAdmin):
    list_display = [
        "original_name",
        "file_type",
        "uploaded_at",
    ]

    list_filter = [
        "file_type",
    ]