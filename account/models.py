from django.db import models

class User(models.Model):
    kakao_id          = models.CharField(max_length = 50,null = True)
    email             = models.CharField(max_length = 50)
    name              = models.CharField(max_length = 50)
    school            = models.CharField(max_length = 50,null = True)
    major             = models.CharField(max_length = 50,null = True)
    minor             = models.CharField(max_length = 50,null = True)
    phone_number      = models.CharField(max_length = 50,null = True)
    login_site        = models.CharField(max_length = 50,null = True)
    access_token      = models.CharField(max_length = 500,null = True)
    email_auth_token  = models.CharField(max_length = 500,null = True)
    profile_thumbnail = models.CharField(max_length = 500,null = True)
    is_corrector      = models.BooleanField(null=True)

    class Meta:
        db_table = 'users'

class RefreshToken(models.Model):
    user  = models.ForeignKey('User', on_delete=models.CASCADE, null = True)
    token = models.CharField(max_length = 500,null = True)

    class Meta:
        db_table = 'refresh_tokens'

class Applicant(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null = True)

    class Meta:
        db_table = 'applicants'

class Corrector(models.Model):
    user             = models.ForeignKey('User', on_delete=models.CASCADE, null = True)
    company_email    = models.CharField(max_length = 50)
    is_authenticated = models.BooleanField(null=True)

    class Meta:
        db_table = 'correctors'