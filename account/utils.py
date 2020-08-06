import jwt

from django.http import (
    HttpResponse,
    JsonResponse
)

from my_settings import SECRET, ALGORITHM
from account.models import User

def decorator_login(func):
    def wrapper(self, request, *args, **kwargs):
        print(request.headers.get("Authorization", None))
        try:
            given_token  = request.headers.get("Authorization", None)
            payload      = jwt.decode(given_token, SECRET['secret'], algorithms=ALGORITHM)
            user         = User.objects.get(email = payload['email'], login_site = payload['site'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({"Error Message": "INVALID_TOKEN"}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({"Error Message": "Id Dose Not Exist"}, status = 400)
        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({"Error Message": "Expired_access_token"}, status = 400)
        return func(self, request, *args, **kwargs)
    return wrapper
