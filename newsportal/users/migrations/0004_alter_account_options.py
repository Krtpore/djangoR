# Generated by Django 4.2.7 on 2023-12-22 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_tag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['user', 'email'], 'verbose_name': 'Аккуант', 'verbose_name_plural': 'Аккаунты'},
        ),
    ]
