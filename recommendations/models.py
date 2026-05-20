from django.db import models

from courses.models import Course
from students.models import StudentProfile


class Grade(models.Model):
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="grades"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    value = models.FloatField()
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}: {self.value}"


class Recommendation(models.Model):
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="recommendations"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField()
    explanation = models.TextField()
    predicted_success = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} -> {self.course.title}"
