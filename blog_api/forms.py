from django.contrib.auth.models import User
from django import forms
from .models import Post

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = {'username', 'email'}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
    

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields ={'label', 'text', 'tag'}
        
