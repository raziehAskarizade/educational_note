from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


def signin(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordconfirm']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'registration/signin.html', {'error': 'Username has already been taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], request.POST['email'], request.POST['password'])
                auth.login(request, user)
                return redirect('mainpage:topics')
        else:
            return render(request, 'registration/signin.html', {'error': 'Usernames didn\'t match'})
    return render(request, 'registration/signin.html')

# second way:
# def signin(request):
#     if request.method != 'POST':
#         form = UserCreationForm()
#     else:
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             saveUser = form.save(commit=False)
#             auth.login(request, saveUser)
#             redirect('mainpages:topics')

#     context = {'form': form}
#     return render(request, 'registration/signin.html', context)
