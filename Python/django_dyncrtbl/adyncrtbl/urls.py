from django.conf.urls import include, url



urlpatterns = [

    url(r'^$', 'adyncrtbl.views.form'),

    url(r'create/', 'adyncrtbl.views.create'),
]
