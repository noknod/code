from django.shortcuts import render

# Create your views here.


#from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect#, HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseServerError
from django.core.urlresolvers import reverse

from django.core.context_processors import csrf


from aclinic.models import Doctor, Schedule, Admission
from aclinic.forms import AdmissionForm, SpecialityChooseForm, DateChooseForm
from aclinic.utils import get_coupon_from_admission
from aclinic.consts import FIND_ADMISSION_DAYS_AHEAD, BLANK_CHOICE



def index(request):
    template = 'clinic_index.html'
    context = {}
    return render(request, template, context)



def registration_choose_speciality(request):
    if request.method == 'POST':
        method = request.POST.get('_method', None)
        if  method == 'DELETE':
            if 'reg_speciality' in request.session:
                del request.session['reg_speciality']
            return HttpResponseRedirect('/clinic/')
        else:
            reg_speciality = request.POST.get('speciality')
            if reg_speciality == BLANK_CHOICE[0]:
                request.session['reg_speciality'] = reg_speciality
                return HttpResponseRedirect('/clinic/registration/speciality/')
            request.session['reg_speciality'] = reg_speciality
            return HttpResponseRedirect('/clinic/registration/date/')
    else:
        template = 'clinic_registration_choose_speciality.html'
        if 'reg_speciality' in request.session:
            speciality = request.session['reg_speciality']
        else:
            speciality = BLANK_CHOICE[0]
        form = SpecialityChooseForm(FIND_ADMISSION_DAYS_AHEAD, 
                initial={'speciality': speciality})
        context = {'form': form}
        context.update(csrf(request))
        return render(request, template, context)



def registration_choose_date(request):
    if request.method == 'POST':
        method = request.POST.get('_method', None)
        if  method == 'DELETE':
            if 'reg_schedule' in request.session:
                del request.session['reg_schedule']
            return HttpResponseRedirect('/clinic/registration/speciality/')
        else:
            reg_schedule = request.POST.get('schedule')
            if reg_schedule == BLANK_CHOICE[0]:
                request.session['reg_schedule'] = reg_schedule
                return HttpResponseRedirect('/clinic/registration/date/')
            request.session['reg_schedule'] = reg_schedule
            return HttpResponseRedirect('/clinic/registration/')
    else:
        if 'reg_speciality' in request.session:
            speciality = request.session['reg_speciality']
            if 'reg_schedule' in request.session:
                schedule = request.session['reg_schedule']
            else:
                schedule = BLANK_CHOICE[0]
            form = DateChooseForm(FIND_ADMISSION_DAYS_AHEAD, speciality, 
                    initial={'schedule': schedule})
            template = 'clinic_registration_choose_date.html'
            context = {'speciality': Doctor.get_speciality(speciality),
                       'form': form}
            return render(request, template, context)
        else:
            return HttpResponseRedirect('/clinic/registration/speciality/')



def registration(request):
    if request.method == 'POST':
        method = request.POST.get('_method', None)
        if  method == 'DELETE':
            return HttpResponseRedirect('/clinic/registration/date/')
        # create a form instance and populate it with data from the request:
        form = AdmissionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            admission = form.save(commit=True)

            coupon = get_coupon_from_admission(admission)

            # redirect to a new URL:
            request.session['coupon'] = coupon
            return HttpResponseRedirect('/clinic/registration/success')

    # if a GET (or any other method) we'll create a blank form
    else:
        if 'reg_schedule' in request.session:
            reg_schedule = request.session['reg_schedule']
        else:
            reg_schedule = ''
        form = AdmissionForm(initial={'schedule_id': reg_schedule})
    template = 'clinic_registration.html'
    context = {'form': form}
    context.update(csrf(request))
    return render(request, template, context)



def registration_success(request):
    template = 'clinic_registration_success.html'
    context = {}
    if 'coupon' in request.session:
        context['coupon'] = request.session['coupon']
        del request.session['coupon']
    if 'reg_schedule' in request.session:
        del request.session['reg_schedule']
    if 'reg_speciality' in request.session:
        del request.session['reg_speciality']
    return render(request, template, context)
