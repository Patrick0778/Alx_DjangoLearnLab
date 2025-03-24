from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Profile will be created by the signal, just update the role
            user.profile.role = 'MEMBER'  # Default role for new users
            user.profile.save()
        return user

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            # Redirect based on role
            if user.profile.role == 'ADMIN':
                return redirect('relationship_app:admin_dashboard')
            elif user.profile.role == 'LIBRARIAN':
                return redirect('relationship_app:librarian_dashboard')
            else:
                return redirect('relationship_app:member_dashboard')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'relationship_app/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            # Redirect based on role
            if user.profile.role == 'ADMIN':
                return redirect('relationship_app:admin_dashboard')
            elif user.profile.role == 'LIBRARIAN':
                return redirect('relationship_app:librarian_dashboard')
            else:
                return redirect('relationship_app:member_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return render(request, 'relationship_app/auth/logout.html')