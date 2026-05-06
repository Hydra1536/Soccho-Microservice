from decimal import Decimal

import graphene
from django.db.models import Q

from transactions.models import Transaction


class TransactionNode(graphene.ObjectType):
    id = graphene.UUID()
    amount = graphene.Float()
    status = graphene.String()
    due_date = graphene.String()
    created_at = graphene.DateTime()


class FriendshipSummary(graphene.ObjectType):
    net_balance = graphene.Float()
    total_given = graphene.Float()
    total_received = graphene.Float()
    recent_transactions = graphene.List(TransactionNode)


class ChartMonth(graphene.ObjectType):
    month = graphene.String()
    total_given = graphene.Float()
    total_lent = graphene.Float()


class Query(graphene.ObjectType):
    friendship_summary = graphene.Field(FriendshipSummary, friend_id=graphene.UUID(required=True))
    monthly_chart = graphene.List(ChartMonth)

    def resolve_friendship_summary(self, info, friend_id):
        user = info.context.user
        if not user or user.is_anonymous:
            return None

        qs = Transaction.objects.filter(
            Q(giver=user, receiver_id=friend_id) | Q(giver_id=friend_id, receiver=user),
            status="confirmed",
            is_soft_deleted=False,
        ).order_by("-created_at")

        given = Decimal("0")
        received = Decimal("0")
        recent = []
        for tx in qs[:50]:
            amount = tx.amount
            if tx.giver_id == user.id:
                given += amount
            else:
                received += amount
            recent.append(
                TransactionNode(
                    id=tx.id,
                    amount=float(amount),
                    status=tx.status,
                    due_date=tx.due_date,
                    created_at=tx.created_at,
                )
            )

        return FriendshipSummary(
            net_balance=float(given - received),
            total_given=float(given),
            total_received=float(received),
            recent_transactions=recent,
        )

    def resolve_monthly_chart(self, info):
        user = info.context.user
        if not user or user.is_anonymous:
            return []

        qs = Transaction.objects.filter(
            Q(giver=user) | Q(receiver=user),
            status="confirmed",
            is_soft_deleted=False,
        ).order_by("-created_at")[:200]

        buckets = {}
        for tx in qs:
            month = tx.created_at.strftime("%Y-%m")
            if month not in buckets:
                buckets[month] = {"given": Decimal("0"), "lent": Decimal("0")}
            if tx.giver_id == user.id:
                buckets[month]["given"] += tx.amount
            else:
                buckets[month]["lent"] += tx.amount

        return [
            ChartMonth(month=month, total_given=float(vals["given"]), total_lent=float(vals["lent"]))
            for month, vals in sorted(buckets.items())
        ]


schema = graphene.Schema(query=Query)
