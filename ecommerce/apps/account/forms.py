from django import forms 
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()



class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirmez votre mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email deja associé à un autre compte.")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("Les mots de passe ne correspondent pas.")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirmez votre mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active',]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,  widget=forms.EmailInput(attrs={
        'placeholder': 'Votre adresse email en tant qu\'invité'
    }))
    

class UserLogin(forms.Form):
    username = forms.EmailField(label="Adresse email",required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Votre adresse email'
    }))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={
        'placeholder': 'Votre mot de passe'
    }))
    
    
class UserRegister(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder':"votre adresse email"
    }))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={
        'placeholder': 'Votre mot de passe'
    }))
    confirm_password = forms.CharField(label="Confirmez votre mot de passe", widget=forms.PasswordInput(attrs={
        'placeholder': 'Votre mot de passe de confirmation'
    }))
    
    

class UserDetailChangeForm(forms.ModelForm):
    lastname = forms.CharField(label='Nom de famille',required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Votre nom de famille'
    }))
    firstname = forms.CharField(label='Prénom',required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Votre prénom'
    }))
    class Meta:
        model = User 
        fields = ['email', ]