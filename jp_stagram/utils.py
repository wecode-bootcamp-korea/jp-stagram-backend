import jwt
import json

from django.http import JsonResponse
from jp_stagram.settings import SECRET_KEY, HASH
from account.models import Account


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            if request.headers.get('Authorization'):
                user_token = request.headers.get('Authorization')
                user_info = jwt.decode(user_token, SECRET_KEY, HASH)
                if Account.objects.filter(pk=user_info['user_id']).exists():
                    user = Account.objects.get(pk=user_info['user_id'])
                    request.user = user  # request 에 존재하지 않던 user 정보를 추가
                    return func(self, request, *args, **kwargs)
                else:
                    # Toekn's user information does not match database ifnormation: Account does not exist
                    return JsonResponse({'message': 'No matching account'}, status=401)
            # header is missing token: the user needs to log in first
            return JsonResponse({'message': 'No token'}, status=401)
        # Token's user information is invalid
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
    return wrapper
