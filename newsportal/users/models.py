from django.db import models
from django.utils.safestring import mark_safe
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
    phone = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=20, null=True)
    second_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    account_image = models.ImageField(default='default.jpg', upload_to='account_images')
    address = models.CharField(max_length=150, null=True)
    vk = models.CharField(max_length=100, null=True)
    instagram = models.CharField(max_length=100, null=True)
    telegram = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username}'s account"
    
    class Meta:
        ordering = ['user', 'email']
        verbose_name = 'Аккуант'
        verbose_name_plural = 'Аккаунты'


# class Image(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, blank=True)
#     image = models.ImageField(upload_to='account_images/')

#     def __str__(self):
#         return self.title

#     def image_tag(self):
#         if self.image is not None:
#             return mark_safe(f'<img src="{self.image.url}" height="40px" width="auto" />')
#         else:
#             return '(no image)'
        
#     class Meta:
#         # ordering = ['title','date']
#         verbose_name= 'Картинка аккаунта'
#         verbose_name_plural='Картинки аккаунтов'
