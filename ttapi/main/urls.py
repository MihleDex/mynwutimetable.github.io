from .views import home, signup, login, logout_view, profile_view
from django.urls import path
urlpatterns = [
    path('', home),
    path('home', home),
    path('signup', signup),
    path('login', login),
    path('logout', logout_view),
    path('profile', profile_view),
]
