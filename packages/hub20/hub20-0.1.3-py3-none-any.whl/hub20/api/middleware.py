from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware:
    """
    Token authorization middleware for websocket consumers (django channels)
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope["headers"])
        authorization_header = "authorization".encode()
        if authorization_header in headers:
            token_name, token_key = headers[authorization_header].decode().split()
            token = Token.objects.filter(key=token_key).first()
            if token_name.lower() == "token" and token is not None:
                scope["user"] = token.user
                close_old_connections()
            else:
                scope["user"] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
