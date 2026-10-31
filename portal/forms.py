from django import forms
from .models import User, Subject, Doubt, DoubtResponse

class StudentRegisterForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Pavan Kumar'})
    )
    roll_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 323136410112'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a simple password'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'roll_number', 'password']

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number').strip()
        if User.objects.filter(roll_number__iexact=roll_number).exists():
            raise forms.ValidationError("This Roll Number is already registered.")
        return roll_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['roll_number'].strip()
        user.roll_number = self.cleaned_data['roll_number'].strip()
        user.full_name = self.cleaned_data['full_name'].strip()
        user.role = 'student'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class TeacherRegisterForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dr. Ramesh Rao'})
    )
    roll_number = forms.CharField(
        max_length=50,
        required=True,
        label="Teacher ID / Roll Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. T101 or 323136410001'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=True,
        empty_label="-- Select Your Subject --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a simple password'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'roll_number', 'subject', 'password']

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number').strip()
        if User.objects.filter(roll_number__iexact=roll_number).exists():
            raise forms.ValidationError("This Teacher ID / Roll Number is already registered.")
        return roll_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['roll_number'].strip()
        user.roll_number = self.cleaned_data['roll_number'].strip()
        user.full_name = self.cleaned_data['full_name'].strip()
        user.role = 'teacher'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    roll_number = forms.CharField(
        max_length=50,
        label="Roll Number / Teacher ID",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll Number or Teacher ID'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )


class DoubtForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="-- Select Subject --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your doubt about?'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your doubt in detail...'})
    )

    class Meta:
        model = Doubt
        fields = ['subject', 'title', 'description']


class ResponseForm(forms.ModelForm):
    response_text = forms.CharField(
        label="Teacher's Answer / Clarification",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your explanation or solution here...'})
    )

    class Meta:
        model = DoubtResponse
        fields = ['response_text']
