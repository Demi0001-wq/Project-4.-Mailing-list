from django.urls import path
from .apps import MailingConfig
from .views import (
    MailingListView, MailingDetailView, MailingCreateView, 
    MailingUpdateView, MailingDeleteView, mailing_send_now, toggle_mailing_status,
    RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    HomeView, UserListView, toggle_user_status
)

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailings/', MailingListView.as_view(), name='list'),
    path('mailings/view/<int:pk>/', MailingDetailView.as_view(), name='view'),
    path('mailings/create/', MailingCreateView.as_view(), name='create'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='edit'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('mailings/send/<int:pk>/', mailing_send_now, name='send_now'),
    path('mailings/toggle/<int:pk>/', toggle_mailing_status, name='toggle_status'),
    
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/toggle/<int:pk>/', toggle_user_status, name='toggle_user_status'),
    
    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
    
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
