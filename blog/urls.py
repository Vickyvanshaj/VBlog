from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('createBlog',views.createBlog,name='createBlog'),
    path('login',views.handleLogin,name='login'),
    path('logout',views.handleLogout,name='logout'),
    path('postComment',views.postComment,name='postComment'),
    path('',views.blogHome,name='blogHome'),
    path('<str:slug>',views.blogPost,name='blogPost'),
    # Api to post a comment

]
