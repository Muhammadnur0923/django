from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', category_by, name='category'),
    path('article/<int:pk>/', article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', EditArticle.as_view(), name='edit'),
    # path('article/<int:pk>/delete/', DeleteArticle.as_view(),name='delete'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('profile/', profile, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logaut, name='logaut'),
    path('register/', register, name='register'),
    path('add_comment/<int:pk>/', save_comment, name='add_comment'),
    path('search/', search, name='search'),
    path('carousel/<int:pk>/', CarouselDetail.as_view(), name='carousel_detail'),
    path('carousel/create/', AddCarousel.as_view(), name='carousel_create'),
    path('carousel/update/<int:pk>/', EditCarousel.as_view(), name='carousel_update'),
    path('carousel/delete/<int:pk>/', DeleteCarousel.as_view(), name='carousel_delete'),
]