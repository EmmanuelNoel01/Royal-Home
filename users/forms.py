from django import forms
from django.contrib.auth.forms import UserCreationForm
from custom_user.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

        date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y', attrs={'class':'datepicker'}),
        input_formats=('%m/%d/%Y', )
        )


class UserUpdateForm():
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm():
    class Meta:
        model = User
        fields = ['image']
