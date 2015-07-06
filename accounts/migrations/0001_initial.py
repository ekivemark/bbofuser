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
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('carrier', models.CharField(default=b'None', max_length=100, blank=True, choices=[(b'NONE', b'None'), (b'3 river wireless', b'3 river wireless(@sms.3rivers.net)'), (b'acs wireless', b'acs wireless(@paging.acswireless.com)'), (b'alltel', b'alltel(@message.alltel.com)'), (b'at&t', b'at&t(@txt.att.net)'), (b'bell canada', b'bell canada(@bellmobility.ca)'), (b'bell mobility txt', b'bell mobility(@txt.bellmobility.ca)'), (b'bell mobility (canada)', b'bell mobility (canada)(@txt.bell.ca)'), (b'blue sky frog', b'blue sky frog(@blueskyfrog.com)'), (b'bluegrass cellular', b'bluegrass cellular(@sms.bluecell.com)'), (b'boost mobile', b'boost mobile(@myboostmobile.com)'), (b'bpl mobile', b'bpl mobile(@bplmobile.com)'), (b'carolina west wireless', b'carolina west wireless(@cwwsms.com)'), (b'cellular one', b'cellular one(@mobile.celloneusa.com)'), (b'cellular south', b'cellular south(@csouth1.com)'), (b'centennial wireless', b'centennial wireless(@cwemail.com)'), (b'centurytel', b'centurytel(@messaging.centurytel.net)'), (b'cingular (now at&t)', b'cingular (now at&t)(@txt.att.net)'), (b'clearnet', b'clearnet(@msg.clearnet.com)'), (b'comcast', b'comcast(@comcastpcs.textmsg.com)'), (b'corr wireless communications', b'corr wireless communications(@corrwireless.net)'), (b'dobson', b'dobson(@mobile.dobson.net)'), (b'edge wireless', b'edge wireless(@sms.edgewireless.com)'), (b'fido', b'fido(@fido.ca)'), (b'golden telecom', b'golden telecom(@sms.goldentele.com)'), (b'helio', b'helio(@messaging.sprintpcs.com)'), (b'houston cellular', b'houston cellular(@text.houstoncellular.net)'), (b'idea cellular', b'idea cellular(@ideacellular.net)'), (b'illinois valley cellular', b'illinois valley cellular(@ivctext.com)'), (b'inland cellular telephone', b'inland cellular telephone(@inlandlink.com)'), (b'mci', b'mci(@pagemci.com)'), (b'metro pcs', b'metro pcs(@mymetropcs.com)'), (b'metrocall', b'metrocall(@page.metrocall.com)'), (b'metrocall 2-way', b'metrocall 2-way(@my2way.com)'), (b'microcell', b'microcell(@fido.ca)'), (b'midwest wireless', b'midwest wireless(@clearlydigital.com)'), (b'mobilcomm', b'mobilcomm(@mobilecomm.net)'), (b'mts', b'mts(@text.mtsmobility.com)'), (b'nextel', b'nextel(@messaging.nextel.com)'), (b'onlinebeep', b'onlinebeep(@onlinebeep.net)'), (b'pcs one', b'pcs one(@pcsone.net)'), (b'presidents choice', b'presidents choice(@txt.bell.ca)'), (b'public service cellular', b'public service cellular(@sms.pscel.com)'), (b'qwest', b'qwest(@qwestmp.com)'), (b'rogers at&t wireless', b'rogers at&t wireless(@pcs.rogers.com)'), (b'rogers canada', b'rogers canada(@pcs.rogers.com)'), (b'satellink', b'satellink(@satellink.net)'), (b'solo mobile', b'solo mobile(@txt.bell.ca)'), (b'southwestern bell', b'southwestern bell(@email.swbw.com)'), (b'sprint', b'sprint(@messaging.sprintpcs.com)'), (b'sumcom', b'sumcom(@tms.suncom.com)'), (b'surewest communications', b'surewest communications(@mobile.surewest.com)'), (b't-mobile', b't-mobile(@tmomail.net)'), (b'telus', b'telus(@msg.telus.com)'), (b'tracfone', b'tracfone(@txt.att.net)'), (b'triton', b'triton(@tms.suncom.com)'), (b'unicel', b'unicel(@utext.com)'), (b'us cellular', b'us cellular(@email.uscc.net)'), (b'us west', b'us west(@uswestdatamail.com)'), (b'verizon', b'verizon(@vtext.com)'), (b'virgin mobile', b'virgin mobile(@vmobl.com)'), (b'virgin mobile canada', b'virgin mobile canada(@vmobile.ca)'), (b'west central wireless', b'west central wireless(@sms.wcc.net)'), (b'western wireless', b'western wireless(@cellularonewest.com)')])),
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
                ('site_url', models.URLField(default=b'', unique=True, verbose_name=b'Site Home Page')),
                ('domain', models.CharField(default=b'domain.com', unique=True, max_length=254)),
                ('name', models.CharField(default=b'', max_length=200, blank=True)),
                ('privacy_url', models.URLField(default=b'http://', verbose_name=b'Privacy Terms Page')),
                ('alternate_owner', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('owner', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(default=oauth2_provider.generators.generate_client_id, unique=True, max_length=100, db_index=True)),
                ('redirect_uris', models.TextField(help_text='Allowed URIs list, space separated', blank=True, validators=[oauth2_provider.validators.validate_uris])),
                ('client_type', models.CharField(max_length=32, choices=[('confidential', 'Confidential'), ('public', 'Public')])),
                ('authorization_grant_type', models.CharField(max_length=32, choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')])),
                ('client_secret', models.CharField(default=oauth2_provider.generators.generate_client_secret, max_length=255, db_index=True, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('icon_link', models.URLField(default=b'', null=True, blank=True)),
                ('organization', models.ForeignKey(related_name='+', blank=True, to='accounts.Organization', null=True)),
                ('owner', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='accounts_orgapplication', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ValidSMSCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sms_code', models.CharField(max_length=4, blank=True)),
                ('expires', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='affiliated_to',
            field=models.ForeignKey(default=b'', to='accounts.Organization', null=True),
        ),
    ]
