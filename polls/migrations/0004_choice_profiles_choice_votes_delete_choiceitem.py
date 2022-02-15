# Generated by Django 4.0.1 on 2022-02-15 22:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_avatar_profile_bio_profile_updated_and_more'),
        ('polls', '0003_alter_poll_unique_together_remove_choice_votes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='profiles',
            field=models.ManyToManyField(related_name='choices', to='users.Profile'),
        ),
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.DeleteModel(
            name='ChoiceItem',
        ),
    ]
