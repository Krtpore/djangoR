from django import forms
from .validators import russian_email #username_check, 
from django.core.validators import MinLengthValidator
from profanity.validators import validate_is_profane

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, Select

from .models import *


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2), validate_is_profane],
                           help_text='Максимум 100 символов')
    email = forms.EmailField(validators=[russian_email],
                            help_text='разрешены только домены @mail.ru, @bk.ru или @yandex.ru')
    message = forms.CharField(widget=forms.Textarea,
                              validators=[validate_is_profane])
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'message']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {'username': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'username'}),
                   'email': EmailInput({'class': 'textinput form-control',
                                        'placeholder': 'email'}),
                   'first_name': TextInput({'class': 'textinput form-control',
                                            'placeholder': 'First name'}),
                   'last_name': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'Last name'}),
                   }

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['phone', 'address','vk','instagram','telegram', 'account_image']
        widgets = {'phone': TextInput({'class': 'textinput form-control',
                                       'placeholder': 'phone number'}),
                   'address': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'address'}),
                   'vk': TextInput({'class': 'textinput form-control',
                                      'placeholder': 'vk'}),
                   'instagram': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'instagram'}),
                   'telegram': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'telegram'}),
                   'account_image': FileInput({'class': 'form-control',
                                       'placeholder': 'image'})
                   }