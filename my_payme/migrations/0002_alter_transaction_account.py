# Generated by Django 4.0.1 on 2022-02-22 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_payme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
