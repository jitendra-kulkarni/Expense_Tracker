from django.urls import path 
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('budget/', views.update_budget, name='update_budget'),
]