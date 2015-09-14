# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aclinic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('vdate', models.DateField(verbose_name='Дата приёма')),
                ('vhour', models.IntegerField(verbose_name='Час приёма', choices=[(9, '09:00'), (10, '10:00'), (11, '11:00'), (12, '12:00'), (14, '14:00'), (15, '15:00'), (16, '16:00'), (17, '17:00')])),
                ('detail', models.CharField(help_text='Пояснение (необязательное поле)', blank=True, max_length=500, null=True, verbose_name='Пояснение')),
                ('doctor_id', models.ForeignKey(help_text='Доктор (внешний ключ)', to='aclinic.Doctor', verbose_name='Доктор')),
            ],
            options={
                'verbose_name': 'Расписание приёма докторов',
                'ordering': ['vdate', 'doctor_id', 'vhour'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='receptiontime',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='receptiontime',
            name='doctor_id',
        ),
        migrations.DeleteModel(
            name='ReceptionTime',
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('doctor_id', 'vdate', 'vhour')]),
        ),
    ]
