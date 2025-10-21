from django import forms
from .models import BlogPost, BlogComment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your blog title...',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your blog content here...',
                'rows': 8,
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*'
            })
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment-textarea',
                'placeholder': 'Write your comment...',
                'rows': 3,
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'comment-file-input',
                'accept': 'image/*'
            })
        }
