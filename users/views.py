from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import CreateView, View, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
import secrets

class UserRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        
        host = self.request.get_host()
        url = f"http://{host}/users/confirm/{token}/"
        
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

class UserConfirmView(View):
    def get(self, request, token):
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = None
        user.save()
        return redirect('users:login')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self):
        return self.request.user

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('email', 'avatar', 'phone', 'country')
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')
