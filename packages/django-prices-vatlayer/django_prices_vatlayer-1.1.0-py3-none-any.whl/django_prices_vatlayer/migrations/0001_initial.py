# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 09:38
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=2, verbose_name='country code')),
                ('data', jsonfield.fields.JSONField(verbose_name='data')),
            ],
        ),
    ]
