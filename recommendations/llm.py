from django.conf import settings


def is_llm_enabled():
    return bool(settings.OPENAI_API_KEY and settings.ENABLE_LLM_EXPLANATIONS)


def build_llm_prompt(student, course, score, predicted_success, local_explanation):
    return f"""
Ты помощник рекомендательной системы учебных курсов.
Сформируй короткое объяснение на русском языке: почему студенту подходит курс.
Не обещай трудоустройство и не придумывай факты, которых нет во входных данных.
Ответ должен быть 1-2 предложения.

Студент:
- ФИО: {student.full_name}
- Группа: {student.group_name}
- Семестр: {student.semester}
- Средний балл: {student.gpa}/100
- Желаемое направление: {student.career_goal}

Курс:
- Название: {course.title}
- Источник: {course.provider}
- Направление: {course.direction}
- Сложность: {course.get_difficulty_display()}
- Описание: {course.description}

Расчет системы:
- Рейтинг: {score}
- Вероятность успешного прохождения: {predicted_success}%
- Локальное объяснение: {local_explanation}
""".strip()


def generate_llm_explanation(student, course, score, predicted_success, local_explanation):
    if not is_llm_enabled():
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=build_llm_prompt(
                student,
                course,
                score,
                predicted_success,
                local_explanation,
            ),
            max_output_tokens=180,
        )
    except Exception:
        return None

    explanation = getattr(response, "output_text", "").strip()
    return explanation or None
