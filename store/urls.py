from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('service/', views.service_list, name='service_list'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('search_result/', views.search_result, name='search_result'),
    path('profile/', views.profile, name='profile'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('create-product/', views.create_product, name='create_product'),
]