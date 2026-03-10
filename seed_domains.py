"""
Run: python seed_domains.py

Seeds the domains table and domain_courses junction table.
Maps existing courses (from courses table) to domains.
Run seed_learn.py first.
"""
from app import create_app
from app.extensions import db
from app.models.domain import Domain, DomainCourse
from app.models.learn import Course

app = create_app()

with app.app_context():
    if Domain.query.count() > 0:
        print('Domains already seeded')
        exit(0)

    # Verify courses exist
    existing_ids = {c.id for c in Course.query.all()}
    print(f'Found {len(existing_ids)} existing courses: {existing_ids}')

    # ── 1. Insert domains ──────────────────────────────────────────────────────
    domains = [
        Domain(
            id='data-science',
            title='Data Science',
            description='Master data analysis, visualisation, and machine learning fundamentals for data-first roles.',
            icon='Database',
            icon_color='text-blue-400',
            bg_color='bg-blue-400/20',
            skills=['Python', 'SQL', 'Statistics', 'ML Basics'],
            is_active=True,
            order=1,
        ),
        Domain(
            id='data-analysis',
            title='Data Analysis',
            description='Learn to collect, clean, analyse, and visualise data to extract actionable business insights.',
            icon='BarChart2',
            icon_color='text-emerald-400',
            bg_color='bg-emerald-400/20',
            skills=['Python', 'SQL', 'Data Visualisation', 'Statistics'],
            is_active=True,
            order=2,
        ),
        Domain(
            id='machine-learning',
            title='Machine Learning',
            description='Learn supervised, unsupervised, and deep learning — from maths fundamentals to production.',
            icon='Brain',
            icon_color='text-purple-400',
            bg_color='bg-purple-400/20',
            skills=['Python', 'Scikit-learn', 'TensorFlow', 'Deep Learning'],
            is_active=True,
            order=2,
        ),
        Domain(
            id='web-development',
            title='Web Development',
            description='Build modern full-stack web applications from HTML/CSS to Node.js APIs.',
            icon='Globe',
            icon_color='text-cyan-400',
            bg_color='bg-cyan-400/20',
            skills=['HTML', 'CSS', 'JavaScript', 'Node.js'],
            is_active=True,
            order=3,
        ),
        Domain(
            id='placement-prep',
            title='Placement Preparation',
            description='Ace placement tests with quantitative aptitude, verbal ability, and core programming skills.',
            icon='Star',
            icon_color='text-amber-400',
            bg_color='bg-amber-400/20',
            skills=['Quantitative', 'Verbal', 'Python', 'SQL'],
            is_active=True,
            order=4,
        ),
    ]

    for d in domains:
        db.session.add(d)
    db.session.flush()

    # ── 2. Map existing courses → domains ─────────────────────────────────────
    # Only reference course IDs that exist in the courses table
    raw_mappings = [
        # Data Science: uses python, sql, data-science
        ('data-science', 'python',       1),
        ('data-science', 'sql',          2),
        ('data-science', 'data-science', 3),

        # Data Analysis: uses python, sql, quantitative
        ('data-analysis', 'python',       1),
        ('data-analysis', 'sql',          2),
        ('data-analysis', 'quantitative', 3),

        # Machine Learning: uses python, data-science
        ('machine-learning', 'python',       1),
        ('machine-learning', 'data-science', 2),

        # Web Development: uses html-css, javascript, nodejs
        ('web-development', 'html-css',    1),
        ('web-development', 'javascript',  2),
        ('web-development', 'nodejs',      3),

        # Placement Prep: uses quantitative, verbal, python, sql
        ('placement-prep', 'quantitative', 1),
        ('placement-prep', 'verbal',       2),
        ('placement-prep', 'python',       3),
        ('placement-prep', 'sql',          4),
    ]

    # Filter out any course IDs not in the DB
    mappings = [(d, c, o) for d, c, o in raw_mappings if c in existing_ids]
    skipped = [(d, c, o) for d, c, o in raw_mappings if c not in existing_ids]
    if skipped:
        print(f'Skipped {len(skipped)} mappings (courses not in DB): {[c for _, c, _ in skipped]}')

    for domain_id, course_id, order_index in mappings:
        db.session.add(DomainCourse(
            domain_id=domain_id,
            course_id=course_id,
            order_index=order_index,
        ))

    db.session.commit()
    print(f'Seeded {len(domains)} domains and {len(mappings)} course mappings')
