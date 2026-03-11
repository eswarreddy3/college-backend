# Fynity — Database Schema

> **Database**: MySQL
> **ORM**: Flask-SQLAlchemy
> **Migrations**: Alembic (Flask-Migrate)
> **Migration head**: `f6a7b8c9d0e1`

---

## Table of Contents

1. [Entity Overview](#entity-overview)
2. [Schema Diagram (relationships)](#schema-diagram)
3. [Table Definitions](#table-definitions)
   - [packages](#packages)
   - [colleges](#colleges)
   - [users](#users)
   - [refresh_tokens](#refresh_tokens)
   - [activity_logs](#activity_logs)
   - [courses](#courses)
   - [lessons](#lessons)
   - [user_lesson_progress](#user_lesson_progress)
   - [domains](#domains)
   - [domain_courses](#domain_courses)
   - [posts](#posts)
   - [post_likes](#post_likes)
   - [comments](#comments)
   - [comment_likes](#comment_likes)
   - [mcq_questions](#mcq_questions)
   - [mcq_attempts](#mcq_attempts)
   - [assignment_questions](#assignment_questions)
   - [assignment_attempts](#assignment_attempts)
   - [coding_problems](#coding_problems)
   - [coding_submissions](#coding_submissions)
   - [companies](#companies)
   - [company_hiring_rounds](#company_hiring_rounds)
   - [company_packages](#company_packages)
   - [company_aptitude_questions](#company_aptitude_questions)
   - [company_coding_questions](#company_coding_questions)
   - [company_tips](#company_tips)

---

## Entity Overview

| Group | Tables |
|-------|--------|
| **Auth & Users** | `packages`, `colleges`, `users`, `refresh_tokens` |
| **Learning** | `courses`, `lessons`, `user_lesson_progress` |
| **Domain Programs** | `domains`, `domain_courses` |
| **Social Feed** | `posts`, `post_likes`, `comments`, `comment_likes` |
| **MCQ Practice** | `mcq_questions`, `mcq_attempts` |
| **Assignments** | `assignment_questions`, `assignment_attempts` |
| **Coding** | `coding_problems`, `coding_submissions` |
| **Company Prep** | `companies`, `company_hiring_rounds`, `company_packages`, `company_aptitude_questions`, `company_coding_questions`, `company_tips` |
| **Audit** | `activity_logs` |

---

## Schema Diagram

```
packages ──< colleges ──< users >─── activity_logs
                                │
                                ├──< refresh_tokens
                                │
                                ├──< user_lesson_progress >── lessons >── courses
                                │                                             │
                                │                                    domain_courses >── domains
                                │
                                ├──< posts (college_id) >── post_likes
                                │         │
                                │         └──< comments >── comment_likes
                                │                 └── (parent_id self-FK for replies)
                                │
                                ├──< mcq_attempts >── mcq_questions
                                │
                                ├──< assignment_attempts
                                │
                                └──< coding_submissions >── coding_problems

companies ──< company_hiring_rounds
          ──< company_packages
          ──< company_aptitude_questions
          ──< company_coding_questions
          ──< company_tips
```

---

## Table Definitions

---

### `packages`
Subscription plans assigned to colleges.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `name` | VARCHAR(100) | NOT NULL | Plan name (e.g. "Basic", "Pro") |
| `plan_type` | VARCHAR(50) | NULLABLE | `free` / `base` / `pro` / `enterprise` |
| `price` | DECIMAL(10,2) | DEFAULT 0 | Price in INR |
| `features` | JSON | | List of feature strings |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | | |

---

### `colleges`
Colleges registered on the platform.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `name` | VARCHAR(255) | NOT NULL | College name |
| `location` | VARCHAR(255) | | City / state |
| `package_id` | INT | FK → `packages.id` | Subscribed plan |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `activation_token` | VARCHAR(255) | UNIQUE | Token for college activation email |
| `activated_at` | DATETIME | NULLABLE | When college was activated |
| `allowed_domain_ids` | JSON | NULLABLE | `NULL` = all domains accessible; `[]` = all locked; `["id1","id2"]` = only those unlocked |
| `allowed_course_ids` | JSON | NULLABLE | `NULL` = all courses accessible; `[]` = all locked; `["id1","id2"]` = only those unlocked |
| `created_at` | DATETIME | | |

---

### `users`
All platform users — students, college admins, super admins.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `name` | VARCHAR(255) | NOT NULL | Full name |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt hash |
| `role` | ENUM | NOT NULL | `student` / `college_admin` / `super_admin` |
| `college_id` | INT | FK → `colleges.id`, NULLABLE | NULL for super_admin |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `first_login` | BOOLEAN | DEFAULT TRUE | Triggers onboarding flow |
| `branch` | VARCHAR(100) | NULLABLE | e.g. "CSE", "ECE" |
| `section` | VARCHAR(50) | NULLABLE | e.g. "A", "B" |
| `roll_number` | VARCHAR(50) | NULLABLE | |
| `passout_year` | INT | NULLABLE | Graduation year |
| `phone` | VARCHAR(20) | NULLABLE | |
| `linkedin` | VARCHAR(255) | NULLABLE | LinkedIn profile URL |
| `points` | INT | DEFAULT 0 | Gamification points |
| `streak` | INT | DEFAULT 0 | Consecutive active days |
| `last_active` | DATETIME | NULLABLE | Last activity timestamp |
| `email_notifications` | BOOLEAN | DEFAULT TRUE | |
| `assignment_reminders` | BOOLEAN | DEFAULT TRUE | |
| `leaderboard_updates` | BOOLEAN | DEFAULT FALSE | |
| `created_at` | DATETIME | | |

---

### `refresh_tokens`
JWT refresh tokens for session management.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `token` | VARCHAR(512) | UNIQUE, NOT NULL | |
| `expires_at` | DATETIME | NOT NULL | |
| `created_at` | DATETIME | | |

---

### `activity_logs`
Audit trail of user actions (lesson completions, submissions, etc.).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `action` | VARCHAR(255) | NOT NULL | Human-readable description |
| `details` | JSON | NULLABLE | Extra context `{description, points, ...}` |
| `created_at` | DATETIME | | |

---

### `courses`
Courses in the learning library. `category` distinguishes type.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | VARCHAR(50) | PK | Slug-style (e.g. `"python"`, `"sql"`) |
| `title` | VARCHAR(100) | NOT NULL | |
| `description` | TEXT | | |
| `category` | VARCHAR(50) | NOT NULL | `programming` / `aptitude` / `domain` |
| `difficulty` | VARCHAR(20) | DEFAULT `"Beginner"` | `Beginner` / `Intermediate` / `Advanced` |
| `icon` | VARCHAR(50) | DEFAULT `"Code"` | Lucide icon name |
| `icon_color` | VARCHAR(50) | | Tailwind text-* class |
| `prerequisite_id` | VARCHAR(50) | FK → `courses.id`, NULLABLE | Self-referential prerequisite |
| `points_per_lesson` | INT | DEFAULT 10 | Points awarded per lesson completion |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `order` | INT | DEFAULT 0 | Display order |

---

### `lessons`
Individual lessons within a course.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `course_id` | VARCHAR(50) | FK → `courses.id`, NOT NULL | |
| `title` | VARCHAR(200) | NOT NULL | |
| `duration_mins` | INT | DEFAULT 10 | Estimated duration |
| `order` | INT | NOT NULL | Position within course |
| `points` | INT | DEFAULT 10 | Points on completion |
| `is_active` | BOOLEAN | DEFAULT TRUE | |

---

### `user_lesson_progress`
Tracks which lessons each student has completed.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `lesson_id` | INT | FK → `lessons.id`, NOT NULL | |
| `points_earned` | INT | DEFAULT 0 | |
| `completed_at` | DATETIME | | |

**Unique constraint**: `(user_id, lesson_id)` — idempotent completion.

---

### `domains`
Specialized learning tracks (Data Science, ML, Web Dev, etc.).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | VARCHAR(50) | PK | Slug (e.g. `"data-science"`) |
| `title` | VARCHAR(100) | NOT NULL | |
| `description` | TEXT | | |
| `icon` | VARCHAR(50) | | Lucide icon name |
| `icon_color` | VARCHAR(50) | | Tailwind text-* class |
| `bg_color` | VARCHAR(50) | | Tailwind bg-* class for icon container |
| `skills` | JSON | | `["Python", "SQL", ...]` |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `order` | INT | DEFAULT 0 | Display order |

---

### `domain_courses`
Junction table mapping courses to domains with ordering.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `domain_id` | VARCHAR(50) | FK → `domains.id`, NOT NULL | |
| `course_id` | VARCHAR(50) | FK → `courses.id`, NOT NULL | References existing courses |
| `order_index` | INT | DEFAULT 0 | Position within domain roadmap |

**Unique constraint**: `(domain_id, course_id)` — one course per domain.

---

### `posts`
College-scoped social feed posts and blogs.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | Author |
| `college_id` | INT | FK → `colleges.id`, NOT NULL | College scope (users only see their college's posts) |
| `type` | ENUM | NOT NULL | `post` / `blog` |
| `title` | VARCHAR(255) | NULLABLE | Blogs only |
| `cover_image_url` | VARCHAR(512) | NULLABLE | Blogs only |
| `reading_time` | INT | DEFAULT 0 | Auto-calculated for blogs (words ÷ 200) |
| `is_published` | BOOLEAN | DEFAULT TRUE | `FALSE` = draft (blogs only) |
| `content` | TEXT | NOT NULL | Markdown / plain text |
| `tags` | JSON | | `["placement", "event", ...]` |
| `created_at` | DATETIME | | |
| `updated_at` | DATETIME | | Auto-updated on edit |

---

### `post_likes`
Likes on posts (one per user per post).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `post_id` | INT | FK → `posts.id`, NOT NULL | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `created_at` | DATETIME | | |

**Unique constraint**: `(post_id, user_id)` — toggle like/unlike.

---

### `comments`
Comments on posts, with support for one level of nested replies.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `post_id` | INT | FK → `posts.id`, NOT NULL | |
| `user_id` | INT | FK → `users.id`, NOT NULL | Author |
| `parent_id` | INT | FK → `comments.id`, NULLABLE | Self-FK — NULL = top-level, set = reply |
| `content` | TEXT | NOT NULL | |
| `created_at` | DATETIME | | |

---

### `comment_likes`
Likes on comments (one per user per comment).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `comment_id` | INT | FK → `comments.id`, NOT NULL | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `created_at` | DATETIME | | |

**Unique constraint**: `(comment_id, user_id)`.

---

### `mcq_questions`
MCQ question bank for practice.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `topic` | VARCHAR(100) | NOT NULL | e.g. `"Python"`, `"SQL"` |
| `subtopic` | VARCHAR(100) | NOT NULL | e.g. `"Data Types"`, `"JOINs"` |
| `question` | TEXT | NOT NULL | |
| `options` | JSON | NOT NULL | Array of 4 strings `["A","B","C","D"]` |
| `correct_answer` | INT | NOT NULL | 0-indexed position in `options` |
| `explanation` | TEXT | NULLABLE | Shown after attempt |
| `difficulty` | ENUM | DEFAULT `"Medium"` | `Easy` / `Medium` / `Hard` |
| `points` | INT | DEFAULT 10 | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | | |

---

### `mcq_attempts`
Records each MCQ answer by a student.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `question_id` | INT | FK → `mcq_questions.id`, NOT NULL | |
| `selected_answer` | INT | NOT NULL | 0-indexed choice |
| `is_correct` | BOOLEAN | NOT NULL | |
| `points_earned` | INT | DEFAULT 0 | |
| `attempted_at` | DATETIME | | |

---

### `assignment_questions`
MCQ questions grouped by module for timed assignments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `module_id` | VARCHAR(100) | NOT NULL, INDEX | e.g. `"python-basics"` groups questions |
| `topic` | VARCHAR(100) | NOT NULL | |
| `subtopic` | VARCHAR(100) | NOT NULL | |
| `question` | TEXT | NOT NULL | |
| `options` | JSON | NOT NULL | Array of 4 strings |
| `correct_answer` | INT | NOT NULL | 0-indexed |
| `explanation` | TEXT | NULLABLE | |
| `difficulty` | ENUM | DEFAULT `"Medium"` | `Easy` / `Medium` / `Hard` |
| `points` | INT | DEFAULT 5 | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | | |

---

### `assignment_attempts`
Records a student's full assignment submission per module.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `module_id` | VARCHAR(100) | NOT NULL, INDEX | Matches `assignment_questions.module_id` |
| `score` | INT | DEFAULT 0 | Total points earned |
| `total_questions` | INT | DEFAULT 0 | |
| `correct_count` | INT | DEFAULT 0 | |
| `answers` | JSON | NULLABLE | `{"question_id": selected_index, ...}` |
| `completed_at` | DATETIME | | |

---

### `coding_problems`
Coding challenges shown in the IDE page.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `title` | VARCHAR(255) | NOT NULL | |
| `slug` | VARCHAR(255) | UNIQUE, NOT NULL | URL-friendly identifier |
| `description` | TEXT | NOT NULL | Markdown problem statement |
| `difficulty` | ENUM | DEFAULT `"Easy"` | `Easy` / `Medium` / `Hard` |
| `tags` | JSON | | `["arrays", "dp", ...]` |
| `examples` | JSON | | `[{input, output, explanation}, ...]` |
| `constraints` | TEXT | NULLABLE | |
| `starter_code` | JSON | | `{"python": "...", "java": "..."}` |
| `test_cases` | JSON | | `[{input, expected_output}, ...]` — not exposed to client |
| `points` | INT | DEFAULT 10 | Awarded on first `accepted` submission |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | | |

---

### `coding_submissions`
Each code run/submit by a student.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `user_id` | INT | FK → `users.id`, NOT NULL | |
| `problem_id` | INT | FK → `coding_problems.id`, NOT NULL | |
| `language` | VARCHAR(50) | NOT NULL | e.g. `"python"`, `"java"` |
| `code` | TEXT | NOT NULL | |
| `status` | ENUM | | `accepted` / `wrong_answer` / `runtime_error` / `time_limit` |
| `runtime_ms` | INT | NULLABLE | Execution time |
| `submitted_at` | DATETIME | | |

---

### `companies`
Companies in the Company Prep section.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | |
| `slug` | VARCHAR(100) | UNIQUE, NOT NULL | URL identifier |
| `description` | TEXT | NULLABLE | |
| `about_points` | JSON | | Bullet-point facts list |
| `industry` | VARCHAR(100) | NULLABLE | e.g. `"Technology"` |
| `founded_year` | INT | NULLABLE | |
| `headquarters` | VARCHAR(200) | NULLABLE | |
| `employee_count` | VARCHAR(50) | NULLABLE | e.g. `"600,000+"` |
| `website` | VARCHAR(255) | NULLABLE | |
| `logo_color` | VARCHAR(100) | | Tailwind gradient class |
| `logo_letter` | VARCHAR(5) | | Single letter for logo avatar |
| `is_active` | BOOLEAN | DEFAULT TRUE | |
| `created_at` | DATETIME | | |

---

### `company_hiring_rounds`
Ordered hiring process stages for a company.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `company_id` | INT | FK → `companies.id`, NOT NULL | |
| `order` | INT | NOT NULL | Round sequence (1, 2, 3 ...) |
| `name` | VARCHAR(100) | NOT NULL | e.g. `"Online Test"`, `"Technical Interview"` |
| `description` | TEXT | NULLABLE | |
| `duration` | VARCHAR(50) | NULLABLE | e.g. `"60 minutes"` |
| `is_eliminatory` | BOOLEAN | DEFAULT TRUE | |

---

### `company_packages`
Salary packages offered by a company per role.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `company_id` | INT | FK → `companies.id`, NOT NULL | |
| `role_name` | VARCHAR(150) | NOT NULL | e.g. `"Software Engineer"` |
| `type` | ENUM | DEFAULT `"Full Time"` | `Full Time` / `Internship` |
| `ctc_min` | DECIMAL(6,2) | NULLABLE | Minimum CTC in LPA |
| `ctc_max` | DECIMAL(6,2) | NULLABLE | Maximum CTC in LPA |
| `location` | VARCHAR(200) | NULLABLE | |
| `eligibility` | VARCHAR(255) | NULLABLE | e.g. `"CSE/IT, CGPA ≥ 7.0"` |

---

### `company_aptitude_questions`
Past aptitude questions from company placement tests.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `company_id` | INT | FK → `companies.id`, NOT NULL | |
| `section` | ENUM | NOT NULL | `Quantitative` / `Logical` / `Verbal` / `Technical` |
| `question` | TEXT | NOT NULL | |
| `options` | JSON | NOT NULL | Array of 4 strings |
| `correct_answer` | INT | NOT NULL | 0-indexed |
| `explanation` | TEXT | NULLABLE | |
| `difficulty` | ENUM | DEFAULT `"Medium"` | `Easy` / `Medium` / `Hard` |
| `year` | INT | NULLABLE | Year of appearance |
| `is_active` | BOOLEAN | DEFAULT TRUE | |

---

### `company_coding_questions`
Past coding questions from company placement tests.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `company_id` | INT | FK → `companies.id`, NOT NULL | |
| `title` | VARCHAR(255) | NOT NULL | |
| `description` | TEXT | NOT NULL | Problem statement |
| `difficulty` | ENUM | DEFAULT `"Medium"` | `Easy` / `Medium` / `Hard` |
| `tags` | JSON | | `["arrays", "strings", ...]` |
| `solution_hint` | TEXT | NULLABLE | Approach hint (not full solution) |
| `year` | INT | NULLABLE | |
| `is_active` | BOOLEAN | DEFAULT TRUE | |

---

### `company_tips`
Interview and preparation tips per company.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | |
| `company_id` | INT | FK → `companies.id`, NOT NULL | |
| `category` | ENUM | NOT NULL | `HR` / `Technical` / `GD` / `Resume` |
| `title` | VARCHAR(255) | NOT NULL | |
| `content` | TEXT | NOT NULL | |
| `order` | INT | DEFAULT 0 | Display order within category |

---

## Migration History

| Revision | Description |
|----------|-------------|
| `f056a9865754` | Initial — colleges, users, packages, coding_problems, refresh_tokens |
| `8ccad5e073f0` | Add MCQ tables |
| `7cf3584e9d27` | Add company prep tables |
| `a1b2c3d4e5f6` | Add domain tables |
| `b2c3d4e5f6a7` | Add feed tables |
| `c3d4e5f6a7b8` | Add `plan_type` to packages |
| `e5f6a7b8c9d0` | Add `allowed_domain_ids` to colleges |
| `f6a7b8c9d0e1` | Add `allowed_course_ids` to colleges ← **current head** |

---

## Key Design Decisions

- **College scoping** — `posts.college_id` ensures social feed is always isolated per college. All feed queries filter by `g.current_user.college_id`.
- **Course prerequisites** — `courses.prerequisite_id` is a self-FK. A course is locked if its prerequisite is not fully completed by the user.
- **Domain ↔ Course mapping** — `domain_courses` is a pure junction table. Domains do not own courses; existing courses are reused across multiple domains.
- **Comment threading** — `comments.parent_id` self-FK supports one level of nested replies. Top-level comments have `parent_id = NULL`.
- **Idempotent likes** — `UNIQUE(post_id, user_id)` and `UNIQUE(comment_id, user_id)` constraints prevent duplicate likes; the API toggles on conflict.
- **Idempotent lesson completion** — `UNIQUE(user_id, lesson_id)` on `user_lesson_progress` prevents duplicate point awards.
- **Slug PKs for courses** — `courses.id` is a human-readable slug (`"python"`, `"sql"`) for readability in API routes and foreign keys.
- **College access control** — `colleges.allowed_domain_ids` and `colleges.allowed_course_ids` are JSON arrays. `NULL` = unrestricted (backward-compatible), `[]` = everything locked, `["id1","id2"]` = only listed items accessible. Plan-locked content returns `lock_reason: "plan"` in API responses; prerequisite-locked returns `lock_reason: "prerequisite"`.
