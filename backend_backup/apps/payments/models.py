from django.db import models


class Payment(models.Model):
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('transfer', 'Transfer')
        ]
    )

    date = models.DateTimeField(auto_now_add=True)


    budget = models.ForeignKey(
        'treatments.Budget',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )

    attention = models.ForeignKey(
        'attentions.Attention',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )

    def __str__(self):
        return f"Payment {self.id} - {self.amount}"


class PaymentDetail(models.Model):
    payment = models.ForeignKey(
        'payments.Payment',
        on_delete=models.CASCADE,
        related_name='details'
    )

    executed_procedure = models.ForeignKey(
        'treatments.ExecutedProcedure',
        on_delete=models.CASCADE,
        related_name='payment_details'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail {self.id} - Payment {self.payment_id}"