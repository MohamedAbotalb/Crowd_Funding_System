from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class CustomUser(User):
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex='^01[0125]{1}[0-9]{8}$', message='Enter a valid Egyptian phone number.')], unique=True)
    profile_picture = models.ImageField(upload_to='user_uploads/', null=True, blank=True, default='user_uploads/default_profile_picture.jpg')
    facebook_profile = models.URLField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_picture_url(self):
        return f'/media/{self.profile_picture}'
