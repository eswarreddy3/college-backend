"""
Seed / upsert the 4 Fynity packages.
Run: .venv/Scripts/python.exe seed_packages.py
"""
from app import create_app
from app.extensions import db
from app.models.package import Package

PACKAGES = [
    {
        "name": "Free",
        "plan_type": "free",
        "price": 0,
        "features": [
            "Python Module (Lessons, MCQ & Assignments)",
            "Aptitude MCQ Bank",
            "Remaining courses & domains visible (locked)",
        ],
    },
    {
        "name": "Base Plan",
        "plan_type": "base",
        "price": 500,
        "features": [
            "Python Module",
            "SQL Module",
            "HTML Module",
            "CSS Module",
            "Aptitude MCQ Bank",
            "Company Preparation",
            "Internal College Social Feed",
            "College Admin Dashboard",
            "Remaining courses & domains visible (locked)",
        ],
    },
    {
        "name": "Pro Plan",
        "plan_type": "pro",
        "price": 1000,
        "features": [
            "Everything in Base Plan",
            "Choose 1 Domain (Data Analysis or Web Development)",
            "Admin: 1-click email to inactive students",
            "Remaining courses & domains visible (locked)",
        ],
    },
    {
        "name": "Enterprise",
        "plan_type": "enterprise",
        "price": 0,
        "features": [
            "Custom domains",
            "Custom courses",
            "Custom analytics",
            "Custom integrations",
        ],
    },
]


def seed():
    app = create_app()
    with app.app_context():
        for data in PACKAGES:
            pkg = Package.query.filter_by(plan_type=data["plan_type"]).first()
            if pkg:
                pkg.name = data["name"]
                pkg.price = data["price"]
                pkg.features = data["features"]
                print(f"  Updated: {data['name']}")
            else:
                pkg = Package(**data)
                db.session.add(pkg)
                print(f"  Created: {data['name']}")

        db.session.commit()
        print("Done — packages seeded.")


if __name__ == "__main__":
    seed()
