from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_financiera_view, name='dashboard_financiera_view'),
]
