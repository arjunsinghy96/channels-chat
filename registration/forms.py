from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from registration.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='Username',
                                widget=forms.TextInput(
                                    attrs={
                                        'class':'form-control',
                                    })
                                )
    email = forms.EmailField(label='Email Address',
                             widget=forms.EmailInput(
                                    attrs={
                                        'class': 'form-control',
                                        })
                            )
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class':'form-control',
                                    })
                                )

    class Meta:
        model = User
        fields = ('username', 'email', 'password' )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    """
    Login Form used for authenticating users.
    """
    username = forms.CharField(label='Username',
                             widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        })
                            )
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class':'form-control',
                                    })
                                )
    
    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirmed_login_allowed(self.user)
        
        return self.cleaned_data

    def confirmed_login_allowed(self, user):
        """
        Checks if the user is active or not.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive'
            )
    
    def get_user(self):
        """
        Returns the user associated.
        """
        return self.user
