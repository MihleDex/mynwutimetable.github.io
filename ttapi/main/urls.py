from .views import home, signup, login, logout_view, profile_view, date_picked, delete_account
from django.urls import path
urlpatterns = [
    path('', home),
    path('home', home),
    path('signup', signup),
    path('login', login),
    path('logout', logout_view),
    path('profile', profile_view),
    path('date_picked', date_picked),
    path('delete_account', delete_account, name='delete_account'),
]
