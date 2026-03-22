from django.db import models
from apps.users.models import User
# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    birth_date= models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tutor_name = models.CharField(max_length=100, blank=True, null=True)
    tutor_phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL, # Si el usuario que creó el paciente es eliminado, se establece como NULL en lugar de eliminar el paciente
    null=True,
    blank=True,
    related_name="patients_created"
)
    def __str__(self):
        return f"{self.name} {self.last_name} - {self.rut}"