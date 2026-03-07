"""
Seed the database with initial data.
Run: python seed.py
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.college import College
from app.models.package import Package
from app.models.coding_problem import CodingProblem
from app.utils.helpers import hash_password

app = create_app()

PACKAGES = [
    {
        'name': 'Free',
        'price': 0,
        'features': ['Up to 50 students', 'Basic coding problems', 'MCQ practice', 'Email support'],
    },
    {
        'name': 'Basic',
        'price': 4999,
        'features': ['Up to 200 students', 'All coding problems', 'MCQ + Assignments', 'Analytics dashboard', 'Email support'],
    },
    {
        'name': 'Pro',
        'price': 9999,
        'features': ['Up to 500 students', 'All features', 'Mock interviews', 'Resume builder', 'Priority support', 'Custom branding'],
    },
    {
        'name': 'Enterprise',
        'price': 24999,
        'features': ['Unlimited students', 'All Pro features', 'Dedicated account manager', 'Custom integrations', 'SLA guarantee', 'On-premise option'],
    },
]

CODING_PROBLEMS = [
    {
        'title': 'Two Sum',
        'slug': 'two-sum',
        'description': (
            'Given an array of integers `nums` and an integer `target`, '
            'return *indices of the two numbers such that they add up to target*.\n\n'
            'You may assume that each input would have **exactly one solution**, '
            'and you may not use the same element twice.\n\n'
            'You can return the answer in any order.'
        ),
        'difficulty': 'Easy',
        'tags': ['Array', 'Hash Table'],
        'examples': [
            {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'nums[0] + nums[1] = 9'},
            {'input': 'nums = [3,2,4], target = 6', 'output': '[1,2]'},
        ],
        'constraints': '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9',
        'starter_code': {
            'python': 'def twoSum(nums, target):\n    # Your code here\n    pass\n',
            'java': 'class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your code here\n    }\n}\n',
            'javascript': 'var twoSum = function(nums, target) {\n    // Your code here\n};\n',
        },
    },
    {
        'title': 'Valid Parentheses',
        'slug': 'valid-parentheses',
        'description': (
            'Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, '
            'determine if the input string is valid.\n\n'
            'An input string is valid if:\n'
            '- Open brackets must be closed by the same type of brackets.\n'
            '- Open brackets must be closed in the correct order.\n'
            '- Every close bracket has a corresponding open bracket of the same type.'
        ),
        'difficulty': 'Easy',
        'tags': ['String', 'Stack'],
        'examples': [
            {'input': 's = "()"', 'output': 'true'},
            {'input': 's = "()[]{}"', 'output': 'true'},
            {'input': 's = "(]"', 'output': 'false'},
        ],
        'constraints': '1 <= s.length <= 10^4\ns consists of parentheses only.',
        'starter_code': {
            'python': 'def isValid(s: str) -> bool:\n    # Your code here\n    pass\n',
            'java': 'class Solution {\n    public boolean isValid(String s) {\n        // Your code here\n    }\n}\n',
            'javascript': 'var isValid = function(s) {\n    // Your code here\n};\n',
        },
    },
    {
        'title': 'Reverse Linked List',
        'slug': 'reverse-linked-list',
        'description': (
            'Given the `head` of a singly linked list, reverse the list, '
            'and return *the reversed list*.'
        ),
        'difficulty': 'Easy',
        'tags': ['Linked List', 'Recursion'],
        'examples': [
            {'input': 'head = [1,2,3,4,5]', 'output': '[5,4,3,2,1]'},
            {'input': 'head = [1,2]', 'output': '[2,1]'},
        ],
        'constraints': 'The number of nodes in the list is in the range [0, 5000].',
        'starter_code': {
            'python': 'class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverseList(head):\n    # Your code here\n    pass\n',
        },
    },
    {
        'title': 'Binary Search',
        'slug': 'binary-search',
        'description': (
            'Given an array of integers `nums` which is sorted in ascending order, '
            'and an integer `target`, write a function to search `target` in `nums`.\n\n'
            'If `target` exists, return its index. Otherwise, return `-1`.'
        ),
        'difficulty': 'Easy',
        'tags': ['Array', 'Binary Search'],
        'examples': [
            {'input': 'nums = [-1,0,3,5,9,12], target = 9', 'output': '4'},
            {'input': 'nums = [-1,0,3,5,9,12], target = 2', 'output': '-1'},
        ],
        'constraints': '1 <= nums.length <= 10^4\nnums is sorted in ascending order.',
        'starter_code': {
            'python': 'def search(nums, target):\n    # Your code here\n    pass\n',
        },
    },
    {
        'title': 'Longest Substring Without Repeating Characters',
        'slug': 'longest-substring-without-repeating',
        'description': (
            'Given a string `s`, find the length of the **longest substring** '
            'without repeating characters.'
        ),
        'difficulty': 'Medium',
        'tags': ['Hash Table', 'String', 'Sliding Window'],
        'examples': [
            {'input': 's = "abcabcbb"', 'output': '3', 'explanation': '"abc" has length 3'},
            {'input': 's = "bbbbb"', 'output': '1'},
            {'input': 's = "pwwkew"', 'output': '3'},
        ],
        'constraints': '0 <= s.length <= 5 * 10^4',
        'starter_code': {
            'python': 'def lengthOfLongestSubstring(s: str) -> int:\n    # Your code here\n    pass\n',
        },
    },
    {
        'title': 'Merge Intervals',
        'slug': 'merge-intervals',
        'description': (
            'Given an array of `intervals` where `intervals[i] = [starti, endi]`, '
            'merge all overlapping intervals, and return *an array of the non-overlapping intervals '
            'that cover all the intervals in the input*.'
        ),
        'difficulty': 'Medium',
        'tags': ['Array', 'Sorting'],
        'examples': [
            {'input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]', 'output': '[[1,6],[8,10],[15,18]]'},
            {'input': 'intervals = [[1,4],[4,5]]', 'output': '[[1,5]]'},
        ],
        'constraints': '1 <= intervals.length <= 10^4',
        'starter_code': {
            'python': 'def merge(intervals):\n    # Your code here\n    pass\n',
        },
    },
    {
        'title': 'Trapping Rain Water',
        'slug': 'trapping-rain-water',
        'description': (
            'Given `n` non-negative integers representing an elevation map where the width '
            'of each bar is `1`, compute how much water it can trap after raining.'
        ),
        'difficulty': 'Hard',
        'tags': ['Array', 'Two Pointers', 'Dynamic Programming'],
        'examples': [
            {'input': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]', 'output': '6'},
            {'input': 'height = [4,2,0,3,2,5]', 'output': '9'},
        ],
        'constraints': 'n == height.length\n1 <= n <= 2 * 10^4',
        'starter_code': {
            'python': 'def trap(height):\n    # Your code here\n    pass\n',
        },
    },
]


def seed():
    with app.app_context():
        db.create_all()

        # Packages
        existing_packages = {p.name: p for p in Package.query.all()}
        package_objs = {}
        for pkg_data in PACKAGES:
            if pkg_data['name'] not in existing_packages:
                pkg = Package(**pkg_data)
                db.session.add(pkg)
                db.session.flush()
                package_objs[pkg_data['name']] = pkg
            else:
                package_objs[pkg_data['name']] = existing_packages[pkg_data['name']]

        db.session.commit()
        print(f"Packages: {Package.query.count()} total")

        # Super admin
        if not User.query.filter_by(email='admin@fynity.in').first():
            super_admin = User(
                name='Super Admin',
                email='admin@fynity.in',
                password_hash=hash_password('Admin@1234'),
                role='super_admin',
                is_active=True,
                first_login=False,
            )
            db.session.add(super_admin)
            print("Created super admin: admin@fynity.in / Admin@1234")

        # Test college
        college = College.query.filter_by(name='Demo Engineering College').first()
        if not college:
            college = College(
                name='Demo Engineering College',
                location='Hyderabad, Telangana',
                package_id=package_objs['Pro'].id,
                is_active=True,
            )
            db.session.add(college)
            db.session.flush()
            print(f"Created college: {college.name}")

        # College admin
        if not User.query.filter_by(email='collegeadmin@demo.edu').first():
            college_admin = User(
                name='College Admin',
                email='collegeadmin@demo.edu',
                password_hash=hash_password('Admin@1234'),
                role='college_admin',
                college_id=college.id,
                is_active=True,
                first_login=False,
            )
            db.session.add(college_admin)
            print("Created college admin: collegeadmin@demo.edu / Admin@1234")

        # Test students
        students_data = [
            {'name': 'Rahul Sharma', 'email': 'rahul@demo.edu', 'branch': 'CSE', 'section': 'A', 'roll_number': 'CS21001', 'passout_year': 2025},
            {'name': 'Priya Patel', 'email': 'priya@demo.edu', 'branch': 'ECE', 'section': 'B', 'roll_number': 'EC21002', 'passout_year': 2025},
            {'name': 'Arjun Kumar', 'email': 'arjun@demo.edu', 'branch': 'CSE', 'section': 'A', 'roll_number': 'CS21003', 'passout_year': 2025},
        ]
        for s in students_data:
            if not User.query.filter_by(email=s['email']).first():
                student = User(
                    name=s['name'],
                    email=s['email'],
                    password_hash=hash_password('Student@1234'),
                    role='student',
                    college_id=college.id,
                    branch=s['branch'],
                    section=s['section'],
                    roll_number=s['roll_number'],
                    passout_year=s['passout_year'],
                    is_active=True,
                    first_login=False,
                    points=100,
                    streak=3,
                )
                db.session.add(student)
                print(f"Created student: {s['email']} / Student@1234")

        # Coding problems
        existing_slugs = {p.slug for p in CodingProblem.query.all()}
        for prob_data in CODING_PROBLEMS:
            if prob_data['slug'] not in existing_slugs:
                prob = CodingProblem(**prob_data)
                db.session.add(prob)
                print(f"Added problem: {prob_data['title']}")

        db.session.commit()
        print("\nSeed complete!")
        print("\nTest credentials:")
        print("  Super Admin:    admin@fynity.in          / Admin@1234")
        print("  College Admin:  collegeadmin@demo.edu    / Admin@1234")
        print("  Student:        rahul@demo.edu           / Student@1234")


if __name__ == '__main__':
    seed()
