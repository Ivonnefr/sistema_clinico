from rest_framework import serializers
from .models import Payment, PaymentDetail
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from django.db import transaction

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ['executed_procedure', 'amount']

class PaymentSerializer(serializers.ModelSerializer):
    details = PaymentDetailSerializer(many=True)

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details')

        # 🔹 VALIDAR TODO PRIMERO
        for detail_data in details_data:
            execution = detail_data['executed_procedure']
            amount = detail_data['amount']

            already_paid = execution.payment_details.aggregate(
                total=Coalesce(Sum('amount'), Value(0), output_field=DecimalField())
            )['total']

            total_price = execution.price or execution.catalog_procedure.base_price

            if already_paid + amount > total_price:
                raise serializers.ValidationError(
                    f"El pago excede el precio del procedimiento. Máximo permitido: {total_price - already_paid}"
                )

        # 🔹 SI TODO OK → CREAR
        with transaction.atomic():
            payment = Payment.objects.create(**validated_data)

            for detail_data in details_data:
                PaymentDetail.objects.create(
                    payment=payment,
                    **detail_data
                )

        return payment