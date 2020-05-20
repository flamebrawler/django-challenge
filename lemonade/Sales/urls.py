from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/report/', views.report, name='report'),
    path('sales/form/', views.form, name='form'),
    path("sales/report/<int:employee>/start=<str:start>/end=<str:end>/", views.report_table,name='table')

]
