from django.db import models


# Create your models here.

class CreatedTables(models.Model):

    class Meta:
        db_table = 'adyncrtbl_tables'

    title = models.CharField(max_length=30)
    fields = models.TextField()