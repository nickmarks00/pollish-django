# Generated by Django 4.0.1 on 2022-01-13 03:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('question_text', models.CharField(default='', max_length=120)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polls', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
                'unique_together': {('user', 'created')},
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(default='Option A', max_length=60)),
                ('votes', models.PositiveIntegerField(default=0)),
                ('poll', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='pollish.poll')),
            ],
        ),
    ]
