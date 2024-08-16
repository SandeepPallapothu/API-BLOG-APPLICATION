"""
URL configuration for blog_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegisterView.as_view(),name='auth_register'),
    path('login/', views.LoginView.as_view(),name='auth_login'),
    path('post/', views.BlogList.as_view(),name='post-list-create'),
    path('posts/<int:pk>/', views.BlogUpdate.as_view(),name='post-retrieve-update-delete'),
    path('comment/', views.CommentList.as_view(),name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentRetrieve.as_view(),name='comment-retrieve-update-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
