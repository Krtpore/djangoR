from django import forms
from .validators import russian_email #username_check, 
from django.core.validators import MinLengthValidator

class ContactForm(forms.Form):
    username = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2)],
                           help_text='Максимум 100 символов')
    email = forms.EmailField(validators=[russian_email],
                            help_text='разрешены только домены @mail.ru, @bk.ru или @yandex.ru')
    message = forms.CharField(widget=forms.Textarea)
    agree_field = forms.BooleanField(label='Даю согласие на обработку персональных данных', required= True)