from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class GatewayHeaderAuthentication(BaseAuthentication):
    """
    Internal auth between gateway and Django services.
    Gateway attaches X-User-Id after JWT validation.
    """

    def authenticate(self, request):
        from django.contrib.auth import get_user_model

        user_id = request.headers.get("X-User-Id")
        if not user_id:
            return None

        User = get_user_model()
        user = User.objects.filter(id=user_id, is_active=True).first()
        if not user:
            raise exceptions.AuthenticationFailed("Invalid gateway user header")
        return (user, None)
