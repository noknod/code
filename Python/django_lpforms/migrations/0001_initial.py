# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('domain', models.CharField(verbose_name='Доменное имя', max_length=75, db_index=True, unique=True, validators=[django.core.validators.RegexValidator(message='Неверно указано доменное имя!', regex=re.compile('^([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,6}$', 32))])),
            ],
            options={
                'verbose_name': 'Доменное имя',
                'ordering': ['domain'],
            },
        ),
        migrations.CreateModel(
            name='DomainForm',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('fname', models.CharField(verbose_name='Наименование поля формы', max_length=30)),
                ('ftype', models.CharField(verbose_name='Тип поля формы', max_length=2, choices=[('IR', 'Integer'), ('CR', 'Char'), ('TT', 'Text')])),
                ('length', models.IntegerField(blank=True, verbose_name='Длина поля (для строкового типа)', null=True)),
                ('required', models.BooleanField(verbose_name='Обязательность заполнения поля пользователем в форме', default=False)),
                ('domain', models.ForeignKey(verbose_name='Доменное имя', to='lpforms.Domain')),
            ],
            options={
                'verbose_name': 'Поля формы',
                'ordering': ['domain', 'fname'],
            },
        ),
        migrations.CreateModel(
            name='FormPostSeq',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('last_value', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'form_post_seq',
            },
        ),
    ]
