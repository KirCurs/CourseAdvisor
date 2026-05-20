# CourseAdvisor

**CourseAdvisor** is a diploma project: an intelligent web-based recommendation
system for open online courses.

The system analyzes a student's profile, academic score, target IT direction,
multi-factor test results, and a catalog of free educational resources. Based on
these signals, it generates personalized course recommendations, calculates a
ranking score, and predicts the probability of successful course completion.

## Features

- Student and administrator authentication.
- Personalized interest and skill assessment test.
- Student academic score is loaded from the database.
- Recommendations are based on tags, target direction, difficulty, and student profile.
- Each course receives a ranking score and success prediction.
- Test attempt history is stored in PostgreSQL.
- Catalog of real open and free educational resources.
- Optional LLM integration for generating recommendation explanations.
- Django Admin for managing students, courses, interests, and recommendations.
- Light and dark UI themes with browser-side preference persistence.

## Course Sources

The demo catalog includes open and free educational resources:

| Source | Used For |
| --- | --- |
| METANIT | Python, SQL, JavaScript |
| roadmap.sh | Backend, Frontend, DevOps, Data, ML, and Security roadmaps |
| Stepik | Python and SQL practice courses |
| freeCodeCamp | Web, JavaScript, and Relational Database tracks |
| CodeBasics | Beginner-friendly interactive courses |
| Hexlet | Free introductory programming courses |

## Why This Project Is Non-Trivial

CourseAdvisor is not just a static list of courses. It implements a
recommendation workflow that uses multiple factors:

- student academic performance on a 1-100 scale;
- desired IT direction;
- current experience level;
- preferred learning format;
- motivation;
- available study time per week;
- interest in different task types;
- self-assessed technical skills;
- course difficulty;
- match between student interests and course tags.

Every test attempt is stored in the database, which makes it possible to extend
the system with analytics and student interest tracking over time.

## Tech Stack

| Component | Technology |
| --- | --- |
| Backend | Django 6 |
| Database | PostgreSQL |
| ORM | Django ORM |
| UI | Django Templates, Bootstrap 5, CSS |
| Authentication | Django Authentication |
| Admin Panel | Django Admin |
| LLM Integration | OpenAI SDK, optional |
| Tests | Django TestCase |

## Data Model

Main entities:

- `StudentProfile` - student profile, group, semester, and academic score.
- `Interest` - possible interests and categories.
- `StudentInterest` - relation between a student and an interest with a weight.
- `StudentTestAttempt` - saved result of a completed assessment test.
- `Course` - open course with source, URL, direction, and difficulty.
- `CourseTag` - tags assigned to a course.
- `Prerequisite` - course prerequisites.
- `Grade` - student grades.
- `Recommendation` - calculated recommendation result.

## User Flow

1. A student signs in with a username and password.
2. The system finds the student's profile in the database.
3. The student completes a multi-factor assessment test.
4. The answers are saved as a test attempt.
5. The system recalculates the student's interest profile.
6. The recommendation algorithm compares the profile with the course catalog.
7. The student receives personalized course recommendations.

## Recommendation Algorithm

The algorithm calculates:

- match between student interests and course tags;
- course difficulty score;
- success probability based on academic score;
- final course ranking score;
- recommendation explanation.

If LLM integration is enabled, a language model generates a more natural
explanation for the top 5 recommendations. The ranking score itself remains
local and transparent.

## Quick Start

### 1. Clone the Repository

```bash
git clone <repo-url>
cd diplom
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL Database

```bash
createdb course_recommender_db
```

Default database configuration:

```text
POSTGRES_DB=course_recommender_db
POSTGRES_USER=sh
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

These values can be overridden with environment variables.

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Seed Demo Data

```bash
python manage.py seed_data
```

The command creates:

- 30 demo students;
- an open course catalog;
- interests;
- grades;
- course tags;
- prerequisites.

### 7. Run the Development Server

```bash
python manage.py runserver 127.0.0.1:8000
```

## Main Pages

| URL | Purpose |
| --- | --- |
| `/` | Home page |
| `/login/` | Sign in |
| `/students/test/` | Multi-factor assessment test |
| `/recommendations/` | Recommendations for the current student |
| `/admin/` | Admin panel |

## Demo Accounts

After running `python manage.py seed_data`, demo students are created:

```text
student1 / 12345
student2 / 12345
...
student30 / 12345
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

If an administrator already exists but the password is unknown:

```bash
python manage.py changepassword <username>
```

## LLM Integration

The project works without an API key. In that mode, recommendations and
explanations are generated by the local algorithm.

To enable OpenAI-powered explanations:

```bash
export OPENAI_API_KEY="your_api_key_here"
export ENABLE_LLM_EXPLANATIONS=true
export OPENAI_MODEL="gpt-5.2"
```

After that, the system will use a language model to generate explanations for
the top 5 recommendations.

## Testing

```bash
python manage.py test
```

Tests cover:

- recommendation scoring;
- student assessment flow;
- test attempt persistence;
- redirect to personalized recommendations.

## Diploma Value

The project demonstrates:

- relational database design;
- authentication and role-based access;
- recommendation algorithm implementation;
- diagnostic data persistence;
- integration of external educational resources;
- optional LLM integration;
- user interface development;
- automated testing of core logic.

## Status

The project is a working MVP of a diploma recommendation system. Possible future
improvements:

- student interest history;
- analytics dashboards;
- external course API imports;
- more advanced ranking model;
- student personal dashboard.
