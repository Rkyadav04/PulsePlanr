from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


# ---------------------------------------------------------
# User Registration Form
# ---------------------------------------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# ---------------------------------------------------------
# User Login Form
# ---------------------------------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



# ---------------------------------------------------------
# Invite Member Form
# ---------------------------------------------------------
class EmailInviteForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[
            ('manager', 'Manager'),
            ('employee', 'Employee'),
        ],
        label="Role",
        widget=forms.Select(attrs={'class': 'form-control'})
    )




