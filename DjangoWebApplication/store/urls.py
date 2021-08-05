from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
urlpatterns = [
    path('', ProductListView.as_view(), name='store-home'),
    path('search/', ProductSearchView.as_view(), name='search'),
    path('product/<pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('review/<pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('review/<pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('review/<pk>/new/', ReviewCreateView.as_view(), name='review-create'),
    path('about/', views.about, name='store-about'),
    path('product/', ProductCreateView.as_view(), name='product-create'),
]
