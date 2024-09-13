from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import InvestmentAccount, UserInvestmentAccount, Transaction
from django.contrib.auth.models import User

class InvestmentAccountTests(APITestCase):
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        # Create investment accounts
        self.account1 = InvestmentAccount.objects.create(name='Account 1')
        self.account2 = InvestmentAccount.objects.create(name='Account 2')

        # Create UserInvestmentAccount links
        UserInvestmentAccount.objects.create(user=self.user1, investment_account=self.account1, permission_level=UserInvestmentAccount.FULL_CRUD)
        UserInvestmentAccount.objects.create(user=self.user2, investment_account=self.account1, permission_level=UserInvestmentAccount.POST_ONLY)

        # Create transactions
        self.transaction1 = Transaction.objects.create(account=self.account1, user=self.user1, amount=100.0)
    
    def test_investment_account_list(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('investment-account-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_full_crud_permission(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('transaction-list-create'), data={'account': self.account2.id, 'user': self.user1.id, 'amount': 200.0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_only_permission(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('transaction-list-create'), data={'account': self.account1.id, 'user': self.user2.id, 'amount': 150.0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_view_only_permission(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('investment-account-detail', args=[self.account1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
