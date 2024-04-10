from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import RegexValidator


class CustomUser(User):
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex='^\+20\d{10}$', message='Enter a valid Egyptian phone number.')])
    profile_picture = models.ImageField(upload_to='user_upload/', null=True, blank=True, default='user_upload/default_profile_pictures.jpg')
    facebook_profile = models.URLField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
   
    @property
    def profile_picture_url(self):
        return f'/media/{self.profile_picture}'
    