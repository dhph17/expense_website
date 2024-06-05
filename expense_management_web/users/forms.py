from django import forms

class registerForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    repassword = forms.CharField(label='Re-Password', max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=100)

class loginForm(forms.Form):
    username = forms.CharField(label='Username or Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
