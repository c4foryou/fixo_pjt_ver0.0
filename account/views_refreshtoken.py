# Ver 1.0에 구현할 refresh token 기능 초안

import json
import jwt
import requests

from datetime import (
    datetime, 
    timedelta
)

from django.shortcuts import render
from django.views import View
from django.http import (
    JsonResponse,
    HttpResponse
)

from account.models import (
    User, 
    Corrector
)

from my_settings import SECRET



class KakaoLogin(View):
    def get(self, request):
        access_token = request.headers['Authorization']
        print(access_token)

        kakao_request = requests.get(
            'https://kapi.kakao.com/v2/user/me',
            headers = {
                "Host"          : "kapi.kakao.com",
                'Authorization' : f'Bearer {access_token}',
                "Content-type"  : "application/x-www-from-urlencoded;charset=utf-8"
            }
        ,timeout = 2)

        
        kakao_id = kakao_request.json().get('id')
        kakao_info = kakao_request.json()
        
        try:
            if User.objects.filter(kakao_id = kakao_id).exists():
                user_info   = User.objects.get(email=kakao_info['kakao_account']['email'])
                new_refresh_token = RefreshToken.objects.get(user=user_info)
                new_refresh_token.token = jwt.encode({"email":user_info.email, "site":user_info.login_site, "exp":datetime.utcnow()+timedelta(weeks=2)}, SECRET['secret'], algorithm = 'HS256').decode('utf-8')
                new_refresh_token.save()
                access_token  = jwt.encode({"email":user_info.email, "site":user_info.login_site, "exp":datetime.utcnow()+timedelta(seconds=600)}, SECRET['secret'], algorithm = 'HS256')

                return JsonResponse({"access_token":access_token.decode('utf-8'),"refresh_token":new_refresh_token.token,"name":user_info.name}, status = 200)

            else:
                User(
                        kakao_id      = kakao_id,
                        email         = kakao_info['kakao_account']['email'],
                        name          = kakao_info['kakao_account']['profile']['nickname'],
                        login_site    = 'k',
                        is_corrector  = '0'
                ).save()

                user_info   = User.objects.get(email=kakao_info['kakao_account']['email'])

                RefreshToken(
                        user          = user_info,
                        token = jwt.encode({"email":user_info.email, "site":user_info.login_site, "exp":datetime.utcnow()+timedelta(weeks=2)}, SECRET['secret'], algorithm = 'HS256').decode('utf-8')
                ).save()
                new_refresh_token = RefreshToken.objects.get(user=user_info)
                access_token  = jwt.encode({"email":user_info.email, "site":user_info.login_site, "exp":datetime.utcnow()+timedelta(seconds=600)}, SECRET['secret'], algorithm = 'HS256')

                return JsonResponse({"access_token":access_token.decode('utf-8'),"refresh_token":new_refresh_token.token,"name":user_info.name}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)


class AccessTokenRefresh(View):
    def get(self, request):
        refresh_token = request.headers['Authorization']
        if RefreshToken.objects.filter(token = refresh_token).exists():
            user_info = RefreshToken.objects.get(token = refresh_token).user

            access_token  = jwt.encode({"email":user_info.email, "site":user_info.login_site, "exp":datetime.utcnow()+timedelta(seconds=600)}, SECRET['secret'], algorithm = 'HS256')

            return JsonResponse({"access_token":access_token.decode('utf-8'),"name":user_info.name}, status = 200)

        return JsonResponse({"message":'invalid refresh token'}, status = 401)


class AccessTokenCheck(View):
    def get(self, request):
        try:
            given_token  = request.headers.get("Authorization", None)
            payload      = jwt.decode(given_token, SECRET['secret'], algorithms='HS256')
            user         = User.objects.get(email = payload['email'], login_site = payload['site'])
            request.user = user

            return JsonResponse({"message":"valid_token"}, status = 200)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"Error Message": "INVALID_TOKEN"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"Error Message": "Id Dose Not Exist"}, status = 400)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({"Error Message": "Expired_access_token"}, status = 400)

