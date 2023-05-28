from typing import Union
from django.http import HttpResponse
from .models import WeekDay, Note
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .forms import NoteForm

# Create your views here.


def index(request):
    return redirect('my_week')


def my_week(request) -> HttpResponse:
    template = loader.get_template("week.html")
    context = {
        "days": WeekDay.objects.all()
    }

    return HttpResponse(template.render(context, request))


def my_day(request, week_day_id: int) -> HttpResponse:
    day = get_object_or_404(WeekDay, pk=week_day_id)

    return render(request, "weekday.html", {"week_day": day})


def my_note(request, note_id: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=note_id)

    return render(request, "note.html", {"weekday": note.week_day, "note": note})


def add_note(request, week_day_id):
    week_day = get_object_or_404(WeekDay, pk=week_day_id)
    form_data = NoteForm(request.POST)
    if form_data.is_valid():
        Note.objects.create(week_day=week_day, title=form_data.cleaned_data['title'], msg=form_data.cleaned_data['msg'])
    return render(request, "weekday.html", {"week_day": week_day, "error_message": form_data.errors})