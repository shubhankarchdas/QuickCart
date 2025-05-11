# accounts/forms.py
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validate_email(email)  # Basic email validation
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match!")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter Your Last Name'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter Your Phone Number'  
        self.fields['email'].widget.attrs['placeholder']= 'Enter Your Email Address'
        self.fields['password'].widget.attrs['placeholder']= 'Enter Your Password'
        self.fields['confirm_password'].widget.attrs['placeholder']= 'Confirm Your Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
