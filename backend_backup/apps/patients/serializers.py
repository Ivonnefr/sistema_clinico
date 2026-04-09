from rest_framework import serializers
from .models import Patient
from rest_framework import serializers
from apps.payments.models import PaymentDetail
from apps.treatments.models import ExecutedProcedure


class PatientSerializer(serializers.ModelSerializer):
    debt = serializers.SerializerMethodField()
    total_billed = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_by']

            

    def get_total_billed(self, obj):
        executions = ExecutedProcedure.objects.filter(
            attention__patient=obj
        )

        total = 0

        for execution in executions:
            total_price = execution.price or execution.catalog_procedure.base_price
            total += total_price

        return float(total)
    
    def get_total_paid(self, obj):
        details = PaymentDetail.objects.filter(
            executed_procedure__attention__patient=obj
        )

        total = sum(d.amount for d in details)

        return float(total)
    
    def get_debt(self, obj):
        return self.get_total_billed(obj) - self.get_total_paid(obj)
    