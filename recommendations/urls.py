from django.urls import path

from .views import recommendation_list

urlpatterns = [
    path("", recommendation_list, name="recommendation_list"),
    path("<int:student_id>/", recommendation_list, name="student_recommendations"),
]
