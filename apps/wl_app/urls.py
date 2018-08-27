from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^wishes/remove/(?P<wid>\d+)/(?P<uid>\d+)$', views.remove),
  url(r'^wishes/delete/(?P<wid>\d+)$', views.delete),
  url(r'^joinwish/(?P<wid>\d+)/(?P<uid>\d+)/$', views.joinwish),
  url(r'^wishes/item/(?P<wid>\d+)/$', views.wish),
  url(r'^logout$', views.logout),
  url(r'^home$', views.home),
  url(r'^wish/processwish/$', views.processwish),
  url(r'^wish_items/create$', views.getawish),
  url(r'^dashboard$', views.dashboard),
  url(r'^login$', views.login),
  url(r'^doregister$', views.doregister),
  url(r'^main$', views.index)     # This line has changed!
]
