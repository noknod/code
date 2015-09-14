# -*- coding: utf-8 -*- 

from django.contrib import admin

# Register your models here.


from .models import Doctor, Schedule, Admission



class DoctorAdmin(admin.ModelAdmin):
    """ Представление таблицы докторов при администрировании  """

    list_display = ('speciality', 'fio',)

    list_filter = ('speciality', )

    search_fields = ('speciality', 'fio',)

    #inlines = [TradeOutletInline]



class ScheduleAdmin(admin.ModelAdmin):
    """ Представление таблицы расписания приёиа при администрировании  """

    list_display = ('read_reception_datehour', 'read_doctor', )

    list_filter = ('vdate', 'vhour', 'doctor_id__speciality',)

    search_fields = ('^doctor_id__speciality', )



class AdmissionAdmin(admin.ModelAdmin):
    """ Представление таблицы записи на приём при администрировании  """

    fieldsets = [
        (None,             {'fields': ['schedule_id', ]}),
        ('Клиент', {'fields': ['fio', 'phone', 'email'], 
                            #'classes': ['collapse']
                            }),
    ]

    list_display = ('read_schedule', 'read_status', 'read_client',)# 'detail',)

    list_filter = ('status', 'schedule_id__vdate', 'schedule_id__vhour', 
                   'schedule_id__doctor_id',)

    search_fields = ('^schedule_id__doctor_id__fio', 'fio',)



admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Admission, AdmissionAdmin)