from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import RegexValidator


class CustomUser(User):
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex='^\+201(0|1|2|5)\d{8}$', message='Enter a valid Egyptian phone number.')], unique=True)
    profile_picture = models.ImageField(upload_to='user_upload/', null=True, blank=True, default='user_upload/default_profile_pictures.jpg')
    facebook_profile = models.URLField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    @property
    def profile_picture_url(self):
        return f'/media/{self.profile_picture}'
    