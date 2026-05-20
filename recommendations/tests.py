from django.contrib.auth.models import User
from django.test import TestCase

from courses.models import Course, CourseTag
from students.models import Interest, StudentInterest, StudentProfile

from .services import calculate_interest_match, generate_recommendations


class RecommendationServiceTests(TestCase):
    def test_recommendations_use_student_interest_weights(self):
        user = User.objects.create_user(username="student")
        student = StudentProfile.objects.create(
            user=user,
            full_name="Иван Иванов",
            group_name="ИС-221",
            semester=2,
            gpa=84,
        )
        interest = Interest.objects.create(name="programming", category="IT")
        StudentInterest.objects.create(student=student, interest=interest, weight=1.0)

        course = Course.objects.create(
            title="Основы программирования",
            description="Python и базовые алгоритмы",
            difficulty="easy",
            semester=1,
            credits=3,
            teacher_name="Иванов И.И.",
        )
        CourseTag.objects.create(course=course, tag_name="programming")

        self.assertEqual(calculate_interest_match(student, course), 1)

        recommendations = generate_recommendations(student)

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["course"], course)
        self.assertGreater(recommendations[0]["predicted_success"], 0)
