from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^books$', views.main_page),
    url(r'^add_book$', views.add_book),
    url(r'^books/(?P<id>\d+)$', views.view_book),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^unfavorite/(?P<id>\d+)$', views.unfavorite),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^favorite1/(?P<id>\d+)$', views.favorite1),
    url(r'^delete$', views.delete),
    url(r'^logout$', views.logout),
]
