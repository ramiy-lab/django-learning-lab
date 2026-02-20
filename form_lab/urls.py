from django.urls import path
from .views import simple_article_create

app_name = "form_lab"

urlpatterns = [
    path("simple/", simple_article_create, name="simple_article_create"),
]
