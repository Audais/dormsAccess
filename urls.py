"""mobApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from mobapp.views import *

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^admin/$', index, name='admin'),
    url(r'^visitor/$', index, name='visitor'),
    url(r'^login_mobile/$', login_mobile, name='login_mobile'),
    url(r'^get_name_mobile/$', get_name_mobile, name='get_name_mobile'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^add_resident/$', add_resident, name='add_resident'),
    url(r'^resident_access/$', resident_access, name='resident_access'),
    url(r'^visitor_access/$', visitor_access, name='visitor_access'),
    url(r'^signup_mobile/$', signup_mobile, name='signup_mobile'),
    url(r'^blacklist/$', blacklist, name='blacklist'),
    url(r'^display_all_logs/$', display_all_logs, name='display_all_logs'),
    url(r'^display_resident_logs/$', display_resident_logs, name='display_resident_logs'),
    url(r'^display_visitor_logs/$', display_visitor_logs, name='display_visitor_logs'),
    url(r'^admin_visitors/$', admin_visitors, name='admin_visitors'),
    url(r'^admin_visitors_access/$', admin_visitors_access, name='admin_visitors_access'),
    
]
