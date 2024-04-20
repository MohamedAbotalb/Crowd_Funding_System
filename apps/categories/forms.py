from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Description", "class": "form-control", "rows": 3}),
    )
