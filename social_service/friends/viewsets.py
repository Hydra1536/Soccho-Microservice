from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from friends.models import Friendship
from friends.search import fuzzy_search_users
from friends.search_history import SearchHistory
from friends.serializers import FriendshipSerializer
from shared.pagination import SocchoCursorPagination


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.select_related("requester", "addressee")
    serializer_class = FriendshipSerializer
    pagination_class = SocchoCursorPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Friendship.objects.filter(Q(requester=user) | Q(addressee=user))
            .select_related("requester", "addressee")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["get"])
    def accepted(self, request):
        qs = self.get_queryset().filter(status="accepted")
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page if page is not None else qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.addressee_id != request.user.id:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        friendship.status = "accepted"
        friendship.save(update_fields=["status"])
        return Response(self.get_serializer(friendship).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        friendship = self.get_object()
        if friendship.addressee_id != request.user.id:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        friendship.status = "rejected"
        friendship.save(update_fields=["status"])
        return Response(self.get_serializer(friendship).data)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        q = (request.query_params.get("q") or "").strip()
        if len(q) < 2:
            return Response({"edges": [], "pageInfo": {"endCursor": None, "hasNextPage": False}})

        SearchHistory.add(str(request.user.id), q)
        users = fuzzy_search_users(q, limit=10)
        edges = [{"node": {"id": str(u["id"]), "username": u["username"]}} for u in users if u["id"] != request.user.id]
        return Response({"edges": edges, "pageInfo": {"endCursor": None, "hasNextPage": False}})

    @action(detail=False, methods=["get"], url_path="search-history")
    def search_history(self, request):
        return Response(SearchHistory.get(str(request.user.id), limit=10))
