import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from notifications.models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user or self.user.is_anonymous:
            await self.close(code=4401)
            return
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or "{}")
        if data.get("action") == "mark_read" and data.get("id"):
            await self.mark_read(data["id"])


    async def mark_read(self, notification_id):
        await self.toggle_read(notification_id, True)

    @database_sync_to_async
    def toggle_read(self, notification_id, read):
        Notification.objects.filter(id=notification_id, recipient=self.user).update(is_read=read)

    async def receive_notification(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "payload": event["payload"],
                    "id": event["id"],
                }
            )
        )


