from django.urls import path
from . import views


urlpatterns = [
    path("clients/", views.ClientViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "clients/<int:pk>",
        views.ClientViewSet.as_view({"patch": "update", "delete": "destroy"}),
    ),
]
