from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)

    geo_name = models.CharField(max_length=255, blank=True, null=True)

    cost_center = models.CharField(max_length=50, unique=True)

    contracted_headcount = models.IntegerField(blank=True, null=True)

    supervisor = models.CharField(max_length=255, blank=True, null=True)
    coordinator = models.CharField(max_length=255, blank=True, null=True)

    street = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    client = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    management_headcount = models.IntegerField(default=0)
    headcount_difference = models.IntegerField(default=0)
    headcount_status = models.CharField(max_length=20, default="balanced")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name