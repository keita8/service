from django import forms 
from .models import *


class ContactForm(forms.ModelForm):
    required_css_class= "required-field"
    error_css_class = "error-field"
    style="resize"
    
    name = forms.CharField(label="Votre nom", widget=forms.TextInput(attrs={
        'placeholder': "Votre nom",
        "id": "contact-name",
        }), 
        required=True, )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id": "contact-email",
        "max_length": 255,
        "placeholder": "Votre adresse email"
        
    }))
    
    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'placeholder': "Laissez votre message",
            "id":"contact-message",
            
        }
    ))
    
    class Meta:
        model = Contact 
        fields = ('name', 'email', 'subject', 'message')
    
    