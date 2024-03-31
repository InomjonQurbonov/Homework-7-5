from django.urls import path

from .views import (AddNewsView, NewsListView,
                    RegistrationView, UpdateNewsView, DeleteNewsView,
                    NewsDetailView, IndexView, CategoriesView
                    )


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('', CategoriesView.as_view(), name='categories'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('list_news/', NewsListView.as_view(), name='list_news'),
    path('add/', AddNewsView.as_view(), name='add_news'),
    path('about_news/<int:pk>/', NewsDetailView.as_view(), name='about_news'),
    path('update/<int:pk>/', UpdateNewsView.as_view(), name='edit_news'),
    path('delete/<int:pk>/', DeleteNewsView.as_view(), name='delete_news'),

]
