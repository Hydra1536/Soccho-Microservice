from rest_framework import serializers
from notifications.models import Notification
from shared.encryption import decrypt_field
import json

class NotificationSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'type', 'payload', 'is_read', 'created_at']
    
    def get_payload(self, obj):
        payload = json.loads(decrypt_field(obj.payload_encrypted))
        return payload

