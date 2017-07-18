# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import weblate.trans.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0078_auto_20170322_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoComponentList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_match', weblate.trans.fields.RegexField(default=b'^.*$', help_text='Regular expression which is used to match project slug.', max_length=200, verbose_name='Project regular expression')),
                ('component_match', weblate.trans.fields.RegexField(default=b'^.*$', help_text='Regular expression which is used to match component slug.', max_length=200, verbose_name='Component regular expression')),
                ('componentlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trans.ComponentList', verbose_name='Component list to assign')),
            ],
            options={
                'verbose_name': 'Automatic component list',
                'verbose_name_plural': 'Automatic component lists',
            },
        ),
    ]
