from django.urls import path

from . import views


urlpatterns = [
    path('rank-br', views.index, name='index'),
    path('user/<int:user_id>', views.user_page, name='userpage'),
    path("calc", views.calculate, name="calculate")
]
