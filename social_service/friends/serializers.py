from django.contrib.auth import get_user_model
from rest_framework import serializers

from friends.models import Friendship


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class FriendshipSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    addressee = UserSerializer(read_only=True)
    addressee_id = serializers.UUIDField(write_only=True, required=True)
    friend = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Friendship
        fields = ["id", "requester", "addressee", "addressee_id", "friend", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    def validate_addressee_id(self, value):
        request = self.context.get("request")
        if request and str(request.user.id) == str(value):
            raise serializers.ValidationError("Cannot send a friend request to yourself.")
        if not User.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("User not found.")
        return value

    def create(self, validated_data):
        addressee_id = validated_data.pop("addressee_id")
        addressee = User.objects.get(id=addressee_id)
        return Friendship.objects.create(
            requester=self.context["request"].user,
            addressee=addressee,
            status="pending",
        )

    def get_friend(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or user.is_anonymous:
            return None
        friend = obj.addressee if obj.requester_id == user.id else obj.requester
        return {"id": str(friend.id), "username": friend.username}
