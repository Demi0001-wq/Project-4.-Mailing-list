from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Mailing, Recipient, Message
from .forms import MailingForm, RecipientForm, MessageForm
from .services import send_mailing
from users.models import User

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        if self.request.user.is_manager or self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return obj.owner == user or user.is_manager or user.is_staff

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        return self.get_object().owner == self.request.user

class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        return self.get_object().owner == self.request.user


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_queryset(self):
        if self.request.user.is_manager or self.request.user.is_staff:
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:recipient_list')

    def test_func(self):
        return self.get_object().owner == self.request.user


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')

    def test_func(self):
        return self.get_object().owner == self.request.user


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        return self.get_object().owner == self.request.user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        return self.get_object().owner == self.request.user


@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        return context


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'mailing/user_list.html'

    def test_func(self):
        return self.request.user.is_manager or self.request.user.is_staff

def mailing_send_now(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.owner == request.user or request.user.is_staff:
        send_mailing(mailing)
        messages.success(request, 'Рассылка успешно отправлена вручную.')
    else:
        messages.error(request, 'У вас нет прав для отправки этой рассылки.')
    return redirect('mailing:view', pk=pk)

def toggle_user_status(request, pk):
    user_to_toggle = get_object_or_404(User, pk=pk)
    if request.user.is_manager or request.user.is_staff:
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        messages.success(request, f'Статус пользователя {user_to_toggle.email} изменен.')
    return redirect('mailing:user_list')

def toggle_mailing_status(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.user.is_manager or request.user.is_staff:
        if mailing.status == 'completed':
            messages.error(request, 'Нельзя изменить статус завершенной рассылки.')
        else:
            mailing.status = 'completed' if mailing.status != 'completed' else 'started'
            mailing.save()
            messages.success(request, f'Статус рассылки изменен.')
    return redirect('mailing:list')
