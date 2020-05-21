import json
import jwt
import bcrypt

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.db.models import Q

from account.models import Account, Follow
from feed.models import *
from jp_stagram.settings import SECRET_KEY, HASH
from jp_stagram.utils import login_decorator


# @login_decorator
# class ProfileView(View):
#    # get method: returns user profile
#    def get(self, request):
#        user = request.user
#        profile_info = {
#            'username': user.username
#            'email': user.email
#            'followers': user.
#            'following': user.
#            'posts':}
#        return JsonResponse({f'all comments written by {account}': commentsList}, status=200)


class LoginView(View):
    # post method: user log-in with any one of username, email, or phone
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(
                Q(username=data.get('username')) |
                Q(email_or_phone=data.get('email_or_phone'))
            ).exists():
                user = Account.objects.get(
                    Q(username=data.get('username')) |
                    Q(email_or_phone=data.get('email_or_phone'))
                )
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    # if password is correct
                    token = jwt.encode({'user_id': user.id},
                                       SECRET_KEY, algorithm=HASH)
                    return JsonResponse({'message': 'login successful!', 'token': token.decode('utf-8')}, status=200)
            return JsonResponse({'message': 'Incorrect id or password'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)


class RegisterView(View):
    # post method: user sign-up
    def post(self, request):
        data = json.loads(request.body)
        """
        condition = {
            realname:data['realname']
        }

        if 'phone' in data:
            condition['phone'] = data['phone']
        if 'eamil' in data
        """

        try:
            e_password = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())
            # **condition -> realname=data['realname']
            Account.objects.create(
                email_or_phone=data['email_or_phone'],
                realname=data['realname'],
                username=data['username'],
                password=e_password.decode('utf-8'),
            )
            # if registered successfully
            return JsonResponse({'message': 'Registration Successful!'}, status=200)
        except IntegrityError:
            return JsonResponse({'message': 'EXISTING_VALUE'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
