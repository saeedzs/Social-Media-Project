from .models import Post,Comment
from django import forms

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','image','caption')

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control form-control-sm rounded-3 shadow-none',
                'rows': 2,
                'placeholder': 'Write a comment...',
                'style': 'resize: none; font-size: 0.875rem;'
            })
        }
