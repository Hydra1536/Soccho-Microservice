import graphene
from graphene_django import DjangoObjectType
from friends.models import Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")
    
    loyalty_score = graphene.Float()

class FriendshipType(DjangoObjectType):
    class Meta:
        model = Friendship
        fields = ("id", "status", "created_at")
    
    friend = graphene.Field(UserType)
    net_balance = graphene.Float()

    def resolve_friend(self, info):
        user = getattr(info.context, "user", None)
        if not user or user.is_anonymous:
            return None
        return self.addressee if self.requester_id == user.id else self.requester

    def resolve_net_balance(self, info):
        # Transaction service integration can replace this placeholder.
        return 0.0

