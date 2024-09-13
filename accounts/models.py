from django.contrib.auth.models import User
from django.db import models

class InvestmentAccount(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='UserInvestmentAccount')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name
    

class UserInvestmentAccount(models.Model):
    VIEW_ONLY = 'view_only'
    FULL_CRUD = 'full_crud'
    POST_ONLY = 'post_only'

    PERMISSION_CHOICES = [
        (VIEW_ONLY, 'View Only'),
        (FULL_CRUD, 'Full CRUD'),
        (POST_ONLY, 'Post Only'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    def __str__(self):
        return f"{self.user} -- {self.investment_account} -- {self.permission_level}"
    

class Transaction(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account}--{self.user}"
    
