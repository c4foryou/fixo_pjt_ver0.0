from django.contrib import admin

from django.urls import (
    path,
    include
)

from account.views import (
    KakaoLogin,
    AccessTokenCheck,
    EmailAuthentication,
    EmailAuthSucc
)

urlpatterns = [
	path('/sign-in', KakaoLogin.as_view()),
    path('/accesstoken', AccessTokenCheck.as_view()),
    path('/auth', EmailAuthentication.as_view()),
    path('/auth-success/<str:token>', EmailAuthSucc.as_view()),
]
