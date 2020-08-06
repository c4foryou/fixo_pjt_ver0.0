from django.contrib import admin
from django.urls import (
    path,
    include
)

from account import urls
#from statement import urls

urlpatterns = [
    path('account', include('account.urls')),
    path('statement', include('statement.urls'))
]
