from django.contrib import admin
from .models import Student, Course, WeekDay
# Register your models here.

class WeekDayAdmin(admin.ModelAdmin):
    list_display = ('title', 'note')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'language', 'course', 'grade')


admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(WeekDay, WeekDayAdmin)