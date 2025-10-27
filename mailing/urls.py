from django.urls import path

from .views import (ClientCreateView, ClientDeleteView, ClientListView,
                    ClientUpdateView, HomeView, MailingAttemptListView,
                    MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingUpdateView, MessageCreateView,
                    MessageDeleteView, MessageListView, MessageUpdateView,
                    SendMailingView)

app_name = "mailing"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # Clients
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    # Messages
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    # Mailings
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("mailings/<int:pk>/send/", SendMailingView.as_view(), name="mailing_send"),
    # Attempts
    path("attempts/", MailingAttemptListView.as_view(), name="attempt_list"),
]
