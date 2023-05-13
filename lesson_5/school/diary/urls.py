from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("select_course/", views.select_course, name="select_course"),
    path("get_grade/", views.get_grade, name="get_grade"),
    path("login/", views.login, name="login"),
]