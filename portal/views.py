from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import User, Subject, Doubt, DoubtResponse
from .forms import StudentRegisterForm, TeacherRegisterForm, LoginForm, DoubtForm, ResponseForm

def index(request):
    return render(request, 'portal/index.html')

def student_register(request):
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'student':
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.full_name}! Your student account is created successfully.")
            return redirect('student_dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'portal/student_register.html', {'form': form})

def teacher_register(request):
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'teacher':
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.full_name}! Your teacher account ({user.subject.name}) is created.")
            return redirect('teacher_dashboard')
    else:
        form = TeacherRegisterForm()
    return render(request, 'portal/teacher_register.html', {'form': form})

def student_login(request):
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'student':
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number'].strip()
            password = form.cleaned_data['password']

            # Check if this roll number exists in the database
            user = User.objects.filter(roll_number__iexact=roll_number).first()
            if not user:
                messages.warning(
                    request,
                    mark_safe(f"This ID (<code>{roll_number}</code>) is not registered. Please try with a registered Roll Number or <a href='/student/register/' class='alert-link text-decoration-underline'>click here to register as a Student</a>.")
                )
            elif user.role != 'student':
                messages.info(
                    request,
                    mark_safe(f"This ID is registered as a Teacher. Please <a href='/teacher/login/' class='alert-link text-decoration-underline'>log in via the Teacher Portal</a>.")
                )
            else:
                auth_user = authenticate(request, username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    messages.success(request, f"Welcome back, {auth_user.full_name}!")
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "Incorrect password. Please check your password and try again.")
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form, 'active_role': 'student'})

def teacher_login(request):
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'teacher':
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number'].strip()
            password = form.cleaned_data['password']

            # Check if this teacher ID exists in the database
            user = User.objects.filter(roll_number__iexact=roll_number).first()
            if not user:
                messages.warning(
                    request,
                    mark_safe(f"This ID (<code>{roll_number}</code>) is not registered. Please try with a registered Teacher ID or <a href='/teacher/register/' class='alert-link text-decoration-underline'>click here to register as a Teacher</a>.")
                )
            elif user.role != 'teacher':
                messages.info(
                    request,
                    mark_safe(f"This ID is registered as a Student. Please <a href='/student/login/' class='alert-link text-decoration-underline'>log in via the Student Portal</a>.")
                )
            else:
                auth_user = authenticate(request, username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    messages.success(request, f"Welcome back, {auth_user.full_name} ({auth_user.subject.name if auth_user.subject else 'General'})!")
                    return redirect('teacher_dashboard')
                else:
                    messages.error(request, "Incorrect password. Please check your password and try again.")
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form, 'active_role': 'teacher'})

def user_login(request):
    # Unified entry point - defaults to student login or role requested
    role = request.GET.get('role', 'student')
    if role == 'teacher':
        return redirect('teacher_login')
    return redirect('student_login')

def student_logout(request):
    logout(request)
    messages.info(request, "Student logged out successfully.")
    return redirect('student_login')

def teacher_logout(request):
    logout(request)
    messages.info(request, "Teacher logged out successfully.")
    return redirect('teacher_login')

def student_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        messages.warning(request, "Please log in with your Student Roll Number.")
        return redirect('student_login')
    
    status_filter = request.GET.get('status')
    subject_filter = request.GET.get('subject')

    doubts = Doubt.objects.filter(student=request.user)
    if status_filter in ['pending', 'answered']:
        doubts = doubts.filter(status=status_filter)
    if subject_filter:
        doubts = doubts.filter(subject_id=subject_filter)

    subjects = Subject.objects.all()
    stats = {
        'total': Doubt.objects.filter(student=request.user).count(),
        'pending': Doubt.objects.filter(student=request.user, status='pending').count(),
        'answered': Doubt.objects.filter(student=request.user, status='answered').count(),
    }

    return render(request, 'portal/student_dashboard.html', {
        'doubts': doubts,
        'subjects': subjects,
        'selected_status': status_filter,
        'selected_subject': subject_filter,
        'stats': stats,
        'portal_type': 'student'
    })

def ask_doubt(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        messages.warning(request, "Please log in as a student to post a doubt.")
        return redirect('student_login')
    
    if request.method == 'POST':
        form = DoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.student = request.user
            doubt.save()
            messages.success(request, f"Your doubt under '{doubt.subject.name}' has been posted!")
            return redirect('student_doubt_detail', doubt_id=doubt.id)
    else:
        form = DoubtForm()
    
    return render(request, 'portal/ask_doubt.html', {'form': form, 'portal_type': 'student'})

def student_doubt_detail(request, doubt_id):
    if not request.user.is_authenticated or request.user.role != 'student':
        messages.warning(request, "Please log in as a student to view your doubts.")
        return redirect('student_login')
    
    doubt = get_object_or_404(Doubt, id=doubt_id, student=request.user)
    responses = doubt.responses.select_related('teacher').all()

    return render(request, 'portal/doubt_detail.html', {
        'doubt': doubt,
        'responses': responses,
        'can_respond': False,
        'portal_type': 'student',
    })

def teacher_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'teacher':
        messages.warning(request, "Please log in with your Teacher ID.")
        return redirect('teacher_login')
    
    teacher_subject = request.user.subject
    status_filter = request.GET.get('status')

    if teacher_subject:
        doubts = Doubt.objects.filter(subject=teacher_subject)
    else:
        doubts = Doubt.objects.none()

    if status_filter in ['pending', 'answered']:
        doubts = doubts.filter(status=status_filter)

    stats = {
        'total': Doubt.objects.filter(subject=teacher_subject).count() if teacher_subject else 0,
        'pending': Doubt.objects.filter(subject=teacher_subject, status='pending').count() if teacher_subject else 0,
        'answered': Doubt.objects.filter(subject=teacher_subject, status='answered').count() if teacher_subject else 0,
    }

    return render(request, 'portal/teacher_dashboard.html', {
        'doubts': doubts,
        'teacher_subject': teacher_subject,
        'selected_status': status_filter,
        'stats': stats,
        'portal_type': 'teacher'
    })

def teacher_doubt_detail(request, doubt_id):
    if not request.user.is_authenticated or request.user.role != 'teacher':
        messages.warning(request, "Please log in as a teacher.")
        return redirect('teacher_login')
    
    teacher_subject = request.user.subject
    doubt = get_object_or_404(Doubt, id=doubt_id, subject=teacher_subject)

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            resp = response_form.save(commit=False)
            resp.doubt = doubt
            resp.teacher = request.user
            resp.save()
            doubt.status = 'answered'
            doubt.save()
            messages.success(request, "Your answer has been submitted and shared with the student!")
            return redirect('teacher_doubt_detail', doubt_id=doubt.id)
    else:
        response_form = ResponseForm()

    responses = doubt.responses.select_related('teacher').all()

    return render(request, 'portal/doubt_detail.html', {
        'doubt': doubt,
        'responses': responses,
        'response_form': response_form,
        'can_respond': True,
        'portal_type': 'teacher',
    })
