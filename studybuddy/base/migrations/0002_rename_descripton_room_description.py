# Generated by Django 5.0.7 on 2024-07-17 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='descripton',
            new_name='description',
        ),
    ]
