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
        


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['created_at', 'dentist']



class BudgetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetDetail
        fields = '__all__'