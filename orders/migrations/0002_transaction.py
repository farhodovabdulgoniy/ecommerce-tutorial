# Generated by Django 4.0.1 on 2022-02-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.CharField(max_length=255)),
                ('request_id', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('account', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[(0, 'processing'), (1, 'paid'), (2, 'failed')], default=0, max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('pay_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
