from django.contrib import admin

from django.urls import (
    path,
    include
)

from account.views import *

urlpatterns = [
	path('/sign-in', KakaoLogin.as_view()),
    path('/accesstoken', AccessTokenCheck.as_view()),
    path('/auth', EmailAuthentication.as_view()),
    path('/auth-success/<str:token>', EmailAuthSucc.as_view()),
    #path('/kakaomessage', KakaoMessageSend.as_view())
]
