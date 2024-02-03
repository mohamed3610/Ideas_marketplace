from django.urls import path
from . import views

urlpatterns = [
    path("submit_idea" , views.submit_Idea , name = "submit_an_idea"),
    path("submit_files/<int:idea_id>",views.add_files , name="submit_files"),
    path("add_files/<int:idea_id>", views.add_files , name = "add_files"),
    path("add_tags/<int:idea_id>",views.add_tags ,name = "add_tags"),
    path("view_idea/<int:idea_id>",views.view_idea , name = "view_idea"),
    path("Download_data/<int:idea_id>",views.download_idea_files , name="download_files"),
    path("View_all_ideas" , views.view_Ideas , name="view_all_ideas"),
    path("add_scores/<int:idea_id>" , views.add_score , name="add_scores")
]
