from django.db import models
from apps.patients.models import Patient
from apps.users.models import User


class Attention(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="attentions"
    )

    dentist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attentions"
    )

    date = models.DateTimeField(auto_now_add=True)

    observations = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attention {self.id} - Patient {self.patient_id}"