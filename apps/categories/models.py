from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    @classmethod
    def get_category_by_slug(cls, slug):
        return get_object_or_404(cls, slug=slug)

    @classmethod
    def get_all_categories(cls):
        categories = cls.objects.all()
        return categories

    @property
    def show_url(self):
        return reverse("category_show", args=[self.slug])

    @property
    def update_url(self):
        return reverse('category_update', args=[self.slug])

    @property
    def delete_url(self):
        return reverse('category_delete', args=[self.slug])
