from tempfile import template
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('customer/<str:pk>/',views.customerpage,name='customer'),
    path('product/',views.productpage,name='product'),
    path('createorder/<str:pk>/',views.createorder,name='createorder'),
    path('updateorder/<str:pk>/',views.updateorder,name='updateorder'),
    path('deleteorder/<str:pk>/',views.deleteorder,name='deleteorder'),
    path('login/',views.loginpage,name='loginpage'),
    path('logout/',views.logoutuser,name='logout'),
    path('register/',views.register,name='register'),
    path('user/',views.userpage,name='userpage'),
    path('account/',views.accountsettings,name='account'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='app2/password_reset.html'),name='password_reset'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='app2/password_reset_sent.html'),name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app2/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app2/password_reset_done.html'),name='password_reset_complete'),
]