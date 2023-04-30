from django.urls import path
from . import views

urlpatterns = [
    path("submit_idea" , views.submit_Idea , name = "submit_an_idea"),
    path("submit_files/<int:idea_id>",views.add_files , name="submit_files")
]
