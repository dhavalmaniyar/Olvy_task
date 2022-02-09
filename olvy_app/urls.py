from django.contrib import admin
from django.urls import path, include
from .views import  UserList, ReviewList, ProductList
urlpatterns = [
    path('users',UserList.as_view()),
    path('review',ReviewList.as_view()),
    # path('products/<str:asin>',ProductView.as_view()),
    path('products',ProductList.as_view()),
]
