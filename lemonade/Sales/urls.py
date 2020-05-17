from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/report/', views.report, name='report'),
    path('sales/form/', views.form, name='form'),
    path('sales/form/remove-<int:item>/', views.remove_item),
    path('sales/form/add-<int:item>/', views.add_item)
]
