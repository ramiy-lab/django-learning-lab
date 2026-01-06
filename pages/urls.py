from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("<int:id>/", views.page_detail, name="detail"),
]
