from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    full_name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=100)
    semester = models.PositiveIntegerField(default=1)
    gpa = models.FloatField(default=0.0)
    career_goal = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class StudentInterest(models.Model):
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="student_interests"
    )
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.student.full_name} - {self.interest.name}"


class StudentTestAttempt(models.Model):
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="test_attempts"
    )
    desired_direction = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=50)
    preferred_format = models.CharField(max_length=50)
    motivation = models.CharField(max_length=50)
    weekly_hours = models.PositiveIntegerField()
    interest_score = models.FloatField(default=0.0)
    skill_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.desired_direction}"
