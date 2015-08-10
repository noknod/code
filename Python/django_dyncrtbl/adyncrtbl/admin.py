from django.contrib import admin

from adyncrtbl.models import CreatedTables

from . import utils


# Register your models here.


class CreatedTablesAdmin(admin.ModelAdmin):
    pass


admin.site.register(CreatedTables, CreatedTablesAdmin)


utils.load_at_startup()