from typing import Union
from django.http import HttpResponse
from .models import WeekDay, Note
from django.shortcuts import get_object_or_404, render
from django.template import loader

# Create your views here.


def my_week(request) -> HttpResponse:
    template = loader.get_template("week.html")
    context = {
        "days": WeekDay.objects.all()
    }

    return HttpResponse(template.render(context, request))


def my_day(request, week_day_id: int) -> HttpResponse:
    day = get_object_or_404(WeekDay, pk=week_day_id)
    return render(request, "weekday.html", {"week_day": day})


def my_note(request, day_id: int, note_id: int) -> HttpResponse:
    weekday = get_object_or_404(WeekDay, pk=day_id)
    print(f"weekday: {weekday}")
    note = get_object_or_404(Note, pk=note_id)
    return render(request, "note.html", {"weekday": weekday, "note": note})
