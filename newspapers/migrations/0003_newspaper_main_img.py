# Generated by Django 4.1 on 2024-05-19 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspapers', '0002_alter_newspaper_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspaper',
            name='main_img',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
