# Generated by Django 4.1 on 2024-05-19 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newspapers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspaper',
            options={'ordering': ['-published_date']},
        ),
    ]
