# Generated by Django 4.0.1 on 2022-02-25 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_profile_user'),
        ('pollish', '0012_profile')
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
