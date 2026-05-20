from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from students.models import StudentProfile

from .services import generate_recommendations


@login_required
def recommendation_list(request, student_id=None):
    if student_id is None:
        if hasattr(request.user, "student_profile"):
            return redirect("student_recommendations", student_id=request.user.student_profile.id)
        return redirect("interest_test")
    else:
        student = get_object_or_404(StudentProfile, id=student_id)

    if not request.user.is_staff and student.user_id != request.user.id:
        return HttpResponseForbidden("Вы можете просматривать только свои рекомендации.")

    if student is None:
        return render(
            request,
            "recommendations/list.html",
            {
                "student": None,
                "recommendations": [],
            },
        )

    recommendations = generate_recommendations(student)

    return render(
        request,
        "recommendations/list.html",
        {
            "student": student,
            "recommendations": recommendations,
        },
    )
