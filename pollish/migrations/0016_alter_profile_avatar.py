# Generated by Django 4.0.1 on 2022-03-09 06:51

from django.db import migrations, models
import pollish.models


class Migration(migrations.Migration):

    dependencies = [
        ('pollish', '0015_choice_uuid_comment_uuid_poll_uuid_profile_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='no_picture.png'),
        ),
    ]
