# Generated by Django 4.2.13 on 2024-06-02 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField(default=False)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
            ],
        ),
    ]
