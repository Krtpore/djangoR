from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    gender_choises= (('M', 'Male'),
                     ('F', 'Female'),
                     ('N/A', 'No answer'))
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    gender = models.CharField(choices=gender_choises, max_length=20)
    email = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=20, null=True)
    second_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    account_image = models.ImageField(default='default.jpg', upload_to='account_images')

    def __str__(self):
        return f"{self.user.username}'s account"
    
    class Meta:
        ordering = ['user', 'email']
        verbose_name = 'Аккуант'
        verbose_name_plural = 'Аккаунты'