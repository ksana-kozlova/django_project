from django.urls import path
from . import views


urlpatterns = [
    path("",views.get_blog_list, name="index"),
    path('<int:blog_id>', views.blog, name="blog_by_id")
]