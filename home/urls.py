from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('signup',views.signup,name='signup'),
    path('login',views.handleLogin,name='login'),
    path('logout',views.handleLogout,name='logout'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
