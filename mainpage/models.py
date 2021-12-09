from typing import Text
from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User


class Topic(models.Model):
    text = CharField(max_length=200)
    date_added = DateTimeField(auto_now_add=True)
    owner = ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic_id = ForeignKey(Topic, on_delete=models.CASCADE)
    text = TextField()
    date_added = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:50]} ...'

    class Meta:
        verbose_name_plural = 'entries'
