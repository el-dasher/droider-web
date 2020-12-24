from django.urls import path

from . import views


urlpatterns = [
    path("invite", views.invite, name="index"),
    path('rank-br', views.board, name='rank-br'),
    path('user/<int:user_id>', views.user_page, name='userpage'),
    path("calc", views.calculate, name="calculate")
]
