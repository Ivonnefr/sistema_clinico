from rest_framework import serializers
from .models import CatalogProcedure
from .models import ExecutedProcedure
from .models import Budget
from .models import BudgetDetail

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
        

class BudgetDetailSerializer(serializers.ModelSerializer):
    is_executed = serializers.SerializerMethodField()
    executions_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BudgetDetail
        fields = '__all__'

    def get_is_executed(self, obj):
        return (obj.executions_count or 0) > 0
class BudgetSerializer(serializers.ModelSerializer):
    total_count = serializers.IntegerField(read_only=True)
    executed_count = serializers.IntegerField(read_only=True)
    progress = serializers.SerializerMethodField()

    details = BudgetDetailSerializer(many=True, read_only=True)

    executed_outside_budget = serializers.SerializerMethodField()
    attention_history = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['created_at', 'dentist']

    def get_progress(self, obj):
        total = obj.total_count or 0
        executed = obj.executed_count or 0

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
                    "date": execution.attention.date,
                    "procedures": []
                }

            data[att_id]["procedures"].append(execution_data)

        return list(data.values())