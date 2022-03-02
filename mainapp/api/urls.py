from django.urls import path
from . import views


urlpatterns = [
    path("clients", views.ClientViewSet.as_view({"get": "list", "post": "create"})),
    path("clients/<int:pk>",
        views.ClientViewSet.as_view({"patch": "update", "delete": "destroy"})
    ),
    path("mailings", views.MailingViewSet.as_view({"get": "list", "post": "create"})),
    path("mailings/<int:pk>",
        views.MailingViewSet.as_view(
            {"patch": "update", "delete": "destroy", 'get': 'retrieve'}
            )
    ),
    path('message-statistic', views.StatisticView.as_view()),
]
