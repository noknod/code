# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('speciality', models.CharField(verbose_name='Специальность доктора', max_length=3, choices=[('010', 'Терапевт'), ('020', 'Хирург'), ('030', 'Окулист')])),
                ('fio', models.CharField(verbose_name='ФИО доктора', max_length=150)),
            ],
            options={
                'verbose_name': 'Доктор',
                'ordering': ['speciality', 'fio'],
            },
        ),
        migrations.CreateModel(
            name='ReceptionTime',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('vdate', models.DateField(verbose_name='Дата приёма')),
                ('vhour', models.IntegerField(verbose_name='Час приёма', choices=[(9, '09:00'), (10, '10:00'), (11, '11:00'), (12, '12:00'), (14, '14:00'), (15, '15:00'), (16, '16:00'), (17, '17:00')])),
                ('detail', models.CharField(blank=True, null=True, verbose_name='Пояснение', help_text='Пояснение (необязательное поле)', max_length=500)),
                ('doctor_id', models.ForeignKey(help_text='Доктор (внешний ключ)', verbose_name='Доктор', to='aclinic.Doctor')),
            ],
            options={
                'verbose_name': 'Время приёма',
                'ordering': ['vdate', 'doctor_id', 'vhour'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='doctor',
            unique_together=set([('speciality', 'fio')]),
        ),
        migrations.AlterUniqueTogether(
            name='receptiontime',
            unique_together=set([('doctor_id', 'vdate', 'vhour')]),
        ),
    ]
