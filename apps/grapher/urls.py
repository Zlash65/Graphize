from django.conf.urls import url

from apps.grapher import views

urlpatterns = [
    url(r'^create-graphie/$', views.create_graphie, name='create-graphie'),
    url(r'^get-graphie-list/$', views.get_graphie_list, name='get-graphie-list'),
]
