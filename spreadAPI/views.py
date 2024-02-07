from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from . models import MarketSpread
from .serializers import MarketSpreadSerializer, UpdateAlertSpread
# Create your views here.

class ListaSpreads(ListAPIView):
    queryset = MarketSpread.objects.all()
    serializer_class = MarketSpreadSerializer

    def list(self, request):
        spreads = MarketSpread.objects.all()
        serializer = MarketSpreadSerializer(spreads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateSpread(UpdateAPIView):
    queryset = MarketSpread.objects.all()
    serializer_class = UpdateAlertSpread

    def get(self, request, identificador):
        spread = MarketSpread.objects.filter(id=identificador)
        serializer = MarketSpreadSerializer(spread, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, identificador):
        spread = MarketSpread.objects.filter(id=identificador).first()
        serializer = UpdateAlertSpread(spread, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
