from django.contrib import admin
from .models import WeekDay, Note
# Register your models here.


class WeekDayAdmin(admin.ModelAdmin):
    list_display = ("day",)


class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "msg",)


admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(Note, NoteAdmin)
