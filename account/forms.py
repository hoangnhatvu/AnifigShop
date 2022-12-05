from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)

    last_name = forms.CharField(max_length=100)

    email = forms.EmailField(max_length=50)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Nhập mật khẩu'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Xác nhận mật khẩu'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nhập tên'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nhập họ'
        self.fields['email'].widget.attrs['placeholder'] = 'Nhập email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Mật khẩu không khớp!'
            )

class UserForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
