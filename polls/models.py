import datetime

from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.utils import timezone
from users.models import User

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, default=None)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return '"' + self.text + '" by ' + self.user.username


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    option = models.ForeignKey(Option, on_delete=CASCADE, default=None)

    def __str__(self):
        return self.user.username + " - " + self.option.text
