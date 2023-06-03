from django.urls import re_path, path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),
    path('categories/', views.show_categories, name='categories'),
    path('create/', views.create_post, name='create_post' ),
    re_path(r'^main/$', views.response, name='main' ),
    path('main', views.response, name='main'),

    path('post/<int:pk>', views.PostDetails.as_view(), name='post_detail'),

    path('profile/<str:name>/<int:pk>', views.profile_view, name='profile_view')
]

