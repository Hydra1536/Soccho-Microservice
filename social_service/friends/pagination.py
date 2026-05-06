from rest_framework.pagination import CursorPagination
from shared.pagination import SocchoCursorPagination

class FriendshipCursorPagination(SocchoCursorPagination):
    ordering = '-created_at'

