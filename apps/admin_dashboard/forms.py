from apps.projects.forms import ProjectForm
from django import forms

class ProjectFormWithImage(ProjectForm):
    image = forms.ImageField(
        label='Image', 
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta(ProjectForm.Meta):
        fields = ProjectForm.Meta.fields + ('image',)
