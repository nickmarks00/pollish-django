# Generated by Django 4.0.1 on 2022-03-28 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pollish', '0018_rename_image_src_pollimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='choice',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='pollish.choice'),
            preserve_default=False,
        ),
    ]
