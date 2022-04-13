"""MRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import imp
from django.contrib import admin
from django.urls import path,include
from MaterialRecommender import views
from django.conf import settings
from django.conf.urls.static import static
from MaterialRecommender import function
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),


    
    # path('jet/', include('jet.urls', 'jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),



    path('', include('MaterialRecommender.urls')),


    
    path("verify/<str:token>/",views.verify),
    path('signup/',views.signup,name="signup"),
    path('contact/', function.contact, name='contact'),
    path('login/',views.user_login,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('rec/',views.Rec,name="rec"),
    path("logout/",views.user_logout,name="logout"),
    
    # path('password_reset/', auth_views.PasswordResetView.as_view(),name="password_reset"),
    # path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # path('reset/done', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)