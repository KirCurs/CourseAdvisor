from django import forms

from .models import StudentProfile


DIRECTION_CHOICES = [
    ("backend", "Backend-разработка"),
    ("frontend", "Frontend-разработка"),
    ("fullstack", "Full Stack"),
    ("data", "Анализ данных"),
    ("machine_learning", "Machine Learning / AI"),
    ("devops", "DevOps"),
    ("cybersecurity", "Кибербезопасность"),
    ("databases", "Базы данных"),
]

EXPERIENCE_LEVEL_CHOICES = [
    ("start", "Начинаю с нуля"),
    ("basic", "Знаю основы"),
    ("practice", "Есть учебные проекты"),
    ("confident", "Уверенно решаю практические задачи"),
]

STUDY_FORMAT_CHOICES = [
    ("interactive", "Интерактивные задания"),
    ("text", "Текстовые конспекты"),
    ("roadmap", "Дорожная карта"),
    ("project", "Проектное обучение"),
]

MOTIVATION_CHOICES = [
    ("career", "Карьерный переход"),
    ("university", "Усилить учебную программу"),
    ("project", "Сделать свой проект"),
    ("research", "Разобраться глубже"),
]

INTEREST_TEST_QUESTIONS = [
    {
        "field": "programming_logic",
        "label": "Разбирать задачу на шаги и писать алгоритм решения",
        "interest": "programming",
        "category": "Core",
    },
    {
        "field": "backend_api",
        "label": "Проектировать серверную логику, API и обработку данных",
        "interest": "backend",
        "category": "Backend",
    },
    {
        "field": "database_design",
        "label": "Продумывать таблицы, связи, SQL-запросы и структуру хранения",
        "interest": "databases",
        "category": "Data",
    },
    {
        "field": "frontend_ui",
        "label": "Создавать интерфейсы, формы, экраны и пользовательские сценарии",
        "interest": "frontend",
        "category": "Frontend",
    },
    {
        "field": "web_apps",
        "label": "Собирать полноценные веб-приложения от идеи до запуска",
        "interest": "web development",
        "category": "Web",
    },
    {
        "field": "data_patterns",
        "label": "Искать закономерности в данных и строить выводы",
        "interest": "data analysis",
        "category": "Data",
    },
    {
        "field": "ml_models",
        "label": "Обучать модели, сравнивать метрики и работать с AI",
        "interest": "machine learning",
        "category": "AI",
    },
    {
        "field": "automation",
        "label": "Автоматизировать сборку, тестирование и развертывание систем",
        "interest": "devops",
        "category": "Infrastructure",
    },
    {
        "field": "security",
        "label": "Искать уязвимости и защищать информационные системы",
        "interest": "cybersecurity",
        "category": "Security",
    },
    {
        "field": "architecture",
        "label": "Проектировать архитектуру приложения и выбирать технологии",
        "interest": "system design",
        "category": "Architecture",
    },
    {
        "field": "mobile",
        "label": "Разрабатывать приложения под Android или iOS",
        "interest": "mobile development",
        "category": "Mobile",
    },
    {
        "field": "cloud",
        "label": "Работать с Linux, Docker, облаками и инфраструктурой",
        "interest": "cloud",
        "category": "Infrastructure",
    },
]

SKILL_TEST_QUESTIONS = [
    {
        "field": "skill_python",
        "label": "Python: переменные, условия, циклы, функции",
        "interest": "python",
        "category": "Core",
    },
    {
        "field": "skill_sql",
        "label": "SQL: SELECT, JOIN, группировка, проектирование таблиц",
        "interest": "databases",
        "category": "Data",
    },
    {
        "field": "skill_html_css",
        "label": "HTML/CSS: верстка, адаптивность, структура страницы",
        "interest": "frontend",
        "category": "Frontend",
    },
    {
        "field": "skill_javascript",
        "label": "JavaScript: DOM, события, массивы, асинхронность",
        "interest": "web development",
        "category": "Frontend",
    },
    {
        "field": "skill_git_linux",
        "label": "Git и Linux: терминал, ветки, команды, окружение",
        "interest": "linux",
        "category": "Infrastructure",
    },
    {
        "field": "skill_math_stats",
        "label": "Математика и статистика для анализа данных и ML",
        "interest": "data analysis",
        "category": "Data",
    },
]

DIRECTION_INTERESTS = {
    "backend": ["backend", "databases", "programming", "system design", "python"],
    "frontend": ["frontend", "web development", "programming"],
    "fullstack": ["frontend", "backend", "web development", "databases"],
    "data": ["data analysis", "databases", "python"],
    "machine_learning": ["machine learning", "data analysis", "python"],
    "devops": ["devops", "cloud", "backend", "linux"],
    "cybersecurity": ["cybersecurity", "databases", "linux"],
    "databases": ["databases", "backend", "data analysis"],
}


class InterestTestForm(forms.Form):
    student = forms.ModelChoiceField(
        label="Студент",
        queryset=StudentProfile.objects.none(),
        widget=forms.Select(attrs={"class": "form-select", "id": "student-select"}),
    )
    desired_direction = forms.ChoiceField(
        label="Желаемое направление",
        choices=DIRECTION_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    experience_level = forms.ChoiceField(
        label="Текущий уровень",
        choices=EXPERIENCE_LEVEL_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    preferred_format = forms.ChoiceField(
        label="Предпочитаемый формат",
        choices=STUDY_FORMAT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    motivation = forms.ChoiceField(
        label="Главная мотивация",
        choices=MOTIVATION_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    weekly_hours = forms.IntegerField(
        label="Сколько часов в неделю готовы учиться",
        min_value=1,
        max_value=40,
        initial=6,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, student=None, allow_student_choice=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = StudentProfile.objects.order_by(
            "full_name", "group_name"
        )
        if student is not None:
            self.fields["student"].initial = student
        if not allow_student_choice:
            self.fields["student"].widget = forms.HiddenInput()

        interest_choices = [
            (1, "1 - неинтересно"),
            (2, "2 - скорее нет"),
            (3, "3 - нейтрально"),
            (4, "4 - интересно"),
            (5, "5 - очень интересно"),
        ]
        skill_choices = [
            (1, "1 - не знаю"),
            (2, "2 - видел тему"),
            (3, "3 - знаю основы"),
            (4, "4 - решал задачи"),
            (5, "5 - уверен"),
        ]

        for question in INTEREST_TEST_QUESTIONS:
            self.fields[question["field"]] = forms.ChoiceField(
                label=question["label"],
                choices=interest_choices,
                widget=forms.RadioSelect,
                initial=3,
            )

        for question in SKILL_TEST_QUESTIONS:
            self.fields[question["field"]] = forms.ChoiceField(
                label=question["label"],
                choices=skill_choices,
                widget=forms.RadioSelect,
                initial=3,
            )
