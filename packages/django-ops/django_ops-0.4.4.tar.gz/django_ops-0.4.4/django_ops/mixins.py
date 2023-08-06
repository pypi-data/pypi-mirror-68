from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


class DefaultAuthMixin:
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication,)
