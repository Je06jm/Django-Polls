from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.question_api, name="question"),
    path("vote", views.vote_api, name="vote"),
]
