import grpc

import shared.proto.soccho_pb2 as soccho_pb2
import shared.proto.soccho_pb2_grpc as soccho_pb2_grpc


class NotificationClient:
    def __init__(self, host: str = "soccho-notification:50054"):
        self.channel = grpc.insecure_channel(host)
        self.stub = soccho_pb2_grpc.NotificationServiceStub(self.channel)

    def send_notification(self, recipient_id: str, type_: str, payload: str):
        request = soccho_pb2.NotificationRequest(
            recipient_id=str(recipient_id),
            type=type_,
            payload=payload,
        )
        response = self.stub.SendNotification(request, timeout=2.0)
        return bool(response.delivered)
