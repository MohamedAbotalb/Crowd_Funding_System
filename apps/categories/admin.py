from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ['name']
    list_per_page = 10
    list_max_show_all = 10
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )


admin.site.register(Category, CategoryAdmin)
