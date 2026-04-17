from django.db import models


class CatalogProcedure(models.Model): # Catalogo de procedimientos
    name = models.CharField(max_length=255)

    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    dentist_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return self.name
    

class ExecutedProcedure(models.Model): # Procedimiento ejecutado
    attention = models.ForeignKey(
        'attentions.Attention',
        on_delete=models.CASCADE,
        related_name="executed_procedures"
    )

    catalog_procedure = models.ForeignKey(
        'treatments.CatalogProcedure',
        on_delete=models.PROTECT,
        related_name="executions"
    )

    piece = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    scope = models.CharField(
        max_length=20,
        choices=[
            ('piece', 'Piece'),
            ('session', 'Session')
        ]
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    budget_detail = models.ForeignKey(
    'treatments.BudgetDetail',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='executions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.catalog_procedure.base_price
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.catalog_procedure.name} - Attention {self.attention_id}"
    
class Budget(models.Model): # Presupuesto
    clinical_record = models.ForeignKey(
        'clinical_records.ClinicalRecord',
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    dentist = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('closed', 'Closed'),
            ('cancelled', 'Cancelled')
        ],
        default='open'
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Budget {self.id} - ClinicalRecord {self.clinical_record_id}"

class BudgetDetail(models.Model): # Detalle del presupuesto
    budget = models.ForeignKey(
        'treatments.Budget',
        on_delete=models.CASCADE,
        related_name='details'
    )

    catalog_procedure = models.ForeignKey(
        'treatments.CatalogProcedure',
        on_delete=models.PROTECT,
        related_name='budget_details'
    )

    piece = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    tooth_side = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    scope = models.CharField(
        max_length=20,
        choices=[
            ('piece', 'Piece'),
            ('sextant', 'Sextant'),
            ('arch', 'Arch'),
            ('mouth', 'Mouth'),
            ('session', 'Session')
        ]
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )
    def __str__(self):
        return f"{self.catalog_procedure.name} - Budget {self.budget_id}"