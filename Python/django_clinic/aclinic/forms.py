from django.forms import ModelForm, ValidationError, ChoiceField, ModelChoiceField, Form


import datetime


from aclinic.models import Admission, Schedule, Doctor
from aclinic.consts import BLANK_CHOICE


class AdmissionForm(ModelForm):

    class Meta:
        model = Admission
        fields = ['schedule_id', 'fio', 'phone', 'email']


    def __init__(self, *args, **kwargs):
        """ 
        Переопределение метода: отображение только свбодных приёмов
        """
        # Вызов метода-предка
        super (AdmissionForm, self ).__init__(*args, **kwargs)

        # Получение для отображения списка только свбодных приёмов
        self.fields['schedule_id'].queryset = Schedule.objects.exclude(
                id__in = Admission.objects.filter(
                        status=0).values_list('schedule_id', flat=True))


    def clean(self, *args, **kwargs):
        """ 
        Переопределение метода: проверка на то, что время приёма свбодно
        """
        # Вызов метода-предка и получение значений полей формы
        cleaned_data = super(AdmissionForm, self).clean()

        schedule_id = cleaned_data.get('schedule_id')
        status = cleaned_data.get('status')
        if status is None:
            status = Admission.ADMISSION_STATUS[0][0]

        if Admission.objects.filter(
                schedule_id=schedule_id.id, status=status).exists():
            raise ValidationError(
                    #_('Время %(datehour)s %(doctor)s, к сожалению, занято'),
                    'Время %(datehour)s %(doctor)s, к сожалению, занято',
                    code='invalid',
                    params={'datehour': schedule_id.read_reception_datehour(), 
                            'doctor': schedule_id.read_doctor()}
                )

        return cleaned_data



class SpecialityChooseForm(Form):

    speciality = ChoiceField(
            choices=[],
            label='Специальность доктора',)


    def __init__(self, days_ahead, *args, **kwargs):
        """ 
        Переопределение метода: отображение специальностей только свободных 
        докторов на заданное время вперёд
        """
        # Вызов метода-предка
        super (SpecialityChooseForm, self ).__init__(*args, **kwargs)

        # Получение для отображения списка специальностей только свободных 
        # докторов на заданное время вперёд
        start_date = datetime.date.today() 
        end_date = start_date + datetime.timedelta(days=days_ahead)

        doctor_id_list = Schedule.objects.filter(
                    vdate__range=(start_date, end_date)
                ).exclude(
                    id__in = Admission.objects.filter(
                                status__in=[0, 1]
                            ).values_list('schedule_id', flat=True)
                ).values_list('doctor_id', flat=True)
        doctor_id_set = set(doctor_id_list)

        speciality_set = Doctor.objects.filter(
                    id__in=doctor_id_set
                ).values_list('speciality', flat=True)

        speciality_list = [BLANK_CHOICE]
        for speciality in speciality_set:
            speciality_list.append((speciality, 
                    Doctor.get_speciality(speciality),))
        
        #self.fields['speciality'].queryset = speciality_list
        self.fields['speciality'].choices = speciality_list



class DateChooseForm(Form):

    schedule = ChoiceField(
            choices=[],
            label='Дата и время приёма',)


    def __init__(self, days_ahead, speciality, *args, **kwargs):
        """ 
        Переопределение метода: отображение дат и времени приёма только 
        свободных докторов на заданное время вперёд
        """
        # Вызов метода-предка
        super (DateChooseForm, self ).__init__(*args, **kwargs)

        # Получение для отображения списка дат и времени приёма только 
        # свободных докторов на заданное время вперёд
        start_date = datetime.date.today() 
        end_date = start_date + datetime.timedelta(days=days_ahead)

        schedule_list = Schedule.objects.filter(
                    doctor_id__speciality__exact=speciality, 
                    vdate__range=(start_date, end_date)
                ).exclude(
                    id__in = Admission.objects.filter(
                                status__in=[0, 1]
                            ).values_list('schedule_id', flat=True)
                )

        schedules = [BLANK_CHOICE]
        for schedule in schedule_list:
            schedules.append((schedule.id, 
                    schedule.read_reception_datehour()),)

        #self.fields['speciality'].queryset = speciality_list
        self.fields['schedule'].choices = schedules