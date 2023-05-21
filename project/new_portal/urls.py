from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),         # отслеживание главной страницы
    path('about/', views.about, name='about'),  # отслеживание страницы, про нас
]
