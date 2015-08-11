# -*- coding: utf-8 -*- 

from django.db import models


from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _



# Create your models here.

from .consts import * 


#def validate_domen(value):
#    """ Проверка введённого пользователем доменного имени """
#    if RE_VALID_DOMEN.match(value) is None:
#        raise ValidationError('%s не является верным доменным именем!' % value)



class Domain(models.Model):
    """ Таблица для хранения доменных имён """

    class Meta:
        verbose_name = 'Доменное имя'
        ordering = ['domain']

    # поле: Доменное имя
    domain = models.CharField(max_length=VALUE_DOMEN_MAXLENGTH, 
                             null=False, 
                             unique=True, 
                             verbose_name='Доменное имя', 
                             help_text='', 
                             db_index=True,
                             #validators=[validate_domen])
                             validators=[RegexValidator(regex=RE_VALID_DOMAIN, 
                                      message='Неверно указано доменное имя!')])

#    def clean(self):
#        print('\n***', get_nextval_from_sequence_sl(FormPostSeq), '\n')

    def __str__(self):
        return self.domain



class DomainForm(models.Model):
    """ Таблица описаний полей формы для данного доменного имени """

    class Meta:
        verbose_name = 'Поля формы'
        ordering = ['domain', 'fname']

    # поле: Внешний ключ на доменное имя
    domain = models.ForeignKey(Domain, 
                             verbose_name='Доменное имя', )

    # поле: Наименование поля
    fname = models.CharField(max_length=30,  
                             null=False, 
                             verbose_name='Наименование поля формы', 
                             help_text='', )

    # поле: Тип поля
    #"""
    FIELD_TYPES = (
        ('IR', 'Integer'),
        ('CR', 'Char'),
        ('TT', 'Text'),
    )
    #"""
    ftype = models.CharField(max_length=2,  
                             null=False, 
                             choices=FIELD_TYPES, 
                             verbose_name='Тип поля формы', 
                             help_text='')

    # поле: Длина поля (для строкового типа)
    length = models.IntegerField(null=True, 
                             blank=True, 
                             verbose_name='Длина поля (для строкового типа)', 
                             help_text='')

    # поле: Обязательность заполнения поля пользователем в форме
    required = models.BooleanField(null=False, 
                             blank=True, 
                             default=VALUE_REQUIRED_DEFAULT, 
                             verbose_name='Обязательность заполнения поля ' + 
                                          'пользователем в форме', 
                             help_text='')

    def clean(self):
        # Для поля с типом Char необходимо задать длину
        try:
            length = int(self.length)
        except:
            length = 0
        #print('\ndfqwe\n')
        #print(get_nextval_from_sequence(FormPostSeq))
        if self.ftype == 'CR' and not (length > 0):
            raise ValidationError(
                #_('Для поля с типом Char "' + '%(fname)' + '" необходимо задать длину'), 
                #_('Для поля с типом Char "(fname)" необходимо задать длину'), 
                'Для поля "{0}" необходимо задать длину!'.format(self.fname), 
                code='invalid',
                #params={'fname': self.fname},
                )

    def read_domain(self):
        """ Возвращает доменное имя """
        domain = Domain.objects.filter(id=self.domain.id)
        if len(domain) > 0:
            return domain[0].domain
        return '*Ошибка, домен с id={0} не найден!*'.format(self.id)
    read_domain.admin_order_field = 'domain'
    read_domain.short_description = 'Доменное имя'

    def read_ftype(self):
        """ Возвращает более читабельное представление для имени поля """
        for ftype in self.FIELD_TYPES:
            if ftype[0] == self.ftype:
                try:
                    length = int(self.length)
                except:
                    length = 0
                return ftype[1] + ((' ' + str(length)) if length > 0 else '')
        return '*Ошибка в типе поля {0}!*'.format(self.ftype)
    read_ftype.admin_order_field = 'ftype'
    read_ftype.short_description = 'Тип поля'

    def __str__(self):
        result = self.read_domain() + ': ' + self.fname
        result += ' (' + self.read_ftype() + ')'
        if self.required:
            result += ' обязательное'
        return  result



class FormSimple(models.Model):
    """ Таблица для хранения значений формы простого типа (Integer, Char) """

    class Meta:
        verbose_name = 'Значения формы простого типа (Integer, Char)'
        ordering = ['message_id', 'field_id']
        unique_together = (('message_id', 'field_id',),)

    # поле: Ключ определения соответствующего сообщения 
    message_id = models.IntegerField(null=False, 
                             blank=True, 
                             verbose_name='Ключ сообщения', 
                             help_text='', )

    # поле: Поле формы
    field_id = models.ForeignKey(DomainForm, 
                             null=False, 
                             #blank=False,
                             verbose_name='Поле формы', 
                             help_text='', )

    # поле: Значение, введённое пользователем
    fvalue = models.CharField(max_length=FIELD_CHAR_MAXLENGTH, 
                             null=True, 
                             blank=True, 
                             verbose_name='Значение, введённое пользователем', 
                             help_text='', )

    def read_domain(self):
        """ Возвращает доменное имя """
        return self.field_id.read_domain()
    #read_domain.admin_order_field = 'domain'
    read_domain.short_description = 'Доменное имя'

    def read_field(self):
        """ Возвращает поле формы """
        return self.field_id.fname
    #read_domain.admin_order_field = 'domain'
    read_field.short_description = 'Поле формы'

    def __str__(self):
        return str(self.field_id) + ': ' + self.fvalue[:VALUE_SIMPLE_SHOWLEN]



class FormText(models.Model):
    """ Таблица для хранения значений формы полного текста (Text) """

    class Meta:
        verbose_name = 'Значения формы полного текста (Text)'
        ordering = ['message_id', 'field_id']
        unique_together = (('message_id', 'field_id',),)

    # поле: Ключ определения соответствующего сообщения 
    message_id = models.IntegerField(null=False, 
                             blank=True, 
                             verbose_name='Ключ сообщения', 
                             help_text='', )

    # поле: Поле формы
    field_id = models.ForeignKey(DomainForm, 
                             null=False, 
                             #blank=False,
                             verbose_name='Поле формы', 
                             help_text='', )

    # поле: Значение, введённое пользователем
    fvalue = models.CharField(max_length=FIELD_CHAR_MAXLENGTH, 
                             null=True, 
                             blank=True, 
                             verbose_name='Значение, введённое пользователем', 
                             help_text='', )

    def read_domain(self):
        """ Возвращает доменное имя """
        return self.field_id.read_domain()
    #read_domain.admin_order_field = 'domain'
    read_domain.short_description = 'Доменное имя'

    def read_field(self):
        """ Возвращает поле формы """
        return self.field_id.fname
    #read_domain.admin_order_field = 'domain'
    read_field.short_description = 'Поле формы'

    def __str__(self):
        return str(self.field_id) + ': ' + self.fvalue[:VALUE_SIMPLE_SHOWLEN]



if DB_USING == DB_SQLITE:
    class FormPostSeq(models.Model):
        """
        Класс для аналога последовательности (sequence) из PostgreSQL.
        form_post_seq - уникальный ключ совокупности значений полей 
        заполненной одной формы
        """
        #sequence_name = models.IntegerField(primary_key=True)
        nextval = models.IntegerField(default=0)

        class Meta:
            db_table = u'form_post_seq'
elif DB_USING == DB_POSTGRESQL:
    pass
#class FormPostSeq(models.Model):
#    """
#    Класс соотноситя с последовательностью (sequence) из PostgreSQL.
#    lpforms.public.form_post_seq - уникальный ключ совокупности значений полей 
#    заполненной одной формы
#    """
#    sequence_name = models.CharField(max_length=128, primary_key=True)
#    last_value = models.IntegerField()
#    increment_by = models.IntegerField()
#    max_value = models.IntegerField()
#    min_value = models.IntegerField()
#    cache_value = models.IntegerField()
#    log_cnt = models.IntegerField()
#    is_cycled = models.BooleanField()
#    is_called = models.BooleanField()

#    class Meta:
#        db_table = u'form_post_seq'