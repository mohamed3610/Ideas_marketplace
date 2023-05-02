from django.urls import path
from . import views

urlpatterns = [
    path("submit_idea" , views.submit_Idea , name = "submit_an_idea"),
    path("submit_files/<int:idea_id>",views.add_files , name="submit_files"),
    path("add_files/<int:idea_id>", views.add_files , name = "add_files"),
    path("add_tags/<int:idea_id>",views.add_tags ,name = "add_tags"),
    path("view_idea/<int:idea_id>",views.view_idea , name = "view_idea"),
]
