from django import forms

class RegisterUser(forms.Form):
    password = forms.CharField(max_length=128, verbose_name='password')
    email = forms.EmailField( max_length=254, verbose_name='email address')
    stripe_id = forms.CharField(max_length=20)
    plan = forms.CharField(max_length=100)
