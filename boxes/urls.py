from django.urls import path
from .views import recommend_box_view

urlpatterns = [
    path('recommend-box/', recommend_box_view, name='recommend_box'),
]
