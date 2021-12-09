from django import forms
from .models import Topic, Entry


class Topicform(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('text',)
        labels = {'text': 'Topic name '}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('text',)
        labels = {'text': 'Entry explanation '}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
