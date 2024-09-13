from django.urls import path
from .views import InvestmentAccountListCreateView,  InvestmentAccountDetailView, TransactionListCreateView, \
AdminTransactionsView


urlpatterns = [
    path('investment-accounts/', InvestmentAccountListCreateView.as_view(), name='investment-account-list-create'),
    path('investment-accounts/<int:pk>/', InvestmentAccountDetailView.as_view(), name='investment-account-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('admin-transactions/<int:user_id>/', AdminTransactionsView.as_view(), name='admin-transactions')
]
