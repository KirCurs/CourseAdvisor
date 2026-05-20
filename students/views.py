from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    DIRECTION_CHOICES,
    DIRECTION_INTERESTS,
    INTEREST_TEST_QUESTIONS,
    SKILL_TEST_QUESTIONS,
    InterestTestForm,
)
from .models import Interest, StudentInterest, StudentProfile, StudentTestAttempt


EXPERIENCE_BONUS = {
    "start": 0.85,
    "basic": 0.95,
    "practice": 1.05,
    "confident": 1.12,
}


def add_interest_score(scores, interest_name, category, value, weight):
    current_score, current_category = scores.get(interest_name, (0, category))
    scores[interest_name] = (max(current_score, value * weight), current_category)


@login_required
def interest_test(request):
    selected_student = None
    allow_student_choice = request.user.is_staff

    if not allow_student_choice:
        try:
            selected_student = request.user.student_profile
        except StudentProfile.DoesNotExist:
            selected_student = None

    if request.method == "POST":
        post_data = request.POST.copy()
        if selected_student is not None:
            post_data["student"] = selected_student.id
        form = InterestTestForm(
            post_data,
            student=selected_student,
            allow_student_choice=allow_student_choice,
        )
        if form.is_valid():
            student = form.cleaned_data["student"]
            desired_direction = form.cleaned_data["desired_direction"]
            direction_labels = dict(DIRECTION_CHOICES)
            experience_level = form.cleaned_data["experience_level"]
            preferred_format = form.cleaned_data["preferred_format"]
            motivation = form.cleaned_data["motivation"]
            weekly_hours = form.cleaned_data["weekly_hours"]
            experience_bonus = EXPERIENCE_BONUS[experience_level]

            student.career_goal = f"{direction_labels[desired_direction]} ({desired_direction})"
            student.save(update_fields=["career_goal"])
            StudentInterest.objects.filter(student=student).delete()

            interest_scores = {}
            interest_values = []
            for question in INTEREST_TEST_QUESTIONS:
                value = int(form.cleaned_data[question["field"]])
                interest_values.append(value)
                if value < 2:
                    continue

                add_interest_score(
                    interest_scores,
                    question["interest"],
                    question["category"],
                    value / 5,
                    0.7,
                )

            skill_values = []
            for question in SKILL_TEST_QUESTIONS:
                value = int(form.cleaned_data[question["field"]])
                skill_values.append(value)
                if value < 2:
                    continue

                add_interest_score(
                    interest_scores,
                    question["interest"],
                    question["category"],
                    value / 5,
                    0.45,
                )

            for interest_name in DIRECTION_INTERESTS[desired_direction]:
                add_interest_score(
                    interest_scores,
                    interest_name,
                    direction_labels[desired_direction],
                    1.0,
                    0.35,
                )

            for interest_name, (score, category) in interest_scores.items():
                interest, _ = Interest.objects.get_or_create(
                    name=interest_name,
                    defaults={"category": category},
                )
                StudentInterest.objects.update_or_create(
                    student=student,
                    interest=interest,
                    defaults={"weight": round(min(score * experience_bonus, 1.0), 2)},
                )

            StudentTestAttempt.objects.create(
                student=student,
                desired_direction=desired_direction,
                experience_level=experience_level,
                preferred_format=preferred_format,
                motivation=motivation,
                weekly_hours=weekly_hours,
                interest_score=round(sum(interest_values) / len(interest_values), 2),
                skill_score=round(sum(skill_values) / len(skill_values), 2),
            )

            return redirect("student_recommendations", student_id=student.id)
    else:
        form = InterestTestForm(
            student=selected_student,
            allow_student_choice=allow_student_choice,
        )

    students = StudentProfile.objects.order_by("full_name", "group_name")
    student_scores = {str(student.id): student.gpa for student in students}

    return render(
        request,
        "students/interest_test.html",
        {
            "form": form,
            "student_scores": student_scores,
            "student_count": students.count(),
            "selected_student": selected_student,
            "allow_student_choice": allow_student_choice,
            "direction_choices": DIRECTION_CHOICES,
            "profile_fields": [
                form["student"],
                form["desired_direction"],
                form["experience_level"],
                form["preferred_format"],
                form["motivation"],
                form["weekly_hours"],
            ],
            "interest_fields": [
                form[question["field"]] for question in INTEREST_TEST_QUESTIONS
            ],
            "skill_fields": [form[question["field"]] for question in SKILL_TEST_QUESTIONS],
        },
    )
