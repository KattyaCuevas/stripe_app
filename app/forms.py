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
            # 'plan',
        ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Username',
            'password': 'Contraseña',
            'email': 'Email',
            # 'plan': 'Plan',
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'username': forms.TextInput(),
            'password':  forms.PasswordInput(),
            'email': forms.EmailInput(),
            # 'plan',
        }
        # password = forms.CharField(max_length=128)
        # email = forms.EmailField( max_length=254)
        # stripe_id = forms.CharField(max_length=20)
        # plan = forms.CharField(max_length=100)
