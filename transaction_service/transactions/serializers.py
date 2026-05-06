from django.contrib.auth import get_user_model
from rest_framework import serializers

from transactions.models import Balance, Transaction


User = get_user_model()


class TransactionSerializer(serializers.ModelSerializer):
    giver_username = serializers.ReadOnlyField(source="giver.username")
    receiver_username = serializers.ReadOnlyField(source="receiver.username")
    amount = serializers.SerializerMethodField()
    due_date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "giver_id",
            "receiver_id",
            "giver_username",
            "receiver_username",
            "amount",
            "due_date",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "giver_id", "status"]

    def get_amount(self, obj):
        return str(obj.amount)

    def get_due_date(self, obj):
        return obj.due_date


class TransactionCreateSerializer(serializers.Serializer):
    receiver_id = serializers.UUIDField(required=False)
    friend_id = serializers.UUIDField(required=False)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    due_date = serializers.DateField(required=False, allow_null=True)
    idempotency_key = serializers.CharField(max_length=255)

    def validate(self, attrs):
        receiver_id = attrs.get("receiver_id") or attrs.get("friend_id")
        if not receiver_id:
            raise serializers.ValidationError({"receiver_id": "receiver_id or friend_id is required."})

        request = self.context.get("request")
        if request and str(request.user.id) == str(receiver_id):
            raise serializers.ValidationError("Cannot create transaction with yourself.")

        try:
            receiver = User.objects.get(id=receiver_id, is_active=True)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError({"receiver_id": "Receiver user does not exist."}) from exc

        if attrs["amount"] <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than zero."})

        attrs["receiver"] = receiver
        return attrs

    def create(self, validated_data):
        giver = validated_data["giver"]
        receiver = validated_data["receiver"]
        amount = validated_data["amount"]
        due_date = validated_data.get("due_date")
        idempotency_key = validated_data["idempotency_key"]

        tx = Transaction(
            giver=giver,
            receiver=receiver,
            status="pending",
            idempotency_key=idempotency_key,
        )
        tx.amount = amount
        tx.due_date = due_date.isoformat() if due_date else None
        tx.save()
        return tx


class BalanceSerializer(serializers.ModelSerializer):
    user_a_username = serializers.ReadOnlyField(source="user_a.username")
    user_b_username = serializers.ReadOnlyField(source="user_b.username")
    net_balance = serializers.SerializerMethodField()

    class Meta:
        model = Balance
        fields = ["user_a", "user_b", "user_a_username", "user_b_username", "net_balance", "updated_at"]

    def get_net_balance(self, obj):
        return str(obj.net_balance)
