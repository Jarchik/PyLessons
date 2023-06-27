from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView

from .models import WeekDay, Note
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .forms import NoteForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class RegisterCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration.html'
    success_url = '/login'


class LoginView(AuthLoginView):
    template_name = "login.html"


def index(request):
    session = request.session
    print(f"{session.get('key')}")
    session[123] = {'all': 'empty'}

    return redirect('my_week')


# def login(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...
def logout_view(request):
    logout(request)


@login_required
def my_week(request) -> HttpResponse:
    print(f"{request.user.is_authenticated}")

    template = loader.get_template("week.html")
    context = {
        "days": WeekDay.objects.all()
    }

    return HttpResponse(template.render(context, request))


@login_required
def my_day(request, week_day_id: int) -> HttpResponse:
    print(f"{request.session.get('123')}")
    request.session["key"] = 123671327819

    day = get_object_or_404(WeekDay, pk=week_day_id)

    return render(request, "weekday.html", {"week_day": day})


@login_required
def my_note(request, note_id: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=note_id)

    return render(request, "note.html", {"weekday": note.week_day, "note": note})


@login_required
def add_note(request, week_day_id) -> HttpResponse:
    week_day = get_object_or_404(WeekDay, pk=week_day_id)
    form_data = NoteForm(request.POST)
    if form_data.is_valid():
        Note.objects.create(
            week_day=week_day,
            title=form_data.cleaned_data['title'],
            msg=form_data.cleaned_data['msg']
        )
    return render(request, "weekday.html", {"week_day": week_day, "error_message": form_data.errors})


def logout(request):
    auth_logout(request)
    return redirect('index')
