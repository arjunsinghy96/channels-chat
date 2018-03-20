from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email',  'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control"
            }),
            'password1': forms.PasswordInput(attrs={
                "class": "form-control"
            }),
            'password2': forms.PasswordInput(attrs={
                "class": "form-control"
            }),
        }

class LoginForm(forms.Form):

    username = forms.CharField(label='username', max_length=150)
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))


class LeagueForm(forms.Form):
    
    name = forms.CharField(label='Leaguename', max_length=50)
