from django.db import models


class WeekDay(models.Model):
    day = models.CharField(max_length=20)

    def __str__(self):
        return f"Week day: {self.day}"


class Note(models.Model):
    week_day = models.ForeignKey(WeekDay, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    msg = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"Title: {self.title}, msg: {self.msg}"
