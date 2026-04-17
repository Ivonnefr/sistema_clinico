from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.treatments.models import ExecutedProcedure
from apps.payments.models import PaymentDetail
from apps.patients.models import Patient


def get_financial_dashboard(date_from=None, date_to=None):

    # Filtros base
    executed_filters = {}
    payment_filters = {}

    if date_from and date_to:
        executed_filters['created_at__date__range'] = [date_from, date_to]
        payment_filters['payment__date__date__range'] = [date_from, date_to]

    # Total facturado
    total_billed = ExecutedProcedure.objects.filter(**executed_filters).aggregate(
        total=Coalesce(Sum('price'), Value(0), output_field=DecimalField())
    )['total']

    # Total pagado
    total_paid = PaymentDetail.objects.filter(**payment_filters).aggregate(
        total=Coalesce(Sum('amount'), Value(0), output_field=DecimalField())
    )['total']

    # Deuda
    total_debt = total_billed - total_paid

    # Pacientes con deuda (SIN filtro por ahora)
    patients_with_debt = Patient.objects.annotate(
        total_billed=Coalesce(
            Sum('clinical_record__attentions__executed_procedures__price'),
            Value(0),
            output_field=DecimalField()
        ),
        total_paid=Coalesce(
            Sum('payments__details__amount'),
            Value(0),
            output_field=DecimalField()
        )
    ).annotate(
        debt=F('total_billed') - F('total_paid')
    ).filter(
        debt__gt=0
    ).count()

    # Ingresos del día (respetando filtro si existe)
    today = timezone.now().date()

    today_income = PaymentDetail.objects.filter(
        payment__date__date=today
    ).aggregate(
        total=Coalesce(Sum('amount'), Value(0), output_field=DecimalField())
    )['total']

    return {
        "total_billed": total_billed,
        "total_paid": total_paid,
        "total_debt": total_debt,
        "patients_with_debt": patients_with_debt,
        "today_income": today_income
    }