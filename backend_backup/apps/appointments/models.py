from django.db import models

# Create your models here.
from django.db import models
from apps.patients.models import Patient
from apps.users.models import User


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("confirmed", "Confirmed"),
        ("reconfirmed", "Reconfirmed"),
        ("attended", "Attended"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    dentist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment {self.id} - Patient {self.patient_id}"