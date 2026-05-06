# -*- coding: utf-8 -*-
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf.internal import builder as _builder


def _field(message, name, number, field_type):
    proto_field = message.field.add()
    proto_field.name = name
    proto_field.number = number
    proto_field.label = _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    proto_field.type = field_type


def _file_descriptor():
    proto_file = _descriptor_pb2.FileDescriptorProto()
    proto_file.name = "shared/proto/soccho.proto"
    proto_file.package = "soccho"
    proto_file.syntax = "proto3"

    token_request = proto_file.message_type.add()
    token_request.name = "TokenRequest"
    _field(token_request, "token", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)

    token_response = proto_file.message_type.add()
    token_response.name = "TokenResponse"
    _field(token_response, "user_id", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
    _field(token_response, "valid", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_BOOL)

    notification_request = proto_file.message_type.add()
    notification_request.name = "NotificationRequest"
    _field(notification_request, "recipient_id", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
    _field(notification_request, "type", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
    _field(notification_request, "payload", 3, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)

    notification_response = proto_file.message_type.add()
    notification_response.name = "NotificationResponse"
    _field(notification_response, "delivered", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_BOOL)

    auth_service = proto_file.service.add()
    auth_service.name = "AuthService"
    validate_token = auth_service.method.add()
    validate_token.name = "ValidateToken"
    validate_token.input_type = ".soccho.TokenRequest"
    validate_token.output_type = ".soccho.TokenResponse"

    notification_service = proto_file.service.add()
    notification_service.name = "NotificationService"
    send_notification = notification_service.method.add()
    send_notification.name = "SendNotification"
    send_notification.input_type = ".soccho.NotificationRequest"
    send_notification.output_type = ".soccho.NotificationResponse"

    return proto_file


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    _file_descriptor().SerializeToString()
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "shared.proto.soccho_pb2", globals())
