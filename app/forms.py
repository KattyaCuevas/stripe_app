from django import forms
from app.models import StripeUser

class RegisterUser(forms.ModelForm):

    class Meta:
        model = StripeUser

        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Username',
            'password': 'Contraseña',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'username': forms.TextInput(),
            'password':  forms.PasswordInput(),
            'email': forms.EmailInput(),
        }

class LoginUser(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
