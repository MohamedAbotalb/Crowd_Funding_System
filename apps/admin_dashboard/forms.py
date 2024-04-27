from django import forms
from apps.categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Description", "class": "form-control", "rows": 3}),
    )
