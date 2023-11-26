from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', views.auth, name="login"),
    path("logout/", views.signOut, name="logout"),
    path("becomeSeller/",views.becomeSeller, name="becomeSeller")
]