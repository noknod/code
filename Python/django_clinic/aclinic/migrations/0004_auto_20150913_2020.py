# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aclinic', '0003_auto_20150913_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionHStatusSeq',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nextval', models.IntegerField(default=0, verbose_name='Текущее значение')),
            ],
            options={
                'verbose_name': 'Последовательность отменённых записей о приёме',
                'db_table': 'admission_hstatus_seq',
            },
        ),
        migrations.AddField(
            model_name='admission',
            name='hstatus_seq',
            field=models.IntegerField(blank=True, default=0, verbose_name='Последовательность отменённых записей о приёме', editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='admission',
            unique_together=set([('schedule_id', 'status', 'hstatus_seq')]),
        ),
    ]
