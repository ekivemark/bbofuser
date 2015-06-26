# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='affiliated_to',
            field=models.ForeignKey(default=b'', to='accounts.Organization', null=True),
        ),
    ]
