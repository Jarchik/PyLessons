from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("week/", views.my_week, name="my_week"),
    path("day/<int:week_day_id>/", views.my_day, name="my_day"),
    path("note/<int:note_id>/", views.my_note, name="my_note"),
    path("day/<int:week_day_id>/add_note/", views.add_note, name="new_note"),
]
