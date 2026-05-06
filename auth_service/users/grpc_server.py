import grpc
from concurrent import futures
import shared.proto.soccho_pb2 as soccho_pb2
import shared.proto.soccho_pb2_grpc as soccho_pb2_grpc
from django.conf import settings
from jose import jwt
from jose.exceptions import JWTError
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthService(soccho_pb2_grpc.AuthServiceServicer):
    def ValidateToken(self, request, context):
        try:
            payload = jwt.decode(request.token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.filter(id=payload['user_id']).first()
            if user:
                return soccho_pb2.TokenResponse(
                    valid=True,
                    user_id=str(user.id)
                )
        except JWTError:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid token")
            return soccho_pb2.TokenResponse(valid=False)
        
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return soccho_pb2.TokenResponse(valid=False)

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    soccho_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve_grpc()

