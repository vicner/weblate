# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 08:53
from __future__ import unicode_literals

from django.db import migrations
import weblate.trans.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0080_auto_20170323_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autocomponentlist',
            name='component_match',
            field=weblate.trans.fields.RegexField(default=b'^$', help_text='Regular expression which is used to match component slug.', max_length=200, verbose_name='Component regular expression'),
        ),
        migrations.AlterField(
            model_name='autocomponentlist',
            name='project_match',
            field=weblate.trans.fields.RegexField(default=b'^$', help_text='Regular expression which is used to match project slug.', max_length=200, verbose_name='Project regular expression'),
        ),
    ]
