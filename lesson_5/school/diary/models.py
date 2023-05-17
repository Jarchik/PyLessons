from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, default='')

    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    username = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, default=None, null=True)
    grade = models.IntegerField(default=None, null=True)

    def __str__(self) -> str:
        return f"Student: {self.username}, language: {self.language}, course: {self.course}, grade: {self.grade}"
