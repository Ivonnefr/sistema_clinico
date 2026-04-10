from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from treatments.models import ExecutedProcedure
from payments.models import PaymentDetail
from patients.models import Patient


def get_financial_dashboard():

    # Total facturado
    total_billed = ExecutedProcedure.objects.aggregate(
        total=Coalesce(Sum('price'), Value(0))
    )['total']

    # Total pagado
    total_paid = PaymentDetail.objects.aggregate(
        total=Coalesce(Sum('amount'), Value(0))
    )['total']

    # Deuda total
    total_debt = total_billed - total_paid

    # Pacientes con deuda
    patients_with_debt = Patient.objects.annotate(
        total_billed=Coalesce(
            Sum('clinicalrecord__attention__executed_procedures__price'),
            Value(0)
        ),
        total_paid=Coalesce(
            Sum('payments__details__amount'),
            Value(0)
        )
    ).annotate(
        debt=F('total_billed') - F('total_paid')
    ).filter(
        debt__gt=0
    ).count()

    # Ingresos de hoy
    today = timezone.now().date()

    today_income = PaymentDetail.objects.filter(
        payment__date__date=today
    ).aggregate(
        total=Coalesce(Sum('amount'), Value(0))
    )['total']

    return {
        "total_billed": total_billed,
        "total_paid": total_paid,
        "total_debt": total_debt,
        "patients_with_debt": patients_with_debt,
        "today_income": today_income
    }