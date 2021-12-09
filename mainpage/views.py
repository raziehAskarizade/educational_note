from django.http.response import Http404
from django.shortcuts import redirect, render
from .models import Topic
from .forms import *
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'mainpage/homepage.html')


@login_required(login_url='accounts:login')
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'mainpage/topics.html', context)


@login_required(login_url='accounts:login')
def entries(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # important
    if topic.owner != request.user:
        raise Http404
    # important
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'mainpage/entries.html', context)

# از لحاظ مهندسی چون ابتدا کلیک روی اضافه کردن تاپیک ، م
# چون هنوز می خواهیم فورم باز شود بهتر است ابتدا پست نبودن را چک کنیم


@login_required(login_url='accounts:login')
def new_topic(request):
    if request.method == 'POST':
        form = Topicform(data=request.POST)
        if form.is_valid:
            # important
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # important
            return redirect('mainpage:topics')
    else:
        form = Topicform()
    context = {'form': form}
    return render(request, 'mainpage/new_topic.html', context)

# def new_entry(request, topic_id):
#     topic = Topic.objects.get(id=topic_id)
#     if request.method != 'POST':
#         form = EntryForm()
#     else:
#         form = EntryForm(data=request.POST)
#         if form.is_valid:
#             form.save()
#             return redirect('mainpage:entries')
#     context = {'form': form, 'topic': topic}
#     return render(request, 'mainpage/new_entry.html', context)

# this is more engeening becouse it check only in this page not on templates page
# and it is better for develope


@login_required(login_url='accounts:login')
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid:
            new_entry = form.save(commit=False)
            new_entry.topic_id = topic
            new_entry.save()
            # important
            return redirect('mainpage:entries', topic_id=topic_id)
    context = {'form': form, 'topic': topic}
    return render(request, 'mainpage/new_entry.html', context)


@login_required(login_url='accounts:login')
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic_id
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('mainpage:entries', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'mainpage/edit_entry.html', context)


@login_required(login_url='accounts:login')
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = Topicform(instance=topic)
    else:
        form = Topicform(instance=topic, data=request.POST)
        if form.is_valid():
            edit_entry = form.save(commit=False)
            edit_entry.owner = request.user
            edit_entry.save()
            return redirect('mainpage:entries', topic_id=topic.id)
    context = {'form': form, 'topic': topic}
    return render(request, 'mainpage/edit_topic.html', context)
