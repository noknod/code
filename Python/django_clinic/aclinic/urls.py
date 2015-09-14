# -*- coding: utf-8 -*- 

from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^$', views.index, name='clinic-index'),

    url(r'^registration/speciality/$', views.registration_choose_speciality, 
            name='clinic-registration-choose-speciality'),

    url(r'^registration/date/$', views.registration_choose_date, 
            name='clinic-registration-choose-date'),

    url(r'^registration/$', views.registration, name='clinic-registration'),

    url(r'^registration/success/$', views.registration_success, 
            name='clinic-registration-success'),
]



"""    url(r'^(?P<order_id>[0-9]+)/$', views.detail, name='lpform-detail'),
    url(r'^(?P<lpform_id>[0-9]+)/results/$', views.results, name='lpform-results'),
    url(r'^(?P<lpform_id>[0-9]+)/post/$', views.post, name='lpform-post'),
"""