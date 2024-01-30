from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.index,name='index'),
    path('get_report/',views.get_report,name='get_report'),
    path('remove_all_products/', views.remove_all_products, name='remove_all_products'),

]