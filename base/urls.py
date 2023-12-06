from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path('select-boks/', views.postRegister, name='postRegister'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('book/<str:pk>/', views.book, name='book'),
    path('myBooks/<str:pk>/', views.user_home, name='user_home'),
    path('recommended/', views.recommended, name='recommended'),
    path('wishlist/<str:pk>/', views.wishlist, name='wishlist'),
    path('rating/<str:pk>/<int:rating>/', views.rating, name='rating'),
]