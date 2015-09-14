# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aclinic', '0002_auto_20150913_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(editable=False, blank=True, choices=[(0, 'Ожидает'), (1, 'Проведён'), (2, 'Отменён')], default=0, db_index=True, verbose_name='Статус приёма')),
                ('fio', models.CharField(max_length=150, verbose_name='ФИО клиента')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон клиента', blank=True, null=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email клиента', blank=True, null=True)),
                ('schedule_id', models.ForeignKey(help_text='Время приёма к доктору по расписанию (внешний ключ)', to='aclinic.Schedule', verbose_name='Время приёма к доктору по расписанию')),
            ],
            options={
                'verbose_name': 'Запись на приём',
                'ordering': ['schedule_id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='admission',
            unique_together=set([('schedule_id', 'status')]),
        ),
    ]
