# Generated by Django 4.2.7 on 2023-12-23 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_account_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(upload_to='account_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.account')),
            ],
            options={
                'verbose_name': 'Картинка аккаунта',
                'verbose_name_plural': 'Картинки аккаунтов',
            },
        ),
    ]
