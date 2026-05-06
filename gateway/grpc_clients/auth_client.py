import grpc

import shared.proto.soccho_pb2 as soccho_pb2
import shared.proto.soccho_pb2_grpc as soccho_pb2_grpc
from shared.exceptions import CircuitOpen


class AuthClient:
    def __init__(self, host: str = "soccho-auth:50051"):
        self.channel = grpc.insecure_channel(host)
        self.stub = soccho_pb2_grpc.AuthServiceStub(self.channel)

    def validate_token(self, token: str):
        try:
            request = soccho_pb2.TokenRequest(token=token)
            response = self.stub.ValidateToken(request, timeout=2.0)
            return bool(response.valid), str(response.user_id)
        except grpc.RpcError as exc:
            if exc.code() == grpc.StatusCode.UNAVAILABLE:
                raise CircuitOpen("Auth service unavailable") from exc
            raise
