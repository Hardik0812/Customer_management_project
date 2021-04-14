from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='reset_password_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html') ,name='password_reset_confirm'),
    path('reset_password_completed/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),
]