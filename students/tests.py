from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import StudentProfile, StudentTestAttempt


class InterestTestViewTests(TestCase):
    def test_interest_test_updates_existing_student_and_redirects(self):
        user = User.objects.create_user(username="student", password="12345")
        student = StudentProfile.objects.create(
            user=user,
            full_name="Анна Петрова",
            group_name="ПИ-221",
            semester=3,
            gpa=88,
        )

        self.client.login(username="student", password="12345")

        response = self.client.post(
            reverse("interest_test"),
            {
                "student": student.id,
                "desired_direction": "backend",
                "experience_level": "practice",
                "preferred_format": "project",
                "motivation": "career",
                "weekly_hours": 8,
                "programming_logic": 5,
                "backend_api": 5,
                "database_design": 5,
                "frontend_ui": 2,
                "web_apps": 4,
                "data_patterns": 3,
                "ml_models": 2,
                "automation": 4,
                "security": 1,
                "architecture": 5,
                "mobile": 2,
                "cloud": 4,
                "skill_python": 4,
                "skill_sql": 5,
                "skill_html_css": 2,
                "skill_javascript": 3,
                "skill_git_linux": 4,
                "skill_math_stats": 3,
            },
        )

        student.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("student_recommendations", kwargs={"student_id": student.id}),
            fetch_redirect_response=False,
        )
        self.assertEqual(student.gpa, 88)
        self.assertIn("Backend-разработка", student.career_goal)
        self.assertGreaterEqual(student.student_interests.count(), 7)
        self.assertEqual(StudentTestAttempt.objects.filter(student=student).count(), 1)
