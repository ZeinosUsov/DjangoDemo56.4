from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ApplicationForm, StatusChangeForm
from .models import Application


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Вы зарегистрированы и вошли в систему.')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправление для админа
            if username == 'BraveGuar':
                return redirect('admin_panel')
            return redirect('profile')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


def home_view(request):
    return render(request, 'home.html')


@login_required
def profile_view(request):
    applications = request.user.applications.all().order_by('-created_at')
    return render(request, 'profile.html', {'applications': applications})


@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.status = 'new'
            app.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})


# Админ-панель для BraveGuar
@login_required
def admin_panel_view(request):
    if request.user.username != 'BraveGuar':
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('home')

    applications = Application.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = StatusChangeForm(request.POST)
        if form.is_valid():
            app_id = request.POST.get('app_id')
            new_status = form.cleaned_data['status']
            application = get_object_or_404(Application, id=app_id)
            application.status = new_status
            application.save()
            messages.success(request,
                             f'Статус заявки "{application.title}" изменён на {application.get_status_display()}')
            return redirect('admin_panel')
    else:
        form = StatusChangeForm()

    return render(request, 'admin_panel.html', {'applications': applications, 'form': form})