from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from shared.exceptions import IdempotencyError
from shared.pagination import SocchoCursorPagination
from transactions.balance import update_balance
from transactions.idempotency import check_idempotency
from transactions.models import Balance, Transaction
from transactions.serializers import BalanceSerializer, TransactionCreateSerializer, TransactionSerializer


class TransactionCursorPagination(SocchoCursorPagination):
    ordering = "-created_at"


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("giver", "receiver")
    serializer_class = TransactionSerializer
    pagination_class = TransactionCursorPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            self.queryset.filter(Q(giver=user) | Q(receiver=user), is_soft_deleted=False)
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        serializer = TransactionCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        try:
            check_idempotency(serializer.validated_data["idempotency_key"])
        except IdempotencyError:
            return Response({"detail": "Duplicate idempotency key"}, status=status.HTTP_409_CONFLICT)

        tx = serializer.save(giver=request.user)
        return Response(TransactionSerializer(tx).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        tx = self.get_object()
        if tx.receiver != request.user:
            return Response({"detail": "Only receiver can confirm"}, status=status.HTTP_403_FORBIDDEN)
        if tx.status != "pending":
            return Response({"detail": "Transaction is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        tx.status = "confirmed"
        tx.version = tx.version + 1
        tx.save(update_fields=["status", "version"])
        update_balance(tx.giver, tx.receiver, tx.amount)
        return Response(TransactionSerializer(tx).data)

    @action(detail=True, methods=["post"])
    def deny(self, request, pk=None):
        tx = self.get_object()
        if tx.receiver != request.user:
            return Response({"detail": "Only receiver can deny"}, status=status.HTTP_403_FORBIDDEN)
        if tx.status != "pending":
            return Response({"detail": "Transaction is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        tx.status = "denied"
        tx.version = tx.version + 1
        tx.save(update_fields=["status", "version"])
        return Response(TransactionSerializer(tx).data)

    @action(detail=False, methods=["get"], url_path="balances")
    def balances(self, request):
        qs = Balance.objects.filter(Q(user_a=request.user) | Q(user_b=request.user)).order_by("-updated_at")
        page = self.paginate_queryset(qs)
        serializer = BalanceSerializer(page if page is not None else qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"balance/(?P<friend_id>[^/.]+)")
    def balance_with_friend(self, request, friend_id=None):
        qs = self.get_queryset().filter(
            Q(giver=request.user, receiver_id=friend_id) | Q(giver_id=friend_id, receiver=request.user),
            status="confirmed",
        )
        total_given = sum(tx.amount for tx in qs if tx.giver_id == request.user.id)
        total_received = sum(tx.amount for tx in qs if tx.receiver_id == request.user.id)
        net_balance = total_given - total_received
        return Response(
            {
                "net_balance": str(net_balance),
                "total_given": str(total_given),
                "total_received": str(total_received),
            }
        )

    @action(detail=False, methods=["get"], url_path=r"list/(?P<friend_id>[^/.]+)")
    def list_with_friend(self, request, friend_id=None):
        qs = self.get_queryset().filter(
            Q(giver=request.user, receiver_id=friend_id) | Q(giver_id=friend_id, receiver=request.user)
        )
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page if page is not None else qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
