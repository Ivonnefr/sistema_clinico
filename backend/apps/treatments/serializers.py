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
        


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['created_at', 'dentist']



class BudgetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetDetail
        fields = '__all__'