from django import forms
from .models import Account, ProfileUser


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'form-control'
        }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
        }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone','password']
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'First Name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Last Name'
        self.fields['email'].widget.attrs['placeholder']= 'Email Address'
        self.fields['phone'].widget.attrs['placeholder']= 'Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password doesn't match!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'First Name'
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

class ProfileUserForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid': ('Image files only!')}, widget=forms.FileInput)
    class Meta:
        model = ProfileUser
        fields = ['address_line_1','address_line_2','profile_picture','city','state','country','pincode']
    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'





# class RegistrationForm(forms.ModelForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder':'First Name',
#         'class':'form-control'
#         }))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder':'Last Name',
#         'class':'form-control'
#         }))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={
#         'placeholder':'Email Address',
#         'class':'form-control'
#         }))
#     phone = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder':'Phone Number',
#         'class':'form-control'
#         }))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder':'Password',
#         'class':'form-control'
#         }))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'placeholder':'Confirm Password',
#         'class':'form-control'
#         }))
#     class Meta:
#         model = Account
#         fields = ['first_name','last_name','email','phone','password']