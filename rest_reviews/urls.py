from django.urls import path
from . import views


urlpatterns = [
    path("",views.get_rest_list, name="index"),
    path('<int:rest_id>', views.restaurant, name="rest_by_id"),
    path('login', views.log_in, name="login"),
    path('signup', views.sign_up, name="signup")
]

