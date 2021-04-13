from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Products/', views.Products, name="Products"),
    path('Customers/<str:pk>/', views.Customers, name='Customers'),
    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    path('userpage/',views.userpage,name='userpage'),
    path('register/',views.registerpage, name='register'),
    path('login/',views.loginpage, name='login'),
    path('logout/',views.logoutpage, name='logout'),
    path('account/',views.accountSettings, name='account'),
]