from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserForm, TaskForm
from .models import Profile, Team, Task




def index(request):
    return render(request, 'index.html')


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user,
                team=form.cleaned_data['team'],
                role=form.cleaned_data['role']
            )
            auth_login(request, user)
            return redirect("index")
    else:
        form = UserForm()
    return render(request, "register.html", {"form": form})


def task_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_team = request.user.profile.team
    tasks = Task.objects.filter(team=user_team)

    status = request.GET.get('status')
    assigned = request.GET.get('assigned')

    if status and status != 'all':
        tasks = tasks.filter(status=status)

    if assigned == 'yes':
        tasks = tasks.filter(assigned_to__isnull=False)
    elif assigned == 'no':
        tasks = tasks.filter(assigned_to__isnull=True)

    context = {
        'tasks': tasks,
        'status': status,
        'assigned': assigned,
        'show_filters': request.GET.get('show_filters'),
    }

    return render(request, 'task_list.html', context)



def take_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)

        if request.user.profile.role != 'worker':
            return redirect('task_list')

        if task.assigned_to is not None:
            return redirect('task_list')

        if task.team != request.user.profile.team:
            return redirect('task_list')

        task.assigned_to = request.user
        task.status = 'in_progress'
        task.save()

    return redirect('task_list')



def change_status(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)

        if task.assigned_to != request.user:
            return redirect('task_list')

        if task.status == 'new':
            task.status = 'in_progress'
        elif task.status == 'in_progress':
            task.status = 'done'

        task.save()

    return redirect('task_list')



def create_task(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.profile.role != 'manager':
        return redirect('task_list')

    if request.method == "POST":
        form = TaskForm(request.POST, team=request.user.profile.team)
        if form.is_valid():
            task = form.save(commit=False)
            task.team = request.user.profile.team
            task.status = 'new'

            if task.assigned_to:
                task.status = 'in_progress'

            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(team=request.user.profile.team)

    return render(request, 'create_task.html', {'form': form})



def edit_task(request, task_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.profile.role != 'manager':
        return redirect('task_list')

    task = Task.objects.get(id=task_id)

    if task.team != request.user.profile.team:
        return redirect('task_list')

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            instance=task,
            team=request.user.profile.team
        )
        if form.is_valid():
            task = form.save(commit=False)

            if task.assigned_to and task.status == 'new':
                task.status = 'in_progress'

            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(
            instance=task,
            team=request.user.profile.team
        )

    return render(request, 'edit_task.html', {'form': form})



def delete_task(request, task_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.profile.role != 'manager':
        return redirect('task_list')

    task = Task.objects.get(id=task_id)

    if task.team != request.user.profile.team:
        return redirect('task_list')

    if task.assigned_to is not None:
        return redirect('task_list')

    task.delete()
    return redirect('task_list')

