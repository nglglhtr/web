# Generated by Django 2.2.4 on 2020-10-13 02:25

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import economy.models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0020_auto_20200925_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(db_index=True, default=economy.models.get_time)),
                ('modified_on', models.DateTimeField(default=economy.models.get_time)),
                ('path', models.CharField(max_length=255)),
                ('reason', models.CharField(blank=True, max_length=255)),
                ('type', models.CharField(blank=True, max_length=255)),
                ('email_tag', models.CharField(blank=True, max_length=255)),
                ('product', models.CharField(blank=True, max_length=255)),
                ('era', models.CharField(blank=True, max_length=255)),
                ('comment', models.TextField(blank=True, default='', max_length=255)),
                ('url', models.URLField(db_index=True)),
                ('stats', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='upcomingdate',
            name='last_modified',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 10, 13, 2, 25, 34, 76819)),
        ),
    ]
