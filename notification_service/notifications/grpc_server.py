import json
from concurrent import futures

import grpc
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

import shared.proto.soccho_pb2 as soccho_pb2
import shared.proto.soccho_pb2_grpc as soccho_pb2_grpc
from notifications.models import Notification
from shared.encryption import encrypt_field


User = get_user_model()
ALLOWED_TYPES = {"lend_confirm", "payment_received", "due_reminder"}


class NotificationService(soccho_pb2_grpc.NotificationServiceServicer):
    def SendNotification(self, request, context):
        if request.type not in ALLOWED_TYPES:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Unsupported notification type")
            return soccho_pb2.NotificationResponse(delivered=False)

        try:
            recipient = User.objects.get(id=request.recipient_id)
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Recipient not found")
            return soccho_pb2.NotificationResponse(delivered=False)

        try:
            payload_dict = {
                "type": request.type,
                "data": request.payload,
            }
            encrypted_payload = encrypt_field(json.dumps(payload_dict))
            notification = Notification.objects.create(
                recipient=recipient,
                type=request.type,
                payload_encrypted=encrypted_payload,
            )

            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f"user_{recipient.id}",
                    {
                        "type": "receive_notification",
                        "id": str(notification.id),
                        "payload": payload_dict,
                    },
                )

            return soccho_pb2.NotificationResponse(delivered=True)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return soccho_pb2.NotificationResponse(delivered=False)


def serve_grpc(port: int = 50054):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    soccho_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve_grpc()
