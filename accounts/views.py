from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import InvestmentAccount, UserInvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import InvestmentAccountPermission
from django.db.models import Sum
from rest_framework.response import Response

# List all investment accounts or create a new one
class InvestmentAccountListCreateView(generics.ListCreateAPIView):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

# Retrieve, update, or delete a specific investment account
class InvestmentAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [permissions.IsAuthenticated, InvestmentAccountPermission]


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


# Admin endpoint to get user's transactions and total balance within a date range
class AdminTransactionsView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        transactions = Transaction.objects.filter(user_id=user_id, created_at__range=[start_date, end_date])
        total_balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0.0

        return Response({
            'transactions': TransactionSerializer(transactions, many=True).data,
            'total_balance': total_balance,
        })