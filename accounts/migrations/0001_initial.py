# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address', db_index=True)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('organization_role', models.CharField(default=b'none', max_length=30, blank=True, choices=[(b'primary', b'Account Owner'), (b'backup', b'Backup Owner'), (b'member', b'Member'), (b'none', b'NONE')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(default=b'Terms of Use', max_length=100, blank=True)),
                ('version', models.CharField(max_length=20, blank=True)),
                ('terms_url', models.URLField(default=b'http://dev.bbonfhir.com/static/accounts/terms_of_use.html', verbose_name=b'Link to Terms')),
                ('effective_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200, blank=True)),
                ('site_url', models.URLField(default=b'', unique=True, verbose_name=b'Site Home Page')),
                ('privacy_url', models.URLField(default=b'http://', verbose_name=b'Privacy Terms Page')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='affiliated_to',
            field=models.ForeignKey(default=b'', blank=True, to='accounts.Organization'),
        ),
    ]
