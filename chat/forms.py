from django import forms
from sqlalchemy import false

from .models import Discussion

class DiscussionModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    image=forms.ImageField(required=false)
    class Meta:
        model = Discussion
        fields = ('Discussion_name', )
