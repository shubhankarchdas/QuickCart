# accounts/forms.py
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from QCart.constants.error_message import ErrorMessage  # Import your custom messages
from django.contrib.auth.password_validation import validate_password

from accounts.models import Account, UserProfile

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError(ErrorMessage.E00001.value)  # Custom message
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

    
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', ErrorMessage.E00004.value)
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your Phone Number'  
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Your Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Your Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')