from datetime import datetime
from rest_framework.authtoken.models import Token
from techser.settings import TOKEN_TTL


def delete_expired_tokens():
    expired_tokens = Token.objects.filter(created__lte=datetime.now() - TOKEN_TTL)

    for token in expired_tokens:
        token.delete()