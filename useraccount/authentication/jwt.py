from rest_framework_simplejwt.tokens import RefreshToken

from useraccount.serializers import MyTokenSerializer


def get_tokens_for_user(user, *args):
    refresh = MyTokenSerializer.get_token(user, *args)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
