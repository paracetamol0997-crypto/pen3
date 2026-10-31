from django.db import models
from django.contrib.auth.models import AbstractUser

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    # roll_number will be unique identifier used for login
    roll_number = models.CharField(max_length=50, unique=True, verbose_name="Roll Number / Teacher ID")
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    # For teachers: the subject they handle
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')

    def __str__(self):
        return f"{self.full_name} ({self.roll_number}) - {self.get_role_display()}"

class Doubt(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Response'),
        ('answered', 'Answered'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='doubts')
    title = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.subject.name}] {self.title} ({self.student.full_name})"

class DoubtResponse(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='responses')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Response by {self.teacher.full_name} on Doubt #{self.doubt.id}"
