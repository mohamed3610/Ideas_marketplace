from django.urls import path
from . import views

urlpatterns = [
    path("" , views.register , name = "register"),
    path("login",views.login_employee , name = "login"),
]
