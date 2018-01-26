"""wds_backstage URL Configuration

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
from django.contrib import admin
from json_utils import views
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.index, name='home'),
    url(r'^reg/$', views.register, name='reg'),
    url(r'^ajax/$', views.ajax_aubmit, name='ajax'),
    url(r'^add/$', views.add, name='add'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test2/$', views.test2, name='test2'),
    url(r'^plus/$', views.plus, name='plus'),
    url(r'^count/$', views.count, name='count'),
    url(r'^sum/$', views.sum, name='sum'),
    url(r'^trans_time/$', views.trans_time, name='trans_time'),
    url(r'^pretty_body/$', views.pretty_body, name='pretty_body'),
]
