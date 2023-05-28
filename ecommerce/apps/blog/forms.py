from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from mptt.forms import TreeNodeChoiceField


class CommentForm(forms.ModelForm):
    
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
    
    name = forms.CharField(label='Votre nom', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Votre nom & prénom',
        'maxlenght': '200'
    }))
    email = forms.EmailField(label='Adresse email', required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Votre adresse email'
    }))
    
    content = forms.CharField(label='Message', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Votre message',
        'cols': '20',
        'rows': '15'
    }))
    class Meta:
        model = Comment
        fields = ("name", "email", "content", "post")
        
    
    def save(self, *args, **kwargs) -> Any:
        Comment.objects.rebuild()
        return super(CommentForm, self).save(*args, **kwargs)
