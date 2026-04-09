from rest_framework import serializers
from .models import CatalogProcedure
from .models import ExecutedProcedure
from .models import Budget
from .models import BudgetDetail
from apps.clinical_records.models import ClinicalEvolution

class CatalogProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogProcedure
        fields = '__all__'
        
        
class ExecutedProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutedProcedure
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def validate(self, data): # validaciones de consistencia de catalogo, pieza y no duplicar ejecuciones
        budget_detail = data.get('budget_detail')
        catalog_procedure = data.get('catalog_procedure')
        piece = data.get('piece')

        if budget_detail.catalog_procedure != catalog_procedure:
            raise serializers.ValidationError("El procedimiento no coincide con el presupuesto.")
        
        if budget_detail.piece != piece:
            raise serializers.ValidationError("La pieza no coincide con el presupuesto.")

        if budget_detail.executions.exists():
            raise serializers.ValidationError("Este procedimiento ya ha sido ejecutado.")

        return data

    def create(self, validated_data):
        print("CREATE EXECUTED PROCEDURE")

        budget_detail = validated_data.get('budget_detail')
        print("budget_detail:", budget_detail)

        catalog_procedure = validated_data.get('catalog_procedure')

        if budget_detail:
            print("precio desde budget:", budget_detail.price)
            validated_data['price'] = budget_detail.price
        else:
            print("precio desde catalogo:", catalog_procedure.base_price)
            validated_data['price'] = catalog_procedure.base_price

        return super().create(validated_data)
            

class BudgetDetailSerializer(serializers.ModelSerializer):
    is_executed = serializers.SerializerMethodField()
    executions_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BudgetDetail
        fields = '__all__'

    def get_is_executed(self, obj):
        return (getattr(obj, 'executions_count', 0) or 0) > 0
    
    
class BudgetSerializer(serializers.ModelSerializer):
    total_count = serializers.IntegerField(read_only=True)
    executed_count = serializers.IntegerField(read_only=True)
    progress = serializers.SerializerMethodField()

    details = BudgetDetailSerializer(many=True, read_only=True)

    executed_outside_budget = serializers.SerializerMethodField()
    attention_history = serializers.SerializerMethodField()

    timeline = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['created_at', 'dentist']

    def get_progress(self, obj):
        total = getattr(obj, 'total_count', 0) or 0
        executed = getattr(obj, 'executed_count', 0) or 0

        if total == 0:
            return 0

        return round((executed / total) * 100, 2)

    # prestaciones fuera de presupuesto
    def get_executed_outside_budget(self, obj):
        executions = ExecutedProcedure.objects.filter(
            attention__clinical_record_id=obj.clinical_record_id,
            budget_detail__isnull=True
        ).select_related('attention')

        return ExecutedProcedureSerializer(executions, many=True).data


    def get_attention_history(self, obj):
        executions = ExecutedProcedure.objects.filter(
            attention__clinical_record_id=obj.clinical_record_id
        ).select_related('attention').order_by('attention__date')

        serialized = ExecutedProcedureSerializer(executions, many=True).data

        data = {}

        for execution, execution_data in zip(executions, serialized):
            att_id = execution.attention.id

            if att_id not in data:
                data[att_id] = {
                    "attention_id": att_id,
                    "date": execution.attention.created_at,
                    "procedures": []
                }

            data[att_id]["procedures"].append(execution_data)

        return list(data.values())
    
    def get_timeline(self, obj):
        executions = ExecutedProcedure.objects.filter(
            attention__clinical_record_id=obj.clinical_record_id
        ).select_related(
            'attention',
            'catalog_procedure'
        ).prefetch_related(
            'payment_details'
        )

        evolutions = ClinicalEvolution.objects.filter(
            attention__clinical_record_id=obj.clinical_record_id
        ).select_related('attention')

        timeline = []

        #SERIALIZAR EJECUCIONES UNA VEZ
        exec_serialized = ExecutedProcedureSerializer(executions, many=True).data

        for execution, execution_data in zip(executions, exec_serialized):

            total_price = execution.price or execution.catalog_procedure.base_price

            paid_amount = sum(
                detail.amount for detail in execution.payment_details.all()
            )

            remaining = total_price - paid_amount

            if paid_amount == 0:
                payment_status = "pending"
            elif paid_amount < total_price:
                payment_status = "partial"
            else:
                payment_status = "paid"

            timeline.append({
                "type": "performed_procedure",
                "category": "financial",
                "date": execution.created_at,
                "attention_id": execution.attention.id,

                "procedure_name": execution.catalog_procedure.name,
                "is_extra": execution.budget_detail_id is None,

                # 🔥 NUEVO NIVEL PRO
                "total_price": float(total_price),
                "paid_amount": float(paid_amount),
                "remaining": float(remaining),
                "payment_status": payment_status,

                "data": execution_data
            })


        for evolution in evolutions:
            timeline.append({
                "type": "clinical_note",
                "category": "clinical",
                "date": evolution.created_at,
                "attention_id": evolution.attention.id,

                "summary": evolution.description[:100],

                "data": {
                    "description": evolution.description
                }
            })


        timeline.sort(key=lambda x: x["date"])

        return timeline