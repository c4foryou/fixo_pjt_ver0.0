import json
import jwt
import requests
import os, copy
import smtplib   

from random import randint
from datetime import (
    datetime, 
    timedelta
)
# SMTP 라이브러리
from string                 import Template   # 문자열 템플릿 모듈
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText

from django.shortcuts import render
from django.views import View
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseRedirect
)
from django.core.validators import validate_email

from account.models import (
    User, 
    Corrector
)
from account.templates import EMAIL_TEMPLATE
from account.utils import (
    decorator_login,
)

from my_settings import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    SECRET,
    ALGORITHM,
)

class KakaoLogin(View):
    def get(self, request):
        access_token = request.headers["Authorization"]


        kakao_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers = {
                "Host"          : "kapi.kakao.com",
                "Authorization" : f"Bearer {access_token}",
                "Content-type"  : "application/x-www-from-urlencoded;charset=utf-8"
            }
        ,timeout = 2)

        kakao_id = kakao_request.json().get("id")
        kakao_info = kakao_request.json()

        random_picture={
        1:'https://i.pinimg.com/564x/fb/fa/b5/fbfab5595b2edb76f4aa574999ca52d7.jpg',
        2:'https://i.pinimg.com/564x/8f/6a/e5/8f6ae57185d5347ac66ae23bbe83802a.jpg',
        3:'https://i.pinimg.com/564x/7b/d2/73/7bd273aaa294b948fbe71a4dfb932aac.jpg'}
        
        picture_number=randint(1,3)

        try:
            if User.objects.filter(kakao_id = kakao_id).exists():
                user_info = User.objects.get(email=kakao_info["kakao_account"]["email"])
                user_info.access_token  = jwt.encode({"email":user_info.email, "site":user_info.login_site}, SECRET["secret"], algorithm = ALGORITHM).decode("utf-8")
                try:
                    user_info.profile_thumbnail = kakao_info["kakao_account"]["profile"]["profile_image_url"]
                except KeyError:
                    user_info.profile_thumbnail = random_picture[picture_number]            
                
                user_info.save()

                access_token  = user_info.access_token

                return JsonResponse({
                    "access_token":access_token, 
                    "name":user_info.name, 
                    "image":user_info.profile_thumbnail, 
                    "is_corrector":user_info.is_corrector
                    }, status = 200)

            else:

                User(
                        kakao_id      = kakao_id,
                        email         = kakao_info["kakao_account"]["email"],
                        name          = kakao_info["kakao_account"]["profile"]["nickname"],
                        login_site    = "k",
                        is_corrector  = "0",
                        profile_thumbnail = "0",
                        access_token  = jwt.encode({"email":kakao_info["kakao_account"]["email"], "site":"k"}, SECRET["secret"], algorithm = ALGORITHM).decode("utf-8")
                ).save()

                user_info = User.objects.get(email=kakao_info["kakao_account"]["email"])
                try:
                    user_info.profile_thumbnail = kakao_info["kakao_account"]["profile"]["profile_image_url"]
                except KeyError:
                    user_info.profile_thumbnail = random_picture[picture_number]
                user_info.save()

                access_token  = user_info.access_token

                return JsonResponse({
                    "access_token":access_token, 
                    "name":user_info.name, 
                    "image":user_info.profile_thumbnail, 
                    "is_corrector":user_info.is_corrector
                    }, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)


class AccessTokenCheck(View):
    def get(self, request):
        try:
            given_token  = request.headers.get("Authorization", None)
            payload      = jwt.decode(given_token, SECRET["secret"], algorithms=ALGORITHM)
            user         = User.objects.get(email = payload["email"], login_site = payload["site"])
            request.user = user

            return JsonResponse({"message":"valid_token"}, status = 200)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"Error Message": "INVALID_TOKEN"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"Error Message": "Id Dose Not Exist"}, status = 400)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({"Error Message": "Expired_access_token"}, status = 400)




class EmailHTMLContent:
    """e메일에 담길 컨텐츠"""
    def __init__(self, str_subject, template, template_params):
        """string template과 딕셔너리형 template_params받아 MIME 메시지를 만든다"""
        assert isinstance(template, Template)
        assert isinstance(template_params, dict)
        self.msg = MIMEMultipart()
        
        # e메일 제목을 설정한다
        self.msg["Subject"] = str_subject # e메일 제목을 설정한다
        
        # e메일 본문을 설정한다
        str_msg  = template.safe_substitute(**template_params) # ${변수} 치환하며 문자열 만든다
        mime_msg = MIMEText(str_msg, "html")                   # MIME HTML 문자열을 만든다
        self.msg.attach(mime_msg)
        
    def get_message(self, str_from_email_addr, str_to_email_addr):
        """발신자, 수신자리스트를 이용하여 보낼메시지를 만든다 """
        send_msg = copy.deepcopy(self.msg)
        send_msg["From"] = str_from_email_addr          # 발신자
        send_msg["To"]   = str_to_email_addr # ",".join(str_to_email_addrs) : 수신자리스트 2개 이상인 경우
        return send_msg

class EmailSender:
    """e메일 발송자"""
    def __init__(self, str_host, num_port):
        """호스트와 포트번호로 SMTP로 연결한다 """
        self.str_host = str_host
        self.num_port = num_port
        self.smtp_connect = smtplib.SMTP(host=str_host, port=num_port)
        # SMTP인증이 필요하면 아래 주석을 해제하세요.
        self.smtp_connect.starttls() # TLS(Transport Layer Security) 시작
        self.smtp_connect.login(EMAIL_ADDRESS, EMAIL_PASSWORD) # 메일서버에 연결한 계정과 비밀번호
    
    def send_message(self, emailContent, str_from_email_addr, str_to_email_addr):
        """e메일을 발송한다 """
        contents = emailContent.get_message(str_from_email_addr, str_to_email_addr)
        self.smtp_connect.send_message(contents, from_addr=str_from_email_addr, to_addrs=str_to_email_addr)
        del contents

class EmailAuthentication(View):
    
    __COMMON_EMAIL_ADDRESS = [
            "hanmail.net","gmail.com","hotmail.com","yahoo.co.kr","yahoo.com","hanmir.com",
            "nate.com","dreamwiz.com","freechal.com","teramail.com","metq.com","lycos.co.kr",
            "chol.com","korea.com",".edu",".ac.kr"
            ]

    @classmethod
    @decorator_login
    def post(cls, request):
        try:
            data = json.loads(request.body)
            company_email   = data["email"]
            user            = request.user
            Corrector(
                user=user, 
                is_authenticated = False, 
                company_email = company_email
                ).save()

            try:
                validate_email(company_email)
            except:
                return JsonResponse({"message":"INVALID EMAIL"}, status = 400)
            
            if company_email.split("@")[1] in cls.__COMMON_EMAIL_ADDRESS:
                return JsonResponse({"message":"NOT COMPANY EMAIL ADDRESS"}, status = 400)

            str_host            = "smtp.gmail.com"
            num_port            = 587       #SMTP Port
            emailSender         = EmailSender(str_host, num_port)
            
            str_subject         = "[픽소서] EMAIL 인증을 완료해주세요!" # e메일 제목

            auth_token          = jwt.encode(
                {
                    "email":company_email, 
                    "name":user.name
                }, 
                SECRET["secret"], 
                algorithm=ALGORITHM
            ).decode("utf-8")


            template            = Template(EMAIL_TEMPLATE)
            template_params     = {"From":EMAIL_ADDRESS, "Token":auth_token}
            emailHTMLContent    = EmailHTMLContent(str_subject, template, template_params)
            
            str_from_email_addr = EMAIL_ADDRESS # 발신자
            str_to_email_addr   = company_email  # 수신자/ 2개 이상인 경우 리스트
            emailSender.send_message(emailHTMLContent, str_from_email_addr, str_to_email_addr)
            

            User.objects.filter(email = user.email).update(email_auth_token = auth_token)
            return JsonResponse(
                {
                    "message":"EMAIL SENT",
                    "EMAIL_AUTH_TOKEN":auth_token
                }, 
                status = 200
            )
        except KeyError as e:
            return JsonResponse({"message":f"KEY ERROR {e}"}, status = 400)


class EmailAuthSucc(View):
    def get(self, request, token):
        auth_token    = token
        decoded_token = jwt.decode(auth_token, SECRET["secret"], algorithm=ALGORITHM)

        try:
            if User.objects.filter(email_auth_token = auth_token).exists():
                
                user = User.objects.get(email_auth_token = auth_token)
                user.is_corrector = True
                user.save()

                specified_corrector = Corrector.objects.get(user = user, company_email = decoded_token["email"])
                specified_corrector.is_authenticated = True
                specified_corrector.save()

                return HttpResponseRedirect(f"http://10.58.6.248:3000/{user.access_token}")

            return JsonResponse({"message":"USER DOES NOT EXIST"}, status = 400)

        except jwt.exceptions.DecodeError:

            return JsonResponse({"message":"INVALID TOKEN"}, status = 400)
        except jwt.exceptions.ExpiredSignatureError:

            return JsonResponse({"message":"EXPIRED TOKEN"}, status = 400)


