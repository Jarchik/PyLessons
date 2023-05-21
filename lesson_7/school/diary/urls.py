from django.urls import path
from . import views

urlpatterns = [
    path("week/", views.my_week, name="my_week"),
    path("day/<int:week_day_id>/", views.my_day, name="my_day"),
    path("day/<int:day_id>/note/<int:note_id>/", views.my_note, name="my_note"),
]
