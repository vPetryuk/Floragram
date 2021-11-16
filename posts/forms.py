from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    # image =forms.ImageField(widget = forms.HiddenInput())
    class Meta:
        model = Post
        fields = ('image' ,'content' )

class PostHistoryModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image',)

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
