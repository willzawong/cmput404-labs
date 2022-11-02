from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.SnippetHighlight.as_view(), name='snippet-highlight')
]
