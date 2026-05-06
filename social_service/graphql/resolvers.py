from friends.models import Friendship
from django.db.models import Q


def resolve_user_friendships(user, limit=10):
    if not user or user.is_anonymous:
        return Friendship.objects.none()
    return Friendship.objects.filter(
        Q(requester=user) | Q(addressee=user),
        status="accepted",
    ).order_by("-created_at")[:limit]
