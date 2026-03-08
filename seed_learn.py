"""Run: python seed_learn.py"""
from app import create_app
from app.extensions import db
from app.models.learn import Course, Lesson

app = create_app()
with app.app_context():
    if Course.query.count() > 0:
        print('Courses already seeded')
        exit(0)

    courses = [
        Course(id='python', title='Python', category='programming', difficulty='Beginner',
               icon='Code', icon_color='text-blue-400', points_per_lesson=10, order=1,
               description='Learn Python from scratch — variables, loops, functions, OOP and more.'),
        Course(id='sql', title='SQL', category='programming', difficulty='Intermediate',
               icon='Database', icon_color='text-cyan-400', points_per_lesson=10, order=2,
               description='Master SQL queries, joins, aggregations and database design.'),
        Course(id='java', title='Java', category='programming', difficulty='Intermediate',
               icon='Braces', icon_color='text-orange-400', points_per_lesson=15, order=3,
               description='Build robust applications with Java — OOP, collections, and more.'),
        Course(id='javascript', title='JavaScript', category='programming', difficulty='Beginner',
               icon='Braces', icon_color='text-yellow-400', points_per_lesson=10, order=4,
               description='Modern JavaScript: ES6+, DOM manipulation, async/await.'),
        Course(id='html-css', title='HTML/CSS', category='programming', difficulty='Beginner',
               icon='Globe', icon_color='text-pink-400', points_per_lesson=10, order=5,
               description='Build beautiful web pages with semantic HTML and modern CSS.'),
        Course(id='nodejs', title='Node.js', category='programming', difficulty='Advanced',
               icon='Server', icon_color='text-green-400', points_per_lesson=20, order=6,
               prerequisite_id='javascript',
               description='Server-side JavaScript with Node.js, Express, and REST APIs.'),
        Course(id='quantitative', title='Quantitative Aptitude', category='aptitude', difficulty='Intermediate',
               icon='Terminal', icon_color='text-purple-400', points_per_lesson=10, order=7,
               description='Master percentages, ratios, time-work, and number series for placement tests.'),
        Course(id='verbal', title='Verbal Ability', category='aptitude', difficulty='Beginner',
               icon='Terminal', icon_color='text-teal-400', points_per_lesson=10, order=8,
               description='Improve grammar, vocabulary, reading comprehension and verbal reasoning.'),
        Course(id='data-science', title='Data Science', category='domain', difficulty='Advanced',
               icon='Database', icon_color='text-violet-400', points_per_lesson=20, order=9,
               description='NumPy, Pandas, data visualization, and intro to machine learning.'),
    ]

    for c in courses:
        db.session.add(c)
    db.session.flush()  # get IDs before adding lessons

    lessons_data = {
        'python': [
            ('Introduction to Python', 'Python is a high-level, interpreted programming language known for its simplicity.\n\n## Why Python?\n- Easy to read and write\n- Huge standard library\n- Used in web, data science, automation, AI\n\n## Your First Program\n```python\nprint("Hello, World!")\n```\n\nRun this in your terminal and you\'ll see the output instantly.', 8),
            ('Variables and Data Types', '## Variables\nVariables store data values.\n```python\nname = "Alice"\nage = 25\nheight = 5.6\nis_student = True\n```\n\n## Built-in Types\n| Type | Example |\n|------|---------|\n| int | `42` |\n| float | `3.14` |\n| str | `"hello"` |\n| bool | `True` |\n| list | `[1,2,3]` |\n| dict | `{"key": "val"}` |', 10),
            ('Strings', '## String Operations\n```python\ns = "Hello, Python!"\nprint(len(s))        # 15\nprint(s.upper())     # HELLO, PYTHON!\nprint(s[0:5])        # Hello\nprint(s.replace("Python", "World"))  # Hello, World!\n```\n\n## f-Strings (Python 3.6+)\n```python\nname = "Alice"\nage = 25\nprint(f"My name is {name} and I am {age} years old.")\n```', 10),
            ('Lists and Tuples', '## Lists\n```python\nfruits = ["apple", "banana", "cherry"]\nfruits.append("mango")   # add item\nfruits.remove("banana")  # remove item\nprint(fruits[0])          # apple\n```\n\n## List Comprehension\n```python\nsquares = [x**2 for x in range(1, 6)]\n# [1, 4, 9, 16, 25]\n```\n\n## Tuples (immutable)\n```python\npoint = (10, 20)\nx, y = point  # unpacking\n```', 12),
            ('Dictionaries and Sets', '## Dictionaries\n```python\nstudent = {"name": "Alice", "age": 20, "grade": "A"}\nprint(student["name"])   # Alice\nstudent["age"] = 21      # update\nstudent["city"] = "NYC"  # add key\n```\n\n## Iterating\n```python\nfor key, value in student.items():\n    print(f"{key}: {value}")\n```\n\n## Sets\n```python\nunique = {1, 2, 3, 2, 1}  # {1, 2, 3}\n```', 12),
            ('Control Flow', '## if / elif / else\n```python\nscore = 75\nif score >= 90:\n    grade = "A"\nelif score >= 75:\n    grade = "B"\nelse:\n    grade = "C"\n```\n\n## Loops\n```python\nfor i in range(5):\n    print(i)\n\nx = 10\nwhile x > 0:\n    x -= 3\n```\n\n## break and continue\n```python\nfor n in range(10):\n    if n == 5:\n        break\n    if n % 2 == 0:\n        continue\n    print(n)  # 1, 3\n```', 12),
            ('Functions', '## Defining Functions\n```python\ndef greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\nprint(greet("Alice"))           # Hello, Alice!\nprint(greet("Bob", "Hi"))       # Hi, Bob!\n```\n\n## *args and **kwargs\n```python\ndef total(*args):\n    return sum(args)\n\nprint(total(1, 2, 3, 4))  # 10\n```\n\n## Lambda\n```python\nsquare = lambda x: x ** 2\nprint(square(5))  # 25\n```', 15),
            ('Modules and Packages', '## Importing\n```python\nimport math\nprint(math.sqrt(16))  # 4.0\n\nfrom datetime import datetime\nnow = datetime.now()\n```\n\n## Creating Your Own Module\nSave `myutils.py`:\n```python\ndef add(a, b):\n    return a + b\n```\n\nImport it:\n```python\nfrom myutils import add\nprint(add(3, 4))  # 7\n```', 10),
            ('File Handling', '## Reading Files\n```python\nwith open("data.txt", "r") as f:\n    content = f.read()\n    # or line by line:\n    for line in f:\n        print(line.strip())\n```\n\n## Writing Files\n```python\nwith open("output.txt", "w") as f:\n    f.write("Hello, file!")\n```\n\n## JSON\n```python\nimport json\ndata = {"name": "Alice", "age": 25}\njson_str = json.dumps(data)\nloaded = json.loads(json_str)\n```', 12),
            ('OOP: Classes and Objects', '## Defining a Class\n```python\nclass Animal:\n    def __init__(self, name, sound):\n        self.name = name\n        self.sound = sound\n\n    def speak(self):\n        return f"{self.name} says {self.sound}"\n\ndog = Animal("Dog", "Woof")\nprint(dog.speak())  # Dog says Woof\n```\n\n## Class vs Instance Variables\n```python\nclass Counter:\n    count = 0  # class variable\n\n    def __init__(self):\n        Counter.count += 1\n```', 15),
            ('OOP: Inheritance', '## Inheritance\n```python\nclass Vehicle:\n    def __init__(self, brand):\n        self.brand = brand\n\n    def info(self):\n        return f"Brand: {self.brand}"\n\nclass Car(Vehicle):\n    def __init__(self, brand, model):\n        super().__init__(brand)\n        self.model = model\n\n    def info(self):\n        return f"{super().info()}, Model: {self.model}"\n\nmy_car = Car("Toyota", "Corolla")\nprint(my_car.info())\n```', 15),
            ('Exception Handling', '## try / except / finally\n```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print("Cannot divide by zero!")\nfinally:\n    print("This always runs")\n```\n\n## Raising Exceptions\n```python\ndef divide(a, b):\n    if b == 0:\n        raise ValueError("Denominator cannot be zero")\n    return a / b\n```\n\n## Custom Exceptions\n```python\nclass AppError(Exception):\n    pass\n```', 12),
        ],
        'sql': [
            ('Introduction to SQL', '## What is SQL?\nSQL (Structured Query Language) is used to manage relational databases.\n\n## Basic SELECT\n```sql\nSELECT * FROM employees;\nSELECT name, salary FROM employees;\n```\n\n## WHERE Clause\n```sql\nSELECT name FROM employees\nWHERE salary > 50000;\n```', 10),
            ('Filtering Data', '## Comparison Operators\n```sql\nWHERE age > 25\nWHERE name = \'Alice\'\nWHERE salary BETWEEN 40000 AND 80000\nWHERE city IN (\'NYC\', \'LA\', \'Chicago\')\nWHERE email IS NOT NULL\n```\n\n## Pattern Matching\n```sql\nWHERE name LIKE \'A%\'   -- starts with A\nWHERE name LIKE \'%son\'  -- ends with son\n```\n\n## AND / OR / NOT\n```sql\nWHERE age > 25 AND department = \'Engineering\'\nWHERE city = \'NYC\' OR city = \'LA\'\n```', 12),
            ('Sorting and Limiting', '## ORDER BY\n```sql\nSELECT name, salary FROM employees\nORDER BY salary DESC;\n\nORDER BY last_name ASC, first_name ASC;\n```\n\n## LIMIT / OFFSET\n```sql\nSELECT * FROM products\nORDER BY price ASC\nLIMIT 10 OFFSET 20;  -- page 3 of 10\n```\n\n## DISTINCT\n```sql\nSELECT DISTINCT department FROM employees;\n```', 10),
            ('Aggregate Functions', '## Common Aggregates\n```sql\nSELECT COUNT(*) FROM employees;\nSELECT AVG(salary) FROM employees;\nSELECT MAX(salary), MIN(salary) FROM employees;\nSELECT SUM(sales) FROM orders;\n```\n\n## GROUP BY\n```sql\nSELECT department, AVG(salary) AS avg_salary\nFROM employees\nGROUP BY department;\n```\n\n## HAVING\n```sql\nSELECT department, COUNT(*) AS headcount\nFROM employees\nGROUP BY department\nHAVING COUNT(*) > 5;\n```', 15),
            ('JOINs', '## INNER JOIN\n```sql\nSELECT e.name, d.department_name\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id;\n```\n\n## LEFT JOIN\n```sql\n-- All employees, even those with no department\nSELECT e.name, d.department_name\nFROM employees e\nLEFT JOIN departments d ON e.dept_id = d.id;\n```\n\n## FULL OUTER JOIN\n```sql\n-- All rows from both tables\nSELECT * FROM a\nFULL OUTER JOIN b ON a.id = b.a_id;\n```', 15),
            ('Subqueries', '## Scalar Subquery\n```sql\nSELECT name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);\n```\n\n## IN Subquery\n```sql\nSELECT name FROM employees\nWHERE dept_id IN (\n    SELECT id FROM departments WHERE location = \'NYC\'\n);\n```\n\n## EXISTS\n```sql\nSELECT name FROM customers c\nWHERE EXISTS (\n    SELECT 1 FROM orders o WHERE o.customer_id = c.id\n);\n```', 15),
            ('INSERT, UPDATE, DELETE', '## INSERT\n```sql\nINSERT INTO employees (name, salary, dept_id)\nVALUES (\'Alice\', 75000, 3);\n```\n\n## UPDATE\n```sql\nUPDATE employees\nSET salary = salary * 1.1\nWHERE department = \'Engineering\';\n```\n\n## DELETE\n```sql\nDELETE FROM employees\nWHERE last_login < \'2023-01-01\';\n```\n\n> Always use WHERE with UPDATE/DELETE to avoid affecting all rows!', 12),
            ('Indexes and Performance', '## What is an Index?\nAn index speeds up queries but slows down writes.\n\n```sql\nCREATE INDEX idx_employees_name ON employees(name);\nCREATE UNIQUE INDEX idx_email ON users(email);\n```\n\n## When to Use\n- Columns frequently used in WHERE\n- Columns used in JOIN conditions\n- Foreign keys\n\n## EXPLAIN\n```sql\nEXPLAIN SELECT * FROM orders WHERE customer_id = 100;\n```', 12),
        ],
        'quantitative': [
            ('Percentages', '## What is a Percentage?\nA percentage is a fraction of 100.\n\n**Formula**: `Percentage = (Part / Whole) × 100`\n\n## Examples\n- 25% of 200 = (25/100) × 200 = **50**\n- If a price increases by 20%: New = Old × 1.20\n- If a price decreases by 15%: New = Old × 0.85\n\n## Successive Changes\nIf price increases by A% then decreases by B%:\nNet change = A − B − (A×B)/100\n\n**Example**: +20% then −20% = 20 − 20 − 4 = **−4%**', 12),
            ('Ratios and Proportions', '## Ratio\nRatio a:b means a/b.\n\n**Example**: If A:B = 3:5 and total = 160\n- A = 3/8 × 160 = **60**\n- B = 5/8 × 160 = **100**\n\n## Proportion\na/b = c/d → a×d = b×c (cross multiply)\n\n## Direct and Inverse Proportion\n- **Direct**: y increases when x increases\n- **Inverse**: y decreases when x increases\n\n**Example**: 6 workers finish in 8 days. How many days for 4 workers?\n6×8 = 4×d → d = **12 days**', 12),
            ('Time and Work', '## Basic Formula\nIf A can do a job in N days, A\'s rate = 1/N per day.\n\n**Combined rate**: If A takes a days and B takes b days:\nTime together = (a×b)/(a+b)\n\n## Example\nA finishes in 10 days, B in 15 days.\nTogether = (10×15)/(10+15) = 150/25 = **6 days**\n\n## Pipes and Cisterns\n- Inlet fills in A hours → rate = +1/A\n- Outlet empties in B hours → rate = −1/B\n\nTime to fill = 1 / (1/A − 1/B)', 15),
            ('Speed, Distance, Time', '## Formula\n`Speed = Distance / Time`\n`Distance = Speed × Time`\n`Time = Distance / Speed`\n\n## Average Speed\nIf same distance at speeds S1 and S2:\n**Average speed = 2S1S2 / (S1+S2)**\n\n## Relative Speed\n- Same direction: |S1 − S2|\n- Opposite direction: S1 + S2\n\n## Example\nA train 200m long passes a pole in 10s.\nSpeed = 200/10 = 20 m/s = 72 km/h', 12),
            ('Number Series', '## Types of Series\n\n**Arithmetic**: 2, 5, 8, 11, ... (common diff = 3)\n**Geometric**: 3, 6, 12, 24, ... (common ratio = 2)\n**Fibonacci**: 1, 1, 2, 3, 5, 8, 13, ...\n\n## Tricks\n- Find the pattern in differences\n- Check alternating terms\n- Look for squares/cubes: 1, 4, 9, 16, 25...\n\n## Example\n2, 6, 12, 20, 30, ?\nDifferences: 4, 6, 8, 10 → next diff = 12\nAnswer: **42**', 10),
        ],
        'verbal': [
            ('Vocabulary: Synonyms & Antonyms', '## Synonyms (same meaning)\n| Word | Synonyms |\n|------|----------|\n| Benevolent | Kind, Charitable, Generous |\n| Verbose | Wordy, Lengthy, Garrulous |\n| Diligent | Hardworking, Industrious |\n| Ephemeral | Temporary, Fleeting, Transient |\n\n## Antonyms (opposite meaning)\n| Word | Antonym |\n|------|---------|\n| Benevolent | Malevolent |\n| Verbose | Concise |\n| Diligent | Lazy |\n| Ephemeral | Permanent |\n\n## Tip\nLearn roots: "bene" = good, "mal" = bad, "temp" = time', 12),
            ('Grammar: Subject-Verb Agreement', '## Rules\n1. Singular subject → singular verb\n2. Plural subject → plural verb\n\n```\nHe goes to school. ✓\nThey go to school. ✓\nHe go to school. ✗\n```\n\n## Tricky Cases\n- **Either/Neither**: uses singular verb\n  - "Neither of the boys **is** at home."\n- **Collective nouns**: usually singular\n  - "The team **has** won the match."\n- **Indefinite pronouns**: everyone, nobody → singular\n  - "Everyone **was** invited."', 12),
            ('Reading Comprehension Tips', '## Strategy\n1. **Skim** the passage first (30 sec)\n2. **Read** the questions before reading in detail\n3. **Scan** for keywords in the text\n4. **Eliminate** clearly wrong options\n\n## Common Question Types\n- Main idea / Central theme\n- Author\'s tone (positive, critical, neutral)\n- Specific detail\n- Inference (what is implied)\n\n## Tone Words\n| Positive | Negative | Neutral |\n|----------|----------|---------|\n| Admiring | Critical | Objective |\n| Optimistic | Pessimistic | Analytical |', 10),
        ],
    }

    order = 1
    for course_id, lesson_list in lessons_data.items():
        for i, (title, _content, duration) in enumerate(lesson_list, start=1):
            db.session.add(Lesson(
                course_id=course_id,
                title=title,
                duration_mins=duration,
                order=i,
                points=10,
            ))

    db.session.commit()

    total_lessons = sum(len(v) for v in lessons_data.values())
    print(f'Seeded {len(courses)} courses and {total_lessons} lessons successfully')
