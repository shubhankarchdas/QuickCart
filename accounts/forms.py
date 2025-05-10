from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control'
    }))


    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number','email', 'password')

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
