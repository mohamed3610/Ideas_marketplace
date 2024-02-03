from django.urls import path
from . import views

urlpatterns = [
    path("register" , views.register , name = "register"),
    path("login",views.login_employee , name = "login"),
     path("", views.homePage , name="Home"),
     path("logout" , views.logout_employee , name = "logout")

]
