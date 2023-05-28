from django import forms
from .models import Newsletter

class EmailForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse email", required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Votre adresse email', 
        'maxlength': 255
    }))
    
    class Meta:
        model = Newsletter
        fields = ("email",)

