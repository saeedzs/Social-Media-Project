from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','email',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput) this widget mask all characters typed in the password field
    
    
    
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget = forms.PasswordInput)
#     password2 = forms.CharField(widget = forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = {'username','email','first_name'}

#     def check_password(self):
#         if self.cleaned_data['password'] != self.cleaned_data['password2']:
#             raise forms.ValidationError('Passwords do not match')
#         return self.cleaned_data['password2']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields+('email','first_name')
        error_messages = {
            'username': { 'unique': "A user with that name already exists.",
                        "required" : "Your name must not be empty",

            }
        }