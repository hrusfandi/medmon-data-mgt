from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings

import jwt


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header:
            raise exceptions.AuthenticationFailed('Token required')

        sp_auth_header = auth_header.split(" ")

        try:
            decoded_auth_token = jwt.decode(sp_auth_header[1],
                                            settings.AUTH_SERVICE_SECRET_KEY,
                                            algorithms=['HS256'])

            if decoded_auth_token['token_type'] != 'access':
                raise exceptions.NotAuthenticated('Token invalid or expired')
        except Exception:
            raise exceptions.NotAuthenticated('Token invalid or expired.')

        return (decoded_auth_token, None)
