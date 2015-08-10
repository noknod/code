# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lpforms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formpostseq',
            old_name='last_value',
            new_name='nextval',
        ),
    ]
