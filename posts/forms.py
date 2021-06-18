from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    # NameOfLower = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}))
    class Meta:
        model = Post
        fields = ('image' ,'content' )

class PostModelNameForm(forms.ModelForm):
    plant_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}))
    class Meta:
        model = Post
        fields = ('plant_name',)

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)
