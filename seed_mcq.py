"""
Seed MCQ questions into the database.
Subtopic names MUST match PYTHON_TOPIC_META in frontend/lib/python-topics.ts

Run: python seed_mcq.py
"""
from app import create_app
from app.extensions import db
from app.models.mcq import MCQQuestion, MCQAttempt

app = create_app()

def Q(topic, subtopic, question, options, correct_answer, explanation, difficulty='Medium', points=10):
    return MCQQuestion(
        topic=topic, subtopic=subtopic, question=question,
        options=options, correct_answer=correct_answer,
        explanation=explanation, difficulty=difficulty, points=points,
    )

questions = [

    # ══════════════════════════════════════════════════════════════════
    # PYTHON — 12 subtopics × 5 questions = 60 questions
    # Subtopic names match PYTHON_TOPIC_META in frontend/lib/python-topics.ts
    # ══════════════════════════════════════════════════════════════════

    # ── 1. Introduction & Variables ──────────────────────────────────
    Q('Python', 'Introduction & Variables',
      'Which of the following is the correct way to declare a variable in Python?',
      ['int x = 5', 'x = 5', 'var x = 5', 'let x = 5'],
      1, "Python uses dynamic typing — just write x = 5. No type keyword needed.", 'Easy', 5),

    Q('Python', 'Introduction & Variables',
      'What is the output of: print(type(3.14))?',
      ["<class 'float'>", "<class 'double'>", "<class 'number'>", "<class 'decimal'>"],
      0, "Python uses 'float' for decimal numbers. type() returns the class.", 'Easy', 5),

    Q('Python', 'Introduction & Variables',
      'Which of these is a valid f-string?',
      ["f'Hello {name}'", "'Hello {name}'", "f'Hello name'", "f(Hello {name})"],
      0, "F-strings use the f prefix and curly braces {} to embed expressions.", 'Easy', 5),

    Q('Python', 'Introduction & Variables',
      'What does the // operator do in Python?',
      ['Regular division', 'Floor division (rounds down)', 'Power', 'Modulo'],
      1, "// is floor division — divides and rounds down. 7 // 2 = 3.", 'Medium', 10),

    Q('Python', 'Introduction & Variables',
      'Which statement about Python variables is TRUE?',
      ['Variable names can start with a number',
       'Python variables must be declared with a type',
       'A variable can change its type by reassigning a different value',
       'Variable names are case-insensitive'],
      2, "Python is dynamically typed. x = 5 then x = 'hello' is valid — type changes with value.", 'Medium', 10),

    # ── 2. Data Structures ────────────────────────────────────────────
    Q('Python', 'Data Structures',
      'Which of the following creates an empty dictionary?',
      ['[]', '{}', '()', 'set()'],
      1, "{} creates an empty dict. [] is list, () is tuple, set() is set.", 'Easy', 5),

    Q('Python', 'Data Structures',
      'How do you access the value for key "name" in a dictionary d?',
      ['d.name', 'd[name]', "d['name']", 'd->name'],
      2, "Dictionary values are accessed with d['key'] — the key in quotes.", 'Easy', 5),

    Q('Python', 'Data Structures',
      'What is the key difference between a list and a tuple?',
      ['Lists use () and tuples use []',
       'Lists are mutable; tuples are immutable',
       'Lists can only hold numbers',
       'Tuples are faster for all operations'],
      1, "Lists are mutable ([1,2,3]). Tuples are immutable ((1,2,3)).", 'Medium', 10),

    Q('Python', 'Data Structures',
      'What does list.append(x) do?',
      ['Inserts x at index 0',
       'Adds x to the end of the list',
       'Replaces all occurrences of x',
       'Returns a new list with x added'],
      1, "append() adds an element to the END of the list, in-place.", 'Easy', 5),

    Q('Python', 'Data Structures',
      'What is the output of:\nd = {"a": 1, "b": 2}\nd["c"] = d.get("c", 0) + 1\nprint(d)',
      ['{"a": 1, "b": 2}', '{"a": 1, "b": 2, "c": 1}', 'Error', '{"c": 1}'],
      1, "d.get('c', 0) returns 0 (default). 0+1=1. So d['c']=1 is added.", 'Hard', 15),

    # ── 3. Strings & Methods ──────────────────────────────────────────
    Q('Python', 'Strings & Methods',
      'Which method converts a string to all uppercase?',
      ['.upper()', '.toUpper()', '.capitalize()', '.UP()'],
      0, "str.upper() returns the string in uppercase. .capitalize() only capitalises the first letter.", 'Easy', 5),

    Q('Python', 'Strings & Methods',
      "What does 'hello world'.split() return?",
      ["'hello', 'world'", "['hello', 'world']", "['hello world']", 'Error'],
      1, "str.split() splits on whitespace and returns a list.", 'Easy', 5),

    Q('Python', 'Strings & Methods',
      "What is the output of: 'Python'[::-1]?",
      ['Python', 'nohtyP', 'Pytho', 'Error'],
      1, "[::-1] reverses the string. 'Python' reversed is 'nohtyP'.", 'Medium', 10),

    Q('Python', 'Strings & Methods',
      'Which method removes whitespace from both ends of a string?',
      ['.strip()', '.trim()', '.clean()', '.remove()'],
      0, "str.strip() removes leading and trailing whitespace.", 'Easy', 5),

    Q('Python', 'Strings & Methods',
      "What does ', '.join(['a', 'b', 'c']) return?",
      ["['a', 'b', 'c']", "'a, b, c'", "'abc'", "'a b c'"],
      1, "str.join(iterable) joins elements using the string as separator.", 'Medium', 10),

    # ── 4. Control Flow ───────────────────────────────────────────────
    Q('Python', 'Control Flow',
      'Which keyword is used for else-if in Python?',
      ['else if', 'elseif', 'elif', 'otherwise'],
      2, "Python uses 'elif' (not 'else if'). It checks additional conditions.", 'Easy', 5),

    Q('Python', 'Control Flow',
      'What is the output of: print(10 > 5 and 3 < 2)?',
      ['True', 'False', 'None', 'Error'],
      1, "10>5 is True, 3<2 is False. True AND False = False.", 'Easy', 5),

    Q('Python', 'Control Flow',
      'What does the "not" operator do?',
      ['Checks if two values are not equal',
       'Inverts a boolean value (not True = False)',
       'Excludes a value from a set',
       'Same as the != operator'],
      1, "not inverts a boolean: not True = False, not False = True.", 'Medium', 10),

    Q('Python', 'Control Flow',
      'What is a ternary expression in Python?',
      ['An expression with three operators',
       'value_if_true if condition else value_if_false',
       'A 3-way comparison',
       'A try/except/finally block'],
      1, "Python ternary: x = 'yes' if condition else 'no'.", 'Medium', 10),

    Q('Python', 'Control Flow',
      'x = 15. What prints?\nif x > 10: print("A")\nelif x > 12: print("B")\nelse: print("C")',
      ['A', 'B', 'A and B', 'C'],
      0, "The first condition (x > 10) is True so 'A' prints. elif and else are skipped.", 'Hard', 15),

    # ── 5. Loops ──────────────────────────────────────────────────────
    Q('Python', 'Loops',
      'How many times does "for i in range(3):" loop?',
      ['2', '3', '4', '0'],
      1, "range(3) produces [0, 1, 2] — 3 values. The loop runs 3 times.", 'Easy', 5),

    Q('Python', 'Loops',
      'Which statement skips the current iteration and moves to the next?',
      ['break', 'continue', 'pass', 'skip'],
      1, "continue skips the rest of the current iteration. break exits the loop entirely.", 'Easy', 5),

    Q('Python', 'Loops',
      'What is the output of:\nfor i in range(1, 6, 2):\n    print(i, end=" ")',
      ['1 2 3 4 5', '1 3 5', '2 4 6', '1 3 5 7'],
      1, "range(1, 6, 2): start 1, stop before 6, step 2 → 1, 3, 5.", 'Medium', 10),

    Q('Python', 'Loops',
      'When should you prefer a while loop over a for loop?',
      ['When iterating over a list',
       'When the number of iterations is unknown and depends on a condition',
       'When you need enumerate()',
       'When you need the loop index'],
      1, "while loops are best when you don't know how many times to loop in advance.", 'Medium', 10),

    Q('Python', 'Loops',
      'What does the else clause on a for loop do in Python?',
      ['Runs if the loop encountered an error',
       'Runs if the loop was skipped entirely',
       'Runs after the loop completes without hitting a break',
       'Python does not support else on loops'],
      2, "for...else: the else block runs ONLY if the loop finished normally (no break).", 'Hard', 15),

    # ── 6. Functions ──────────────────────────────────────────────────
    Q('Python', 'Functions',
      'What keyword defines a function in Python?',
      ['function', 'def', 'fn', 'func'],
      1, "'def' defines a function in Python: def my_func():.", 'Easy', 5),

    Q('Python', 'Functions',
      'What does a function return if it has no return statement?',
      ['0', "''", 'None', 'Error'],
      2, "A function without return implicitly returns None.", 'Easy', 5),

    Q('Python', 'Functions',
      'What are default parameter values?',
      ['Parameters that are automatically 0',
       'Values used when the caller does not provide that argument',
       'Parameters that must always be provided',
       'The first parameter of every function'],
      1, "Default values: def greet(name='Guest'): — if no name passed, 'Guest' is used.", 'Medium', 10),

    Q('Python', 'Functions',
      'What does **kwargs allow in a function?',
      ['Any number of positional arguments as a tuple',
       'Any number of keyword arguments as a dictionary',
       'Required keyword-only arguments',
       'Pointer to another function'],
      1, "**kwargs collects extra keyword arguments into a dict inside the function.", 'Medium', 10),

    Q('Python', 'Functions',
      'What is a lambda function?',
      ['A function defined inside a class',
       'A function that calls itself',
       'An anonymous one-expression function: lambda args: expression',
       'A function imported from another module'],
      2, "lambda creates a small anonymous function: double = lambda x: x * 2.", 'Hard', 15),

    # ── 7. Built-in Modules ───────────────────────────────────────────
    Q('Python', 'Built-in Modules',
      'How do you import the math module?',
      ['include math', 'import math', 'using math', "require('math')"],
      1, "Python uses 'import module_name'. Use math.sqrt(), math.pi after importing.", 'Easy', 5),

    Q('Python', 'Built-in Modules',
      'Which module generates random numbers in Python?',
      ['math', 'random', 'numbers', 'rand'],
      1, "The 'random' module: random.random(), random.randint(a,b), random.choice(list).", 'Easy', 5),

    Q('Python', 'Built-in Modules',
      'What does datetime.now() return?',
      ['The current Unix timestamp as an integer',
       'A datetime object with the current date and time',
       'The current time as a string',
       'The number of seconds since 1970'],
      1, "from datetime import datetime; datetime.now() returns a datetime object.", 'Medium', 10),

    Q('Python', 'Built-in Modules',
      "What does json.dumps({'key': 'value'}) do?",
      ['Reads a JSON file',
       'Converts a Python dict to a JSON string',
       'Parses a JSON string into a dict',
       'Saves JSON to a database'],
      1, "json.dumps() serialises Python objects to a JSON string. json.loads() is the reverse.", 'Medium', 10),

    Q('Python', 'Built-in Modules',
      'How do you import only sqrt from the math module?',
      ['import sqrt from math', 'from math import sqrt', 'import math.sqrt', 'include math.sqrt'],
      1, "'from math import sqrt' lets you call sqrt() directly without the math. prefix.", 'Hard', 15),

    # ── 8. File I/O ───────────────────────────────────────────────────
    Q('Python', 'File I/O',
      'Which file mode opens for writing, creating or overwriting?',
      ["'r'", "'a'", "'w'", "'x'"],
      2, "'w' mode writes and overwrites. 'a' appends. 'r' reads. 'x' creates (fails if exists).", 'Easy', 5),

    Q('Python', 'File I/O',
      "Why use 'with open(file) as f:' instead of f = open(file)?",
      ['with is faster',
       'with automatically closes the file even if an error occurs',
       'with allows reading and writing simultaneously',
       'There is no difference'],
      1, "The context manager guarantees the file is closed when the block exits.", 'Easy', 5),

    Q('Python', 'File I/O',
      'How do you read all lines of a file into a list?',
      ['f.read()', 'f.readline()', 'f.readlines()', 'f.lines()'],
      2, "f.readlines() returns a list of strings, one per line (with newlines).", 'Medium', 10),

    Q('Python', 'File I/O',
      'Which modules handle file paths in Python?',
      ['fileutils', 'path', 'os and pathlib', 'system'],
      2, "Both 'os' (os.path.join) and 'pathlib' (Path objects) handle paths cross-platform.", 'Medium', 10),

    Q('Python', 'File I/O',
      'What does csv.DictReader do?',
      ['Reads CSV rows as plain lists',
       'Reads CSV rows as dicts, using the header row as keys',
       'Writes a dict to a CSV file',
       'Validates CSV format'],
      1, "csv.DictReader maps CSV column headers to values, returning OrderedDicts per row.", 'Hard', 15),

    # ── 9. OOP Basics ─────────────────────────────────────────────────
    Q('Python', 'OOP Basics',
      'What is __init__ in a Python class?',
      ['A method that destroys an object',
       'A constructor that initialises a new object',
       'A method that prints the object',
       'A required method for all classes'],
      1, "__init__ is called automatically when you create an object. It sets initial attributes.", 'Easy', 5),

    Q('Python', 'OOP Basics',
      "What does 'self' refer to in a class method?",
      ['The class itself',
       'The current object (instance) calling the method',
       'The parent class',
       'A global variable'],
      1, "'self' is a reference to the calling instance — how methods access instance attributes.", 'Easy', 5),

    Q('Python', 'OOP Basics',
      'What is the difference between a class attribute and an instance attribute?',
      ['No difference',
       'Class attributes are shared by all instances; instance attributes are unique per object',
       'Instance attributes are faster',
       'Class attributes cannot be changed'],
      1, "Class attributes (in class body) are shared. Instance attributes (self.x) belong to each object.", 'Medium', 10),

    Q('Python', 'OOP Basics',
      'How do you create an object from a class called Student?',
      ['Student.new("Arjun")', 'new Student("Arjun")', 's = Student("Arjun")', 'Student.create("Arjun")'],
      2, "Call the class like a function: s = Student('Arjun'). This invokes __init__.", 'Easy', 5),

    Q('Python', 'OOP Basics',
      'What is a @property decorator used for?',
      ['Making a method static',
       'Allowing a method to be accessed like an attribute (computed property)',
       'Preventing a method from being overridden',
       'Making an attribute private'],
      1, "@property lets obj.full_name access a computed value without calling it as a method.", 'Hard', 15),

    # ── 10. Inheritance ───────────────────────────────────────────────
    Q('Python', 'Inheritance',
      'How do you define a class Admin that inherits from class User?',
      ['class Admin extends User:', 'class Admin inherits User:', 'class Admin(User):', 'class Admin <- User:'],
      2, "Python inheritance: class Child(Parent):. Admin(User) inherits all User methods.", 'Easy', 5),

    Q('Python', 'Inheritance',
      'What does super() do in Python?',
      ['Makes the class a superclass',
       'Calls a method from the parent class',
       'Creates a super user',
       'Skips the parent __init__'],
      1, "super() gives access to parent class methods. super().__init__() calls the parent constructor.", 'Easy', 5),

    Q('Python', 'Inheritance',
      'What is method overriding?',
      ['Calling a method twice',
       'A child class providing its own version of a parent method',
       'Adding more parameters to a method',
       "Deleting a parent method"],
      1, "Overriding: child defines same method name as parent. Python calls the child's version.", 'Medium', 10),

    Q('Python', 'Inheritance',
      'What is polymorphism in Python?',
      ['Having many classes in one file',
       'Different object types used interchangeably through a shared method interface',
       'Multiple inheritance only',
       'Converting between data types'],
      1, "Polymorphism: different classes implementing the same method name, each behaving differently.", 'Medium', 10),

    Q('Python', 'Inheritance',
      'What is the MRO (Method Resolution Order)?',
      ['The order in which modules are imported',
       'The order Python searches for methods in class hierarchies',
       'The order methods are defined in a class',
       'The order of method parameters'],
      1, "MRO determines which class method is called in multiple inheritance (C3 linearisation).", 'Hard', 15),

    # ── 11. Exception Handling ────────────────────────────────────────
    Q('Python', 'Exception Handling',
      'What is the syntax for handling exceptions in Python?',
      ['try { } catch { }', 'try: ... except: ...', 'try: ... error: ...', 'begin: ... rescue: ...'],
      1, "Python uses try/except. try: runs code. except ExceptionType: handles the error.", 'Easy', 5),

    Q('Python', 'Exception Handling',
      "What does the 'finally' block guarantee?",
      ['Runs only if no exception occurred',
       'Runs only if an exception occurred',
       'Always runs, whether or not an exception occurred',
       'Runs after returning from a function'],
      2, "finally always executes — used for cleanup like closing files or DB connections.", 'Easy', 5),

    Q('Python', 'Exception Handling',
      'How do you raise a ValueError with a message?',
      ["throw ValueError('msg')", "raise ValueError('msg')",
       "error ValueError('msg')", "except ValueError('msg')"],
      1, "Python uses 'raise' to throw exceptions: raise ValueError('Invalid input').", 'Medium', 10),

    Q('Python', 'Exception Handling',
      'What is the purpose of creating custom exception classes?',
      ['To make code run faster',
       'To group and identify domain-specific errors clearly',
       'Required to use try/except',
       'To bypass built-in error handling'],
      1, "Custom exceptions give meaningful names to domain errors and allow targeted except blocks.", 'Medium', 10),

    Q('Python', 'Exception Handling',
      "What does 'except Exception as e' let you do?",
      ['Catch only the Exception base class',
       "Catch any exception and access the exception object as variable e",
       "Create a new exception named e",
       'Rethrow the exception'],
      1, "'as e' binds the exception to a variable so you can print(e) for the error message.", 'Hard', 15),

    # ── 12. List Comprehensions ───────────────────────────────────────
    Q('Python', 'List Comprehensions',
      'Which is a valid list comprehension?',
      ['[for x in range(5)]', '[x for x in range(5)]',
       '{x for x in range(5)}', 'list(x for x in range(5))'],
      1, "[expression for item in iterable] is the basic list comprehension syntax.", 'Easy', 5),

    Q('Python', 'List Comprehensions',
      'What does [x**2 for x in range(4)] produce?',
      ['[1, 4, 9, 16]', '[0, 1, 4, 9]', '[0, 2, 4, 6]', '[1, 2, 3, 4]'],
      1, "range(4)=[0,1,2,3]. x**2: 0,1,4,9 -> [0, 1, 4, 9].", 'Easy', 5),

    Q('Python', 'List Comprehensions',
      'How do you add a filter condition to a list comprehension?',
      ['[x if x > 2 for x in lst]', '[x for x in lst if x > 2]',
       '[x for x in lst | x > 2]', '[x where x > 2 for x in lst]'],
      1, "[x for x in lst if condition] — only items where condition is True are included.", 'Medium', 10),

    Q('Python', 'List Comprehensions',
      'What is a generator expression vs a list comprehension?',
      ['No difference — both create lists',
       'Generator uses () and produces values lazily; list comprehension builds the full list in memory',
       'Generator expressions are always faster',
       'List comprehensions can only use numbers'],
      1, "(x for x in range(n)) is memory-efficient — values computed on demand.", 'Medium', 10),

    Q('Python', 'List Comprehensions',
      "What does {k: v*2 for k, v in {'a': 1, 'b': 2}.items()} produce?",
      ["{'a': 1, 'b': 2}", "{'a': 2, 'b': 4}", "['a', 'b']", 'Error'],
      1, "Dict comprehension iterates over .items() and builds a new dict with doubled values.", 'Hard', 15),

    # ══════════════════════════════════════════════════════════════════
    # SQL
    # ══════════════════════════════════════════════════════════════════
    Q('SQL', 'SELECT Queries',
      'Which clause filters rows in SQL?',
      ['HAVING', 'WHERE', 'FILTER', 'SELECT'],
      1, "WHERE filters rows before grouping. HAVING filters after GROUP BY.", 'Easy', 5),

    Q('SQL', 'SELECT Queries',
      'What does SELECT DISTINCT do?',
      ['Returns NULL values', 'Returns unique rows', 'Returns the first row', 'Returns sorted rows'],
      1, "DISTINCT eliminates duplicate rows from the result set.", 'Easy', 5),

    Q('SQL', 'SELECT Queries',
      'What is the correct order of SQL clauses?',
      ['WHERE, SELECT, FROM',
       'SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY',
       'FROM, WHERE, SELECT',
       'SELECT, WHERE, FROM'],
      1, "Standard order: SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY.", 'Medium', 10),

    Q('SQL', 'Joins',
      'Which JOIN returns all rows from both tables with NULLs where no match?',
      ['INNER JOIN', 'LEFT JOIN', 'FULL OUTER JOIN', 'CROSS JOIN'],
      2, "FULL OUTER JOIN returns all rows from both tables, NULLs on the non-matching side.", 'Medium', 10),

    Q('SQL', 'Joins',
      'What does INNER JOIN return?',
      ['All rows from left table', 'All rows from right table',
       'Only rows with a match in both tables', 'All rows from both tables'],
      2, "INNER JOIN returns only rows where there is a match in both tables.", 'Easy', 5),

    Q('SQL', 'Joins',
      'How do you find records in Table A with NO match in Table B?',
      ['INNER JOIN', 'LEFT JOIN ... WHERE B.id IS NULL',
       'RIGHT JOIN', 'FULL JOIN ... WHERE A.id = B.id'],
      1, "LEFT JOIN keeps all A rows. WHERE B.id IS NULL filters to only unmatched rows.", 'Hard', 15),

    Q('SQL', 'Aggregations',
      'Which aggregate function returns the highest value in a column?',
      ['TOP()', 'MAXIMUM()', 'MAX()', 'HIGHEST()'],
      2, "MAX() returns the maximum value. MIN() for minimum. Both ignore NULLs.", 'Easy', 5),

    Q('SQL', 'Aggregations',
      'Which clause filters groups after GROUP BY?',
      ['WHERE', 'FILTER', 'HAVING', 'WHEN'],
      2, "HAVING filters after grouping and can use aggregate functions like COUNT, SUM.", 'Medium', 10),

    Q('SQL', 'Aggregations',
      'Difference between COUNT(*) and COUNT(column)?',
      ['No difference',
       'COUNT(*) counts all rows including NULLs; COUNT(column) only counts non-NULL values',
       'COUNT(column) is faster',
       'COUNT(*) counts only distinct rows'],
      1, "COUNT(*) counts every row. COUNT(col) skips NULL values in that column.", 'Hard', 15),

    # ══════════════════════════════════════════════════════════════════
    # Data Structures
    # ══════════════════════════════════════════════════════════════════
    Q('Data Structures', 'Arrays & Lists',
      'Time complexity of accessing an array element by index?',
      ['O(n)', 'O(log n)', 'O(1)', 'O(n²)'],
      2, "Array index access is O(1) — direct memory address calculation.", 'Easy', 5),

    Q('Data Structures', 'Arrays & Lists',
      'Worst-case time complexity of linear search in an unsorted array?',
      ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
      2, "Linear search checks each element — worst case is O(n).", 'Easy', 5),

    Q('Data Structures', 'Stacks & Queues',
      'What ordering does a Stack follow?',
      ['FIFO', 'LIFO', 'Random', 'Sorted'],
      1, "Stack is LIFO — Last In First Out. Like a stack of plates.", 'Easy', 5),

    Q('Data Structures', 'Stacks & Queues',
      'Which data structure is used to implement BFS?',
      ['Stack', 'Queue', 'Heap', 'Linked List'],
      1, "BFS uses a Queue (FIFO) to explore nodes level by level.", 'Medium', 10),

    Q('Data Structures', 'Trees',
      'In a BST, which traversal gives sorted output?',
      ['Preorder', 'Postorder', 'Inorder', 'Level order'],
      2, "Inorder traversal (Left -> Root -> Right) of a BST gives sorted ascending order.", 'Medium', 10),

    Q('Data Structures', 'Trees',
      'Time complexity of searching in a balanced BST?',
      ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
      1, "A balanced BST halves the search space at each step — O(log n).", 'Medium', 10),

    Q('Data Structures', 'Sorting',
      'Average time complexity of Merge Sort?',
      ['O(n²)', 'O(n log n)', 'O(n)', 'O(log n)'],
      1, "Merge Sort always runs in O(n log n) — splits log n levels, n work per level.", 'Medium', 10),

    Q('Data Structures', 'Sorting',
      'Worst-case time complexity of QuickSort?',
      ['O(n log n)', 'O(n)', 'O(n²)', 'O(log n)'],
      2, "QuickSort worst case is O(n²) when the pivot is always the min or max element.", 'Hard', 15),

    Q('Data Structures', 'Hashing',
      'Average time complexity of HashMap get() and put()?',
      ['O(n)', 'O(log n)', 'O(1)', 'O(n log n)'],
      2, "Hash maps give O(1) average by computing a hash to find the bucket directly.", 'Medium', 10),

    # ══════════════════════════════════════════════════════════════════
    # Aptitude
    # ══════════════════════════════════════════════════════════════════
    Q('Aptitude', 'Percentages',
      'What is 25% of 200?',
      ['25', '50', '75', '100'],
      1, "25/100 × 200 = 50.", 'Easy', 5),

    Q('Aptitude', 'Percentages',
      'A price increases by 20% then decreases by 20%. Net change?',
      ['0%', '-4%', '+4%', '-2%'],
      1, "100 -> 120 -> 96. Net = -4%.", 'Medium', 10),

    Q('Aptitude', 'Time & Work',
      'A finishes in 10 days, B in 15 days. Together how many days?',
      ['5 days', '6 days', '8 days', '12 days'],
      1, "1/10 + 1/15 = 1/6. Together: 6 days.", 'Medium', 10),

    Q('Aptitude', 'Time & Work',
      'A is twice as fast as B. B takes 12 days. How long for A alone?',
      ['6 days', '4 days', '8 days', '3 days'],
      0, "A is twice as fast, so A takes 12/2 = 6 days.", 'Easy', 5),

    Q('Aptitude', 'Speed & Distance',
      'A train travels 360 km in 4 hours. Speed in km/h?',
      ['80', '90', '100', '75'],
      1, "Speed = Distance / Time = 360 / 4 = 90 km/h.", 'Easy', 5),

    Q('Aptitude', 'Speed & Distance',
      'Car covers 240 km at 60 km/h and returns at 80 km/h. Average speed?',
      ['70 km/h', '68.57 km/h', '72 km/h', '75 km/h'],
      1, "Harmonic mean: 2×60×80/(60+80) = 9600/140 ≈ 68.57 km/h.", 'Hard', 15),

    Q('Aptitude', 'Number Series',
      'Next in series: 1, 1, 2, 3, 5, 8, 13, __?',
      ['18', '20', '21', '24'],
      2, "Fibonacci: each term = sum of previous two. 8 + 13 = 21.", 'Easy', 5),

    # ══════════════════════════════════════════════════════════════════
    # Verbal
    # ══════════════════════════════════════════════════════════════════
    Q('Verbal', 'Vocabulary',
      'Antonym of "benevolent"?',
      ['Kind', 'Malevolent', 'Generous', 'Charitable'],
      1, "Benevolent means kind/well-meaning. Malevolent means wishing harm.", 'Easy', 5),

    Q('Verbal', 'Vocabulary',
      'What does "verbose" mean?',
      ['Brief and concise', 'Using more words than needed', 'Silent', 'Clearly expressed'],
      1, "Verbose means using or expressed in more words than are needed.", 'Easy', 5),

    Q('Verbal', 'Grammar',
      'Which sentence is grammatically correct?',
      ['He go to school', 'He goes to school', 'He going to school', 'He gone to school'],
      1, '"He goes to school" — correct subject-verb agreement for third person singular.', 'Easy', 5),
]


with app.app_context():
    # Clear existing MCQ data cleanly
    print('Clearing existing MCQ data...')
    MCQAttempt.query.delete()
    MCQQuestion.query.delete()
    db.session.commit()

    for q in questions:
        db.session.add(q)
    db.session.commit()

    from sqlalchemy import func
    total = MCQQuestion.query.count()
    python_count = MCQQuestion.query.filter_by(topic='Python').count()

    print(f'\nSeeded {total} MCQ questions total')
    print(f'\nPython: {python_count} questions across 12 subtopics:')
    rows = (db.session.query(MCQQuestion.subtopic, func.count(MCQQuestion.id))
            .filter_by(topic='Python')
            .group_by(MCQQuestion.subtopic)
            .order_by(MCQQuestion.subtopic)
            .all())
    for subtopic, count in rows:
        print(f'   • {subtopic}: {count} questions')

    print('\nOther topics:')
    other = (db.session.query(MCQQuestion.topic, func.count(MCQQuestion.id))
             .filter(MCQQuestion.topic != 'Python')
             .group_by(MCQQuestion.topic)
             .all())
    for topic, count in other:
        print(f'   • {topic}: {count} questions')
