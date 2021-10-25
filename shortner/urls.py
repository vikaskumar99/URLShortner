from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_request, name="logout"),
    path('dashboard/', views.show_login_user_links, name="dashboard"),
    path('create', views.create, name='create'),
    path('<str:pk>', views.go, name='go'),
]