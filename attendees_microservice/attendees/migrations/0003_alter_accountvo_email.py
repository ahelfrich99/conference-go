# Generated by Django 4.1.7 on 2023-03-30 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_accountvo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountvo',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
