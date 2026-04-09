from rest_framework import serializers
from .models import Payment, PaymentDetail


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
        payment = Payment.objects.create(**validated_data)

        for detail_data in details_data:
            execution = detail_data['executed_procedure']
            amount = detail_data['amount']

            # calcular pagado actual
            already_paid = sum(
                d.amount for d in execution.payment_details.all()
            )

            total_price = execution.price or execution.catalog_procedure.base_price

            # si ya se pagó todo, no permitir más pagos
            if already_paid + amount > total_price:
                raise serializers.ValidationError(
                    f"El pago excede el precio del procedimiento. Máximo permitido: {total_price - already_paid}"
                )

            PaymentDetail.objects.create(
                payment=payment,
                **detail_data
            )

        return payment