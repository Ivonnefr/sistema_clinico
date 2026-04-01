from django.db import models
from apps.patients.models import Patient


class ClinicalRecord(models.Model):
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="clinical_record"
    )

    opened_at = models.DateTimeField(auto_now_add=True)

    medical_history = models.TextField(blank=True, null=True)
    general_observations = models.TextField(blank=True, null=True)
    medical_alerts = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Clinical Record - Patient {self.patient_id}"