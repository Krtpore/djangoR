# Generated by Django 4.2.7 on 2023-12-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_alter_image_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
