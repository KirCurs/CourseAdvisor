import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from students.models import StudentProfile, Interest, StudentInterest
from courses.models import Course, CourseTag, Prerequisite
from recommendations.models import Grade, Recommendation


class Command(BaseCommand):
    help = "Generate demo data for the course recommendation system"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old demo data...")

        Recommendation.objects.all().delete()
        Grade.objects.all().delete()
        StudentInterest.objects.all().delete()
        StudentProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        Prerequisite.objects.all().delete()
        CourseTag.objects.all().delete()
        Course.objects.all().delete()
        Interest.objects.all().delete()

        self.stdout.write("Creating interests...")

        interests = [
            ("programming", "IT"),
            ("python", "IT"),
            ("databases", "IT"),
            ("web development", "IT"),
            ("machine learning", "AI"),
            ("data analysis", "Data"),
            ("backend", "IT"),
            ("frontend", "IT"),
            ("cybersecurity", "Security"),
            ("devops", "Infrastructure"),
            ("cloud", "Infrastructure"),
            ("linux", "Infrastructure"),
            ("system design", "Architecture"),
            ("mobile development", "Mobile"),
            ("algorithms", "Computer Science"),
        ]

        interest_objects = {}

        for name, category in interests:
            interest = Interest.objects.create(
                name=name,
                category=category
            )
            interest_objects[name] = interest

        self.stdout.write("Creating courses...")

        course_data = [
            {
                "title": "Python: основы программирования",
                "description": "Открытый учебный курс по синтаксису Python, функциям, коллекциям и ООП.",
                "difficulty": "easy",
                "semester": 1,
                "credits": 4,
                "teacher_name": "METANIT",
                "provider": "METANIT",
                "source_url": "https://metanit.com/python/tutorial/",
                "direction": "backend",
                "tags": ["programming", "python", "backend"],
            },
            {
                "title": "SQL и реляционные базы данных",
                "description": "Материалы по SQL, выборке данных, фильтрации, группировке и проектированию БД.",
                "difficulty": "medium",
                "semester": 2,
                "credits": 4,
                "teacher_name": "METANIT",
                "provider": "METANIT",
                "source_url": "https://metanit.com/sql/",
                "direction": "databases",
                "tags": ["databases", "backend", "data analysis"],
            },
            {
                "title": "Frontend Roadmap",
                "description": "Дорожная карта изучения HTML, CSS, JavaScript, фреймворков и инструментов frontend-разработчика.",
                "difficulty": "medium",
                "semester": 2,
                "credits": 4,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/frontend",
                "direction": "frontend",
                "tags": ["frontend", "web development", "programming"],
            },
            {
                "title": "Backend Roadmap",
                "description": "Дорожная карта backend-разработчика: интернет, языки, базы данных, API, безопасность и масштабирование.",
                "difficulty": "medium",
                "semester": 3,
                "credits": 4,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/backend",
                "direction": "backend",
                "tags": ["backend", "databases", "system design"],
            },
            {
                "title": "JavaScript и веб-программирование",
                "description": "Открытые материалы по JavaScript, DOM, событиям и разработке интерактивных страниц.",
                "difficulty": "medium",
                "semester": 2,
                "credits": 4,
                "teacher_name": "METANIT",
                "provider": "METANIT",
                "source_url": "https://metanit.com/web/javascript/",
                "direction": "frontend",
                "tags": ["frontend", "web development", "programming"],
            },
            {
                "title": "Data Analyst Roadmap",
                "description": "Дорожная карта аналитика данных: SQL, таблицы, статистика, визуализация и BI-инструменты.",
                "difficulty": "medium",
                "semester": 3,
                "credits": 4,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/data-analyst",
                "direction": "data",
                "tags": ["data analysis", "databases", "python"],
            },
            {
                "title": "Machine Learning Roadmap",
                "description": "Дорожная карта по машинному обучению: математика, Python, модели, оценка качества и MLOps.",
                "difficulty": "hard",
                "semester": 4,
                "credits": 5,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/machine-learning",
                "direction": "machine_learning",
                "tags": ["machine learning", "data analysis", "python"],
            },
            {
                "title": "DevOps Roadmap",
                "description": "Дорожная карта DevOps: Linux, сети, контейнеризация, CI/CD, облака и мониторинг.",
                "difficulty": "hard",
                "semester": 4,
                "credits": 5,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/devops",
                "direction": "devops",
                "tags": ["devops", "cloud", "linux"],
            },
            {
                "title": "Cyber Security Roadmap",
                "description": "Дорожная карта по кибербезопасности: сети, Linux, веб-уязвимости, защита и анализ рисков.",
                "difficulty": "hard",
                "semester": 4,
                "credits": 5,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/cyber-security",
                "direction": "cybersecurity",
                "tags": ["cybersecurity", "linux", "web development"],
            },
            {
                "title": "Алгоритмы и структуры данных",
                "description": "Дорожная карта по базовым структурам данных, алгоритмам и оценке сложности.",
                "difficulty": "hard",
                "semester": 2,
                "credits": 5,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/datastructures-and-algorithms",
                "direction": "backend",
                "tags": ["algorithms", "programming"],
            },
            {
                "title": "Full Stack Roadmap",
                "description": "Дорожная карта полного цикла веб-разработки: frontend, backend, базы данных и деплой.",
                "difficulty": "hard",
                "semester": 4,
                "credits": 5,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/full-stack",
                "direction": "fullstack",
                "tags": ["frontend", "backend", "web development", "databases"],
            },
            {
                "title": "Django Roadmap",
                "description": "План изучения Django для разработки серверной части и веб-приложений на Python.",
                "difficulty": "medium",
                "semester": 3,
                "credits": 4,
                "teacher_name": "roadmap.sh",
                "provider": "roadmap.sh",
                "source_url": "https://roadmap.sh/django",
                "direction": "backend",
                "tags": ["backend", "python", "web development"],
            },
            {
                "title": "Stepik: Поколение Python для начинающих",
                "description": "Бесплатный практический курс по основам Python с теорией и большим набором задач с автоматической проверкой.",
                "difficulty": "easy",
                "semester": 1,
                "credits": 4,
                "teacher_name": "Stepik",
                "provider": "Stepik",
                "source_url": "https://stepik.org/course/58852",
                "direction": "backend",
                "tags": ["programming", "python", "algorithms"],
            },
            {
                "title": "Stepik: интерактивный тренажер по SQL",
                "description": "Практический курс по SQL-запросам и работе с реляционными базами данных.",
                "difficulty": "medium",
                "semester": 2,
                "credits": 4,
                "teacher_name": "Stepik",
                "provider": "Stepik",
                "source_url": "https://stepik.org/course/63054",
                "direction": "databases",
                "tags": ["databases", "data analysis", "backend"],
            },
            {
                "title": "freeCodeCamp: Responsive Web Design",
                "description": "Бесплатная практическая программа по HTML, CSS, адаптивной верстке и базовым frontend-проектам.",
                "difficulty": "easy",
                "semester": 1,
                "credits": 4,
                "teacher_name": "freeCodeCamp",
                "provider": "freeCodeCamp",
                "source_url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
                "direction": "frontend",
                "tags": ["frontend", "web development"],
            },
            {
                "title": "freeCodeCamp: JavaScript Algorithms and Data Structures",
                "description": "Бесплатный трек по JavaScript, базовым алгоритмам, структурам данных и практическим задачам.",
                "difficulty": "medium",
                "semester": 2,
                "credits": 4,
                "teacher_name": "freeCodeCamp",
                "provider": "freeCodeCamp",
                "source_url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/",
                "direction": "frontend",
                "tags": ["frontend", "programming", "algorithms"],
            },
            {
                "title": "freeCodeCamp: Relational Database",
                "description": "Практический бесплатный трек по Linux-командам, Bash, SQL, PostgreSQL и работе с реляционными БД.",
                "difficulty": "medium",
                "semester": 3,
                "credits": 4,
                "teacher_name": "freeCodeCamp",
                "provider": "freeCodeCamp",
                "source_url": "https://www.freecodecamp.org/learn/relational-database/",
                "direction": "databases",
                "tags": ["databases", "linux", "backend"],
            },
            {
                "title": "CodeBasics: основы Python",
                "description": "Бесплатный интерактивный курс для старта в программировании на Python.",
                "difficulty": "easy",
                "semester": 1,
                "credits": 3,
                "teacher_name": "CodeBasics",
                "provider": "CodeBasics",
                "source_url": "https://code-basics.com/languages/python",
                "direction": "backend",
                "tags": ["programming", "python"],
            },
            {
                "title": "CodeBasics: основы JavaScript",
                "description": "Бесплатный интерактивный курс по базовому JavaScript для начинающих frontend-разработчиков.",
                "difficulty": "easy",
                "semester": 1,
                "credits": 3,
                "teacher_name": "CodeBasics",
                "provider": "CodeBasics",
                "source_url": "https://code-basics.com/languages/javascript",
                "direction": "frontend",
                "tags": ["frontend", "programming", "web development"],
            },
            {
                "title": "Hexlet: бесплатные курсы по программированию",
                "description": "Подборка бесплатных вводных курсов по frontend, backend, Python, JavaScript, SQL, DevOps и другим IT-направлениям.",
                "difficulty": "easy",
                "semester": 1,
                "credits": 3,
                "teacher_name": "Hexlet",
                "provider": "Hexlet",
                "source_url": "https://ru.hexlet.io/courses/free",
                "direction": "fullstack",
                "tags": ["frontend", "backend", "programming", "devops"],
            },
        ]

        course_objects = {}

        for item in course_data:
            course = Course.objects.create(
                title=item["title"],
                description=item["description"],
                difficulty=item["difficulty"],
                semester=item["semester"],
                credits=item["credits"],
                teacher_name=item["teacher_name"],
                provider=item["provider"],
                source_url=item["source_url"],
                direction=item["direction"],
                is_active=True,
            )

            for tag in item["tags"]:
                CourseTag.objects.create(
                    course=course,
                    tag_name=tag
                )

            course_objects[item["title"]] = course

        Prerequisite.objects.create(
            course=course_objects["Machine Learning Roadmap"],
            required_course=course_objects["Python: основы программирования"]
        )

        Prerequisite.objects.create(
            course=course_objects["Backend Roadmap"],
            required_course=course_objects["SQL и реляционные базы данных"]
        )

        Prerequisite.objects.create(
            course=course_objects["DevOps Roadmap"],
            required_course=course_objects["Backend Roadmap"]
        )

        Prerequisite.objects.create(
            course=course_objects["freeCodeCamp: JavaScript Algorithms and Data Structures"],
            required_course=course_objects["freeCodeCamp: Responsive Web Design"]
        )

        Prerequisite.objects.create(
            course=course_objects["Stepik: интерактивный тренажер по SQL"],
            required_course=course_objects["Stepik: Поколение Python для начинающих"]
        )

        self.stdout.write("Creating students...")

        first_names = [
            "Иван", "Алексей", "Дмитрий", "Анна", "Мария",
            "Елена", "Кирилл", "Артем", "София", "Никита",
        ]

        last_names = [
            "Петров", "Смирнов", "Иванов", "Кузнецов", "Соколов",
            "Морозов", "Волков", "Федоров", "Орлов", "Алексеев",
        ]

        groups = ["ИС-221", "ИС-222", "ПИ-221", "ПИ-222"]

        all_courses = list(course_objects.values())
        all_interests = list(interest_objects.values())

        for index in range(30):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"

            username = f"student{index + 1}"

            user = User.objects.create_user(
                username=username,
                password="12345"
            )

            average_score = random.randint(55, 100)

            student = StudentProfile.objects.create(
                user=user,
                full_name=full_name,
                group_name=random.choice(groups),
                semester=random.randint(1, 5),
                gpa=average_score,
                career_goal=random.choice([
                    "Backend-разработчик",
                    "Frontend-разработчик",
                    "Data Analyst",
                    "ML Engineer",
                    "DevOps Engineer",
                    "Специалист по кибербезопасности",
                ])
            )

            selected_interests = random.sample(all_interests, 3)

            for interest in selected_interests:
                StudentInterest.objects.create(
                    student=student,
                    interest=interest,
                    weight=round(random.uniform(0.5, 1.0), 2)
                )

            passed_courses = random.sample(
                all_courses,
                random.randint(2, 5)
            )

            for course in passed_courses:
                Grade.objects.create(
                    student=student,
                    course=course,
                    value=random.randint(60, 100),
                    semester=random.randint(1, 5)
                )

        self.stdout.write(
            self.style.SUCCESS("Demo data successfully created!")
        )
