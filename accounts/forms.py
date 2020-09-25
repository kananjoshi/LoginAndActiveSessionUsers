from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()

    # extra field
    phone_no = forms.CharField(max_length=10)
    description = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2','description']

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no', None)
        try:
            if not phone_no.is_digit() and len(phone_no) != 10:
                raise ValidationError('Please enter a valid phone number, Length must be bbetween 10 to 15 digits.')
        except (ValueError, TypeError):
            raise ValidationError('Please enter a valid phone number')
        return phone_no

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.extra_field = self.cleaned_data["description"]
        if commit:
            user.save()
        return user