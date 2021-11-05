from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('', views.index, name='index'),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_request, name="logout"),
    path('dashboard/', views.show_login_user_links, name="dashboard"),
    path('create/', views.create, name='create'),
    path('<str:pk>', views.go, name='go'),
]