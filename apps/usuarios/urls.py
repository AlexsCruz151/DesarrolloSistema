from django.urls import path
from .views import LoginView, LogoutView, ListView

app_name = 'usuarios'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('usuarios', ListView.as_view(), name='list') ,
]
