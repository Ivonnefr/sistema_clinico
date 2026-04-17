from rest_framework.views import APIView
from rest_framework.response import Response

from .services.financial_dashboard import get_financial_dashboard
from .serializers import FinancialDashboardFilterSerializer


class FinancialDashboardAPIView(APIView):

    def get(self, request):

        serializer = FinancialDashboardFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        date_from = serializer.validated_data.get('from_date')
        date_to = serializer.validated_data.get('to_date')

        data = get_financial_dashboard(date_from, date_to)

        return Response(data)
    
    def validate(self, data):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise serializers.ValidationError("from_date no puede ser mayor que to_date")

        return data