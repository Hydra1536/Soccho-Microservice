import graphene
from django.db.models import Q

from friends.models import Friendship
from .types import FriendshipType


class Query(graphene.ObjectType):
    friends = graphene.List(FriendshipType, limit=graphene.Int(default_value=10))
    suggested_friends = graphene.List(FriendshipType, limit=graphene.Int(default_value=10))

    def resolve_friends(self, info, limit=10):
        user = info.context.user
        if not user or user.is_anonymous:
            return Friendship.objects.none()
        return Friendship.objects.filter(
            Q(requester=user) | Q(addressee=user),
            status="accepted",
        ).order_by("-created_at")[:limit]

    def resolve_suggested_friends(self, info, limit=10):
        user = info.context.user
        if not user or user.is_anonymous:
            return Friendship.objects.none()
        return Friendship.objects.exclude(requester=user).exclude(addressee=user).order_by("-created_at")[:limit]


schema = graphene.Schema(query=Query)
