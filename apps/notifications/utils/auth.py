from rest_framework.response import Response
from django.conf import settings
secret_key = settings.SECRET_KEY
from rest_framework import status
import jwt

def validate_token(request):
    token = request.META.get('HTTP_AUTHORIZATION').split()[1]

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({"error": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return Response({"error": "An error occurred while decoding the token."}, status=status.HTTP_401_UNAUTHORIZED)

    return payload

