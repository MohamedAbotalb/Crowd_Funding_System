from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_all_categories(cls):
        categories = cls.objects.all()
        return categories

    @classmethod
    def get_category_by_name(cls, name):
        return get_object_or_404(cls, name=name)

    @property
    def show_url(self):
        return reverse("category_show", args=[self.name])

    @property
    def update_url(self):
        return reverse('category_update', args=[self.name])

    @property
    def delete_url(self):
        return reverse('category_delete', args=[self.name])
