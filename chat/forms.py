from django import forms
from sqlalchemy import false

from .models import Discussion

class DiscussionModelForm(forms.ModelForm):
    Discussion_name = forms.CharField(widget=forms.Textarea(attrs={'rows':1}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    slug = forms.CharField(widget = forms.HiddenInput(),required=False)
    author = forms.CharField(widget = forms.HiddenInput(),required=False)
    image =forms.ImageField(required=False)
    class Meta:
        model = Discussion
        fields = ('Discussion_name','content','image')
