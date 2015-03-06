# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('developer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='developer',
            old_name='termsAgreedDate',
            new_name='terms_agreed_date',
        ),
        migrations.RenameField(
            model_name='developer',
            old_name='userName',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='developer',
            old_name='userType',
            new_name='user_type',
        ),
        migrations.AddField(
            model_name='developer',
            name='agree_terms',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='developer',
            name='organization',
            field=models.CharField(default='America/New_York', max_length=100),
            preserve_default=False,
        ),
    ]
