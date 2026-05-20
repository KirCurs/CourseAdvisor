from courses.models import Course

from .llm import generate_llm_explanation
from .models import Recommendation


def get_student_interests(student):
    return {
        item.interest.name.lower(): item.weight
        for item in student.student_interests.select_related("interest")
    }


def get_course_tags(course):
    return [t.tag_name.lower() for t in course.tags.all()]


def calculate_interest_match(student, course):
    student_interests = get_student_interests(student)
    course_tags = set(get_course_tags(course))

    if not course_tags:
        return 0

    common = course_tags.intersection(student_interests)
    weighted_match = sum(student_interests[tag] for tag in common)

    return min(weighted_match / len(course_tags), 1)


def calculate_difficulty_score(course):
    if course.difficulty == "easy":
        return 1.0

    elif course.difficulty == "medium":
        return 0.8

    return 0.5


def predict_success(student, course):
    gpa_factor = student.gpa / 100

    if course.difficulty == "easy":
        difficulty_factor = 1.0

    elif course.difficulty == "medium":
        difficulty_factor = 0.8

    else:
        difficulty_factor = 0.6

    prediction = gpa_factor * difficulty_factor

    return round(prediction * 100, 1)


def build_explanation(student, course, interest_score):
    reasons = []

    if interest_score > 0.5:
        reasons.append("курс соответствует вашим интересам")

    if student.gpa >= 85:
        reasons.append("у вас высокий средний балл")
    elif student.gpa < 60:
        reasons.append("курс может потребовать дополнительной подготовки")

    if course.direction and course.direction.lower() in student.career_goal.lower():
        reasons.append("курс относится к выбранному направлению")

    if course.difficulty == "easy":
        reasons.append("курс подходит для базового уровня")

    elif course.difficulty == "medium":
        reasons.append("курс соответствует вашему текущему уровню")

    else:
        reasons.append("курс повышенной сложности")

    return ", ".join(reasons)


def calculate_score(student, course):
    interest_score = calculate_interest_match(student, course)

    difficulty_score = calculate_difficulty_score(course)

    total_score = 0.7 * interest_score + 0.3 * difficulty_score

    return round(total_score, 2)


def generate_recommendations(student):
    courses = Course.objects.filter(is_active=True).prefetch_related("tags")

    Recommendation.objects.filter(student=student).delete()

    results = []

    for course in courses:
        interest_score = calculate_interest_match(student, course)
        score = calculate_score(student, course)
        prediction = predict_success(student, course)

        explanation = build_explanation(student, course, interest_score)

        recommendation = Recommendation.objects.create(
            student=student,
            course=course,
            score=score,
            predicted_success=prediction,
            explanation=explanation,
        )

        results.append(
            {
                "course": course,
                "score": score,
                "predicted_success": prediction,
                "explanation": explanation,
                "recommendation": recommendation,
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)

    for item in results[:5]:
        llm_explanation = generate_llm_explanation(
            student,
            item["course"],
            item["score"],
            item["predicted_success"],
            item["explanation"],
        )
        if llm_explanation:
            item["explanation"] = llm_explanation
            item["recommendation"].explanation = llm_explanation
            item["recommendation"].save(update_fields=["explanation"])

    return results
