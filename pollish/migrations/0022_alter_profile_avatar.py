# Generated by Django 4.0.1 on 2022-04-02 03:55

from django.db import migrations, models
import pollish.models


class Migration(migrations.Migration):

    dependencies = [
        ('pollish', '0021_alter_pollimage_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='no_picture.png', upload_to=pollish.models.Profile.profile_path),
        ),
    ]