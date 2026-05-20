from django.db import models


class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Легкий"),
        ("medium", "Средний"),
        ("hard", "Сложный"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="medium"
    )
    semester = models.PositiveIntegerField()
    credits = models.PositiveIntegerField(default=3)
    teacher_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(blank=True)
    direction = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CourseTag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tags")
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course.title} - {self.tag_name}"


class Prerequisite(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="prerequisites"
    )
    required_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="required_for"
    )

    def __str__(self):
        return f"{self.required_course.title} -> {self.course.title}"
