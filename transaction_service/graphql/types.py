import graphene
from graphene_django import DjangoObjectType
from transactions.models import Transaction, Balance

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ("id", "status", "created_at")
    
    amount = graphene.Float()
    due_date = graphene.DateTime()

    def resolve_amount(self, info):
        return float(self.amount)

    def resolve_due_date(self, info):
        return self.due_date

class BalanceType(DjangoObjectType):
    class Meta:
        model = Balance
        fields = ("updated_at",)
    
    net_balance = graphene.Float()

    def resolve_net_balance(self, info):
        return float(self.net_balance)

