from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email',  'password1', 'password2')

class LoginForm(forms.Form):

    username = forms.CharField(label='username', max_length=150)
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput)


class LeagueForm(forms.Form):
    
    name = forms.CharField(label='Leaguename', max_length=50)
