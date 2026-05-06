# Generated-compatible gRPC bindings for shared/proto/soccho.proto.
import grpc

from shared.proto import soccho_pb2 as shared_dot_proto_dot_soccho__pb2


class AuthServiceStub:
    def __init__(self, channel):
        self.ValidateToken = channel.unary_unary(
            "/soccho.AuthService/ValidateToken",
            request_serializer=shared_dot_proto_dot_soccho__pb2.TokenRequest.SerializeToString,
            response_deserializer=shared_dot_proto_dot_soccho__pb2.TokenResponse.FromString,
        )


class AuthServiceServicer:
    def ValidateToken(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented")
        raise NotImplementedError("Method not implemented")


def add_AuthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ValidateToken": grpc.unary_unary_rpc_method_handler(
            servicer.ValidateToken,
            request_deserializer=shared_dot_proto_dot_soccho__pb2.TokenRequest.FromString,
            response_serializer=shared_dot_proto_dot_soccho__pb2.TokenResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "soccho.AuthService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class NotificationServiceStub:
    def __init__(self, channel):
        self.SendNotification = channel.unary_unary(
            "/soccho.NotificationService/SendNotification",
            request_serializer=shared_dot_proto_dot_soccho__pb2.NotificationRequest.SerializeToString,
            response_deserializer=shared_dot_proto_dot_soccho__pb2.NotificationResponse.FromString,
        )


class NotificationServiceServicer:
    def SendNotification(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented")
        raise NotImplementedError("Method not implemented")


def add_NotificationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "SendNotification": grpc.unary_unary_rpc_method_handler(
            servicer.SendNotification,
            request_deserializer=shared_dot_proto_dot_soccho__pb2.NotificationRequest.FromString,
            response_serializer=shared_dot_proto_dot_soccho__pb2.NotificationResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "soccho.NotificationService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
