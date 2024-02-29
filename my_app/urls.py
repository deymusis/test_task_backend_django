from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:product_id>/lessons/', views.LessonListByProduct.as_view(), name='lesson-list-by-product'),
]
