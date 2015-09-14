# -*- coding: utf-8 -*- 

from django.db import models

# Create your models here.


import re

from django.contrib.auth.models import User

from aclinic.utils import fio_clean, get_nextval_from_sequence
from aclinic.consts import DB_USING, DB_SQLITE, DB_POSTGRESQL



class Doctor(models.Model):
    """ Таблица описания докторов """

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктор'
        ordering = ['speciality', 'fio']
        unique_together = (('speciality', 'fio',),)


    PROFESSION = (
        ('010', 'Терапевт'),
        ('020', 'Хирург'),
        ('030', 'Окулист'),
    )


    # Поле: Специальность доктора
    speciality = models.CharField(
            max_length=3,
            null=False,
            choices=PROFESSION, 
            verbose_name='Специальность доктора',
            help_text='',
            )

    # Поле: ФИО доктора
    fio = models.CharField(
            max_length=150,
            null=False,
            verbose_name='ФИО доктора',
            help_text='',
            )


    @classmethod
    def get_speciality(cls, code_speciality):
        """ 
        Метод класса.
        Возвращает строковое представление специальности доктора.
        """
        for speciality in cls.PROFESSION:
            if speciality[0] == code_speciality:
                return speciality[1]
        return None


    def save(self, *args, **kwargs):
        """ 
        Переопределение метода: приведение поля fio к виду 'Слово Слово...'
        """
        self.fio = fio_clean(self.fio)

        # Вызов метода-предка
        super(Doctor, self).save(*args, **kwargs)


    def read_speciality(self):
        """ Возвращает строковое представление специальности доктора """
        for speciality in self.PROFESSION:
            if speciality[0] == self.speciality:
                return speciality[1]
        return None
    read_speciality.admin_order_field = 'speciality'
    read_speciality.short_description = 'Специальность доктора'


    def __str__(self):
        return self.read_speciality() + ' ' + self.fio



class Schedule(models.Model):
    """ Таблица расписания приёма докторов """

    class Meta:
        verbose_name = 'Расписание приёма докторов'
        verbose_name_plural = 'Расписание приёма докторов'
        ordering = ['vdate', 'doctor_id', 'vhour']
        unique_together = (('doctor_id', 'vdate', 'vhour',),)


    RECEPTION_HOUR = (
        (9, '09:00'),
        (10, '10:00'),
        (11, '11:00'),
        (12, '12:00'),
        (14, '14:00'),
        (15, '15:00'),
        (16, '16:00'),
        (17, '17:00'),
    )


    # Поле: Доктор (внешний ключ)
    doctor_id = models.ForeignKey(
            Doctor, 
            null=False, 
            verbose_name='Доктор',
            help_text='',
            db_index=True,
            )

    # Поле: Дата приёма
    vdate = models.DateField(
            null=False,
            verbose_name='Дата приёма', 
            help_text='',
            )

    # Поле: Час приёма
    vhour = models.IntegerField(
            choices=RECEPTION_HOUR, 
            null=False, 
            verbose_name='Час приёма', 
            help_text='',
            )

    # Поле: Пояснение
    detail = models.CharField(
            max_length=500, 
            null=True, 
            blank=True, 
            verbose_name='Пояснение', 
            help_text='(необязательное поле)',
            )


    def read_doctor(self):
        """ Возвращает строковое представление доктора """
        return str(self.doctor_id)
    read_doctor.admin_order_field = 'doctor_id__fio'
    read_doctor.short_description = 'Доктор'


    def read_reception_date(self):
        """ Возвращает строковое представление даты приёма """
        return self.vdate.strftime('%d.%m.%Y') 
    read_reception_date.admin_order_field = 'vdate'
    read_reception_date.short_description = 'Дата приёма'


    def read_reception_hour(self):
        """ Возвращает строковое представление часа приёма """
        for hour in self.RECEPTION_HOUR:
            if hour[0] == self.vhour:
                return hour[1]
        return None
    read_reception_hour.admin_order_field = 'vhour'
    read_reception_hour.short_description = 'Час приёма'


    def read_reception_datehour(self):
        """ Возвращает строковое представление даты и часа приёма """
        return self.read_reception_date() + ' ' + self.read_reception_hour()
    read_reception_datehour.short_description = 'Дата и время приёма'


    def __str__(self):
        return self.read_reception_datehour() + ' ' + self.read_doctor()



if DB_USING == DB_SQLITE:

    class AdmissionHStatusSeq(models.Model):
        """
        Класс для аналога последовательности (sequence) из PostgreSQL.
        admission_hstatus_seq - уникальный ключ для создания нескольких записей 
        о приёме со статусом Отменён.
        """

        class Meta:
            db_table = 'admission_hstatus_seq'
            verbose_name = 'Последовательность отменённых записей о приёме'


        # Поле: Текущее значение последовательности
        nextval = models.IntegerField(
                null=False, 
                default=0, 
                verbose_name='Текущее значение',
                help_text=''
                )


elif DB_USING == DB_POSTGRESQL:
    pass
    """
    class AdmissionHStatusSeq(models.Model):
        "" "
        Класс соотноситя с последовательностью (sequence) из PostgreSQL.
        aclinic.public.admission_hstatus_seq - уникальный ключ для создания 
        нескольких записей о приёме со статусом Отменён.
        "" "

        class Meta:
            db_table = 'admission_hstatus_seq'
            verbose_name = 'Последовательность отменённых записей о приёме'

        sequence_name = models.CharField(max_length=128, primary_key=True)
        last_value = models.IntegerField()
        increment_by = models.IntegerField()
        max_value = models.IntegerField()
        min_value = models.IntegerField()
        cache_value = models.IntegerField()
        log_cnt = models.IntegerField()
        is_cycled = models.BooleanField()
        is_called = models.BooleanField()
    """



class Admission(models.Model):
    """ Таблица для записи на приём """

    class Meta:
        verbose_name = 'Запись на приём'
        verbose_name_plural = 'Запись на приём'
        ordering = ['schedule_id']
        unique_together = (('schedule_id', 'status', 'hstatus_seq'),)


    ADMISSION_STATUS = (
        (0, 'Ожидает'),
        (1, 'Проведён'),
        (2, 'Отменён'),
    )


    # Поле: Время приёма к доктору по расписанию (внешний ключ)
    schedule_id = models.ForeignKey(
            Schedule, 
            null=False, 
            verbose_name='Время приёма к доктору по расписанию',
            help_text='', 
            db_index=True,
            )

    # Поле: Статус приёма
    status = models.IntegerField(
            choices=ADMISSION_STATUS, 
            null=False, 
            blank=True,
            editable=False,
            default=ADMISSION_STATUS[0][0],
            verbose_name='Статус приёма', 
            help_text='',
            db_index=True,
            )

    # Поле: Вспомогательное поле: для возможности создания нескольких записей 
    # со статусом Отменён, заполняется последующим значением последовательности 
    # AdmissionHStatusSeq
    hstatus_seq = models.IntegerField(
            null=False, 
            blank=True,
            editable=False,
            default=0,
            verbose_name='Последовательность отменённых записей о приёме', 
            help_text='',
            )

    # Поле: ФИО клиента
    fio = models.CharField(
            max_length=150, 
            null=False, 
            verbose_name='ФИО клиента', 
            help_text='',
            )

    # Поле: Телефон клиента
    phone = models.CharField(
            max_length=20, 
            null=True,
            blank=True, 
            verbose_name='Телефон клиента', 
            help_text='',
            )

    # Поле: Email клиента
    email = models.EmailField(
            max_length=254, 
            null=True, 
            blank=True, 
            verbose_name='Email клиента', 
            help_text='',
            )


    def save(self, *args, **kwargs):
        """ 
        Переопределение метода: 
            1. в случае статуса Отменён заполнение поля hstatus_seq уникальным 
        значением; 
            2. приведение поля fio к виду 'Слово Слово...'.
        """
        # в случае статуса Отменён заполнение поля hstatus_seq уникальным 
        # значением
        if self.status == self.ADMISSION_STATUS[2][0]:
            self.hstatus_seq = get_nextval_from_sequence(AdmissionHStatusSeq)
        
        # приведение поля fio к виду 'Слово Слово...'
        self.fio = fio_clean(self.fio)

        # Вызов метода-предка
        super(Admission, self).save(*args, **kwargs)


    def read_schedule(self):
        """ Возвращает строковое представление расписания """
        return str(self.schedule_id)
    read_schedule.admin_order_field = 'schedule_id'
    read_schedule.short_description = 'Расписание'


    def read_status(self):
        """ Возвращает строковое представление статуса приёма """
        for status in self.ADMISSION_STATUS:
            if status[0] == self.status:
                return status[1]
        return None
    read_status.admin_order_field = 'status'
    read_status.short_description = 'Статус приёма'


    def read_client(self):
        """ Возвращает строковое представление данных клиента """
        client = self.fio
        if self.phone is not None and self.phone != '':
            client += ' ' + self.phone
        if self.email is not None and self.email != '':
            client += ' ' + self.email
        return client
    read_client.admin_order_field = 'fio'
    read_client.short_description = 'Клиент'


    def __str__(self):
        return self.read_schedule() + '(' + self.read_status() + ') ' + \
                self.read_client()