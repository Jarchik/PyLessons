from random import randint
import re
from typing import Union
from django.http import HttpResponse
from django.shortcuts import render
from diary.models import Student, Course, WeekDay
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request):
    return HttpResponse("Hello!")

def validate_text_value(value) -> Union[None, ValueError]:
    if not value:
        raise ValueError("Empty data is not allowed")
    
    pattern = re.compile("^[a-zA-Z]+$")
    if not pattern.match(value):
        raise ValueError("Wrong value! Allowed only alphabet symbols")

def get_user_from_session(request, students_manager) -> Union[None, Student]:
    student = None
    if request.session.get("user_id", False):
        session_student = request.session.get("user_id")
        print(f"User_id: {session_student}")
        student = students_manager.get(username=session_student)
        print(f"Student: {student}")
    return student

def login(request):
    students = Student.objects
    student = None
    error_message = ''
    created = False
    if request.method =='POST':
        try:
            student_name = request.POST["student_name"]
            student_language = request.POST["student_lang"]
            validate_text_value(student_name)
            validate_text_value(student_language)

            print(f"Name: {student_name} Language: {student_language}")
            student, created = students.get_or_create(username=student_name)
            request.session["user_id"] = student.username
            if student_language != student.language:
                print(f"Changing student language from {student.language} to {student_language}")
                student.language = student_language
                student.save()
            print(f"Student: {student}")
        except (KeyError, ValueError):
            print("Invalid data")
            error_message = "Please enter valid data"

        if created:
            print("New user was created")
            error_message = "You were not registered in our system. But now you are ;)"

    return render(
        request,
        "login.html",
        {
            "student": student,
            "error_message": error_message
        },
    )

def select_course(request):
    courses = Course.objects
    selected_course = None
    error_message = None

    student = get_user_from_session(request, Student.objects)
    

    if request.method =='POST' and student and not student.course:
        try:
            print(f"Course from the form: {request.POST['course']}")
            selected_course = courses.get(pk=request.POST["course"])
            print(f"Selected course: {selected_course}")
            student.course = selected_course
            print(f"Student: {student}")
            student.save()
        except (KeyError, Course.DoesNotExist):
            error_message =  "You haven't selected any course."
    elif not student:
        error_message =  "You are not registered here."

    return render(
        request,
        "select_course.html",
        {
            "student": student,
            "courses": courses.all(),
            "selected_course": selected_course,
            "error_message": error_message,
        },
    )

def get_grade(request):
    student = None
    error_message = None

    student = get_user_from_session(request, Student.objects)
    
    if student and not student.grade:
        grade = randint(1, 12)
        student.grade = grade
        print(f"Student: {student}")
        student.save()
    elif not student:
        error_message = "You are not registered here!"

    return render(
        request,
        "get_grade.html",
        {
            "student": student,
            "error_message": error_message,
        },
    )

def my_week(request):
    my_week = WeekDay.objects.all()
    return HttpResponse(my_week)
