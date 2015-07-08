# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import oauth2_provider.validators
import oauth2_provider.generators
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=255, db_index=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('organization_role', models.CharField(max_length=30, choices=[('primary', 'Account Owner'), ('backup', 'Backup Owner'), ('member', 'Member'), ('none', 'NONE')], default='none', blank=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('carrier', models.CharField(max_length=100, choices=[('NONE', 'None'), ('3 river wireless', '3 river wireless(@sms.3rivers.net)'), ('acs wireless', 'acs wireless(@paging.acswireless.com)'), ('alltel', 'alltel(@message.alltel.com)'), ('at&t', 'at&t(@txt.att.net)'), ('bell canada', 'bell canada(@bellmobility.ca)'), ('bell mobility txt', 'bell mobility(@txt.bellmobility.ca)'), ('bell mobility (canada)', 'bell mobility (canada)(@txt.bell.ca)'), ('blue sky frog', 'blue sky frog(@blueskyfrog.com)'), ('bluegrass cellular', 'bluegrass cellular(@sms.bluecell.com)'), ('boost mobile', 'boost mobile(@myboostmobile.com)'), ('bpl mobile', 'bpl mobile(@bplmobile.com)'), ('carolina west wireless', 'carolina west wireless(@cwwsms.com)'), ('cellular one', 'cellular one(@mobile.celloneusa.com)'), ('cellular south', 'cellular south(@csouth1.com)'), ('centennial wireless', 'centennial wireless(@cwemail.com)'), ('centurytel', 'centurytel(@messaging.centurytel.net)'), ('cingular (now at&t)', 'cingular (now at&t)(@txt.att.net)'), ('clearnet', 'clearnet(@msg.clearnet.com)'), ('comcast', 'comcast(@comcastpcs.textmsg.com)'), ('corr wireless communications', 'corr wireless communications(@corrwireless.net)'), ('dobson', 'dobson(@mobile.dobson.net)'), ('edge wireless', 'edge wireless(@sms.edgewireless.com)'), ('fido', 'fido(@fido.ca)'), ('golden telecom', 'golden telecom(@sms.goldentele.com)'), ('helio', 'helio(@messaging.sprintpcs.com)'), ('houston cellular', 'houston cellular(@text.houstoncellular.net)'), ('idea cellular', 'idea cellular(@ideacellular.net)'), ('illinois valley cellular', 'illinois valley cellular(@ivctext.com)'), ('inland cellular telephone', 'inland cellular telephone(@inlandlink.com)'), ('mci', 'mci(@pagemci.com)'), ('metro pcs', 'metro pcs(@mymetropcs.com)'), ('metrocall', 'metrocall(@page.metrocall.com)'), ('metrocall 2-way', 'metrocall 2-way(@my2way.com)'), ('microcell', 'microcell(@fido.ca)'), ('midwest wireless', 'midwest wireless(@clearlydigital.com)'), ('mobilcomm', 'mobilcomm(@mobilecomm.net)'), ('mts', 'mts(@text.mtsmobility.com)'), ('nextel', 'nextel(@messaging.nextel.com)'), ('onlinebeep', 'onlinebeep(@onlinebeep.net)'), ('pcs one', 'pcs one(@pcsone.net)'), ('presidents choice', 'presidents choice(@txt.bell.ca)'), ('public service cellular', 'public service cellular(@sms.pscel.com)'), ('qwest', 'qwest(@qwestmp.com)'), ('rogers at&t wireless', 'rogers at&t wireless(@pcs.rogers.com)'), ('rogers canada', 'rogers canada(@pcs.rogers.com)'), ('satellink', 'satellink(@satellink.net)'), ('solo mobile', 'solo mobile(@txt.bell.ca)'), ('southwestern bell', 'southwestern bell(@email.swbw.com)'), ('sprint', 'sprint(@messaging.sprintpcs.com)'), ('sumcom', 'sumcom(@tms.suncom.com)'), ('surewest communications', 'surewest communications(@mobile.surewest.com)'), ('t-mobile', 't-mobile(@tmomail.net)'), ('telus', 'telus(@msg.telus.com)'), ('tracfone', 'tracfone(@txt.att.net)'), ('triton', 'triton(@tms.suncom.com)'), ('unicel', 'unicel(@utext.com)'), ('us cellular', 'us cellular(@email.uscc.net)'), ('us west', 'us west(@uswestdatamail.com)'), ('verizon', 'verizon(@vtext.com)'), ('virgin mobile', 'virgin mobile(@vmobl.com)'), ('virgin mobile canada', 'virgin mobile canada(@vmobile.ca)'), ('west central wireless', 'west central wireless(@sms.wcc.net)'), ('western wireless', 'western wireless(@cellularonewest.com)')], default='None', blank=True)),
                ('mfa', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=100, default='Terms of Use', blank=True)),
                ('version', models.CharField(max_length=20, blank=True)),
                ('terms_url', models.URLField(default='http://dev.bbonfhir.com/static/accounts/terms_of_use.html', verbose_name='Link to Terms')),
                ('effective_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('site_url', models.URLField(unique=True, default='', verbose_name='Site Home Page')),
                ('domain', models.CharField(unique=True, max_length=254, default='domain.com')),
                ('name', models.CharField(max_length=200, default='', blank=True)),
                ('privacy_url', models.URLField(default='http://', verbose_name='Privacy Terms Page')),
                ('alternate_owner', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, blank=True)),
                ('owner', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgApplication',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('client_id', models.CharField(unique=True, max_length=100, db_index=True, default=oauth2_provider.generators.generate_client_id)),
                ('redirect_uris', models.TextField(validators=[oauth2_provider.validators.validate_uris], help_text='Allowed URIs list, space separated', blank=True)),
                ('client_type', models.CharField(max_length=32, choices=[('confidential', 'Confidential'), ('public', 'Public')])),
                ('authorization_grant_type', models.CharField(max_length=32, choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')])),
                ('client_secret', models.CharField(db_index=True, max_length=255, default=oauth2_provider.generators.generate_client_secret, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('icon_link', models.URLField(null=True, default='', blank=True)),
                ('organization', models.ForeignKey(null=True, related_name='+', to='accounts.Organization', blank=True)),
                ('user', models.ForeignKey(related_name='accounts_orgapplication', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ValidSMSCode',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('sms_code', models.CharField(max_length=4, blank=True)),
                ('expires', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='affiliated_to',
            field=models.ForeignKey(null=True, default='', to='accounts.Organization'),
        ),
    ]
