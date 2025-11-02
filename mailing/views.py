from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ClientForm, MailingForm, MessageForm
from .models import Client, Mailing, MailingAttempt, Message
from .tasks import send_mailing


class OwnerRequiredMixin:
    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return super().get_queryset()
        return super().get_queryset().filter(owner=self.request.user)


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Менеджеры").exists()


class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = "home_stats"
        stats = cache.get(cache_key)

        if not stats:
            if self.request.user.is_authenticated:
                if self.request.user.groups.filter(name="Менеджеры").exists():
                    total_mailings = Mailing.objects.count()
                    active_mailings = Mailing.objects.filter(
                        status="started",
                        start_time__lte=timezone.now(),
                        end_time__gte=timezone.now(),
                    ).count()
                    unique_clients = Client.objects.distinct().count()
                else:
                    total_mailings = Mailing.objects.filter(
                        owner=self.request.user
                    ).count()
                    active_mailings = Mailing.objects.filter(
                        owner=self.request.user,
                        status="started",
                        start_time__lte=timezone.now(),
                        end_time__gte=timezone.now(),
                    ).count()
                    unique_clients = (
                        Client.objects.filter(owner=self.request.user)
                        .distinct()
                        .count()
                    )
            else:
                total_mailings = 0
                active_mailings = 0
                unique_clients = 0

            stats = {
                "total_mailings": total_mailings,
                "active_mailings": active_mailings,
                "unique_clients": unique_clients,
            }
            cache.set(cache_key, stats, 300)

        context.update(stats)
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailing/client_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")


class ClientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")


# Аналогичные представления для Message и Mailing...
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailing/attempt_list.html"

    def get_queryset(self):
        queryset = MailingAttempt.objects.select_related("mailing", "client")
        if not self.request.user.groups.filter(name="Менеджеры").exists():
            queryset = queryset.filter(mailing__owner=self.request.user)
        return queryset


class SendMailingView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = "mailing/send_mailing.html"

    def test_func(self):
        mailing = self.get_object()
        return (
            mailing.owner == self.request.user
            or self.request.user.groups.filter(name="Менеджеры").exists()
        )

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        send_mailing.delay(mailing.id)
        return render(
            request,
            self.template_name,
            {"object": mailing, "message": "Рассылка запущена"},
        )
