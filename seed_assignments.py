"""
Seed assignment questions into the assignment_questions table.
Run: .venv/Scripts/python.exe seed_assignments.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.assignment import AssignmentQuestion, AssignmentAttempt

app = create_app()


def Q(module_id, topic, subtopic, question, options, correct_answer, explanation, difficulty='Medium', points=5):
    return AssignmentQuestion(
        module_id=module_id,
        topic=topic,
        subtopic=subtopic,
        question=question,
        options=options,
        correct_answer=correct_answer,
        explanation=explanation,
        difficulty=difficulty,
        points=points,
        is_active=True,
    )


QUESTIONS = [

    # ─── PYTHON BASICS (module_id='python-basics', 12 questions) ───────────────
    Q('python-basics', 'Python', 'Introduction & Variables',
      "What is the correct way to declare a variable in Python?",
      ["int x = 5", "x = 5", "var x = 5", "declare x = 5"], 1,
      "Python uses dynamic typing. Simply assign a value with `x = 5` — no type declaration needed."),

    Q('python-basics', 'Python', 'Introduction & Variables',
      "Which of the following is NOT a valid Python data type?",
      ["int", "float", "char", "bool"], 2,
      "Python has int, float, bool, str, list, dict, etc. There is no `char` type — single characters are just strings of length 1."),

    Q('python-basics', 'Python', 'Data Structures',
      "How do you create an empty list in Python?",
      ["list = {}", "list = []", "list = ()", "list = <>"], 1,
      "Square brackets `[]` create a list. `{}` creates a dict, `()` creates a tuple."),

    Q('python-basics', 'Python', 'Data Structures',
      "What is the output of `len({'a': 1, 'b': 2, 'c': 3})`?",
      ["6", "3", "2", "Error"], 1,
      "len() on a dictionary returns the number of key-value pairs, which is 3."),

    Q('python-basics', 'Python', 'Data Structures',
      "Which data structure uses key-value pairs?",
      ["List", "Tuple", "Dictionary", "Set"], 2,
      "Dictionaries store data as key-value pairs, e.g. `{'name': 'Alice', 'age': 25}`."),

    Q('python-basics', 'Python', 'Strings & Methods',
      "What does `'hello'.upper()` return?",
      ["hello", "HELLO", "Hello", "hELLO"], 1,
      "The `upper()` method converts all characters to uppercase."),

    Q('python-basics', 'Python', 'Strings & Methods',
      "How do you find the length of the string `s = 'Python'`?",
      ["s.length()", "length(s)", "len(s)", "s.size()"], 2,
      "Python uses the built-in `len()` function: `len('Python')` returns 6."),

    Q('python-basics', 'Python', 'Strings & Methods',
      "What is the result of `'Python'[1:4]`?",
      ["Pyt", "yth", "ytho", "Pyth"], 1,
      "Slicing `[1:4]` returns characters at indices 1, 2, 3 → 'yth'."),

    Q('python-basics', 'Python', 'Control Flow',
      "Which keyword is used for conditional execution in Python?",
      ["when", "if", "check", "case"], 1,
      "Python uses `if`, `elif`, and `else` for conditional branching."),

    Q('python-basics', 'Python', 'Control Flow',
      "What will `print(5 > 3 and 2 < 1)` output?",
      ["True", "False", "Error", "None"], 1,
      "`5 > 3` is True, but `2 < 1` is False. `True and False` = False."),

    Q('python-basics', 'Python', 'Control Flow',
      "What does the `pass` statement do in Python?",
      ["Exits the program", "Skips the current iteration", "Does nothing — placeholder", "Returns None"], 2,
      "`pass` is a null operation. It is used as a placeholder where code is syntactically required but you don't want any action."),

    Q('python-basics', 'Python', 'Control Flow',
      "Which operator checks equality in Python?",
      ["=", "==", "===", ":="], 1,
      "`==` checks equality. `=` is assignment, `===` doesn't exist in Python, `:=` is the walrus operator."),

    # ─── PYTHON INTERMEDIATE (module_id='python-intermediate', 12 questions) ───
    Q('python-intermediate', 'Python', 'Loops',
      "What is the output of `for i in range(3): print(i)`?",
      ["1 2 3", "0 1 2", "0 1 2 3", "1 2"], 1,
      "`range(3)` generates 0, 1, 2. So the output is 0, 1, 2 (one per line)."),

    Q('python-intermediate', 'Python', 'Loops',
      "Which statement immediately exits a loop?",
      ["continue", "exit", "break", "stop"], 2,
      "`break` immediately terminates the loop. `continue` skips to the next iteration."),

    Q('python-intermediate', 'Python', 'Loops',
      "What is the purpose of `continue` in a loop?",
      ["Exit the loop", "Skip remaining code in iteration and go to next", "Restart the loop from the beginning", "Pause the loop"], 1,
      "`continue` skips the rest of the current loop body and jumps to the next iteration."),

    Q('python-intermediate', 'Python', 'Functions',
      "Which keyword is used to define a function in Python?",
      ["function", "def", "func", "define"], 1,
      "Functions are defined with the `def` keyword: `def my_function():`."),

    Q('python-intermediate', 'Python', 'Functions',
      "What does a function return if no `return` statement is used?",
      ["0", "False", "None", "Empty string"], 2,
      "Python functions implicitly return `None` if no `return` statement is present."),

    Q('python-intermediate', 'Python', 'Functions',
      "What is a lambda function?",
      ["A named function", "A class method", "An anonymous single-expression function", "A built-in function"], 2,
      "Lambda creates small anonymous functions: `lambda x: x * 2`. They are limited to a single expression."),

    Q('python-intermediate', 'Python', 'Built-in Modules',
      "Which module provides mathematical functions like `sqrt()` and `pi`?",
      ["numpy", "math", "calc", "numbers"], 1,
      "The `math` module provides mathematical operations: `import math; math.sqrt(16)` returns 4.0."),

    Q('python-intermediate', 'Python', 'Built-in Modules',
      "How do you generate a random integer between 1 and 10 (inclusive)?",
      ["random.rand(1, 10)", "random.randint(1, 10)", "random.integer(1, 10)", "math.random(1, 10)"], 1,
      "`random.randint(a, b)` returns a random integer N such that a <= N <= b."),

    Q('python-intermediate', 'Python', 'Built-in Modules',
      "Which module is used to work with dates and times?",
      ["time_module", "calendar", "datetime", "clock"], 2,
      "The `datetime` module provides classes for date, time, and datetime manipulation."),

    Q('python-intermediate', 'Python', 'File I/O',
      "Which mode opens a file for reading in Python?",
      ["'w'", "'r'", "'a'", "'x'"], 1,
      "`open('file.txt', 'r')` opens for reading. 'w' writes (overwrites), 'a' appends, 'x' creates new."),

    Q('python-intermediate', 'Python', 'File I/O',
      "What is the correct way to open a file safely in Python?",
      ["file = open('f.txt')", "with open('f.txt') as file:", "open file 'f.txt':", "file.open('f.txt')"], 1,
      "The `with` statement (context manager) ensures the file is automatically closed even if an error occurs."),

    Q('python-intermediate', 'Python', 'File I/O',
      "Which method reads all lines of a file into a list?",
      ["read()", "readline()", "readlines()", "readall()"], 2,
      "`readlines()` returns a list where each element is one line of the file including the newline character."),

    # ─── PYTHON ADVANCED (module_id='python-advanced', 12 questions) ───────────
    Q('python-advanced', 'Python', 'OOP Basics',
      "Which keyword creates a class in Python?",
      ["object", "class", "new", "struct"], 1,
      "Classes are defined with the `class` keyword: `class MyClass:`."),

    Q('python-advanced', 'Python', 'OOP Basics',
      "What is `__init__` in a Python class?",
      ["A destructor method", "A constructor method called on object creation", "A static method", "A class variable"], 1,
      "`__init__` is the initializer (constructor). It is called automatically when a new instance is created."),

    Q('python-advanced', 'Python', 'OOP Basics',
      "What does `self` refer to in a class method?",
      ["The class itself", "The current instance of the class", "The parent class", "A static reference"], 1,
      "`self` refers to the current instance. It must be the first parameter of instance methods."),

    Q('python-advanced', 'Python', 'Inheritance',
      "How do you inherit from a parent class in Python?",
      ["class Child(Parent):", "class Child extends Parent:", "class Child inherits Parent:", "class Child -> Parent:"], 0,
      "Inheritance is expressed by putting the parent class in parentheses: `class Child(Parent):`."),

    Q('python-advanced', 'Python', 'Inheritance',
      "Which function calls the parent class's method?",
      ["parent()", "super()", "base()", "inherit()"], 1,
      "`super()` returns a proxy object that allows calling methods of the parent class."),

    Q('python-advanced', 'Python', 'Inheritance',
      "What is method overriding?",
      ["Defining a method in a parent class", "Redefining a parent class method in a child class", "Calling two methods at once", "Adding extra parameters to a method"], 1,
      "Method overriding means redefining a method in the child class with the same name, replacing the parent's implementation."),

    Q('python-advanced', 'Python', 'Exception Handling',
      "Which keyword is used to catch exceptions in Python?",
      ["catch", "except", "handle", "error"], 1,
      "Python uses `try`/`except` blocks. The `except` clause catches specific or general exceptions."),

    Q('python-advanced', 'Python', 'Exception Handling',
      "What happens if an exception is not caught?",
      ["Python ignores it", "The program terminates with a traceback", "The program continues normally", "Python auto-fixes it"], 1,
      "An uncaught exception propagates up the call stack and eventually terminates the program, printing a traceback."),

    Q('python-advanced', 'Python', 'Exception Handling',
      "Which block always runs regardless of whether an exception occurred?",
      ["else", "except", "finally", "catch"], 2,
      "The `finally` block always executes — whether an exception was raised or not. Used for cleanup code."),

    Q('python-advanced', 'Python', 'List Comprehensions',
      "What is the output of `[x**2 for x in range(4)]`?",
      ["[1, 4, 9, 16]", "[0, 1, 4, 9]", "[0, 1, 2, 3]", "[1, 2, 3, 4]"], 1,
      "`range(4)` = 0,1,2,3. Squaring each: 0,1,4,9. Result: [0, 1, 4, 9]."),

    Q('python-advanced', 'Python', 'List Comprehensions',
      "Which list comprehension filters even numbers from 0 to 9?",
      ["[x for x in range(10) if x % 2 != 0]", "[x for x in range(10) if x % 2 == 0]", "[x if x % 2 == 0 for x in range(10)]", "[filter(x, range(10))]"], 1,
      "`x % 2 == 0` is True for even numbers. The comprehension `[x for x in range(10) if x % 2 == 0]` gives [0,2,4,6,8]."),

    Q('python-advanced', 'Python', 'List Comprehensions',
      "What is a generator expression?",
      ["A list comprehension that returns a generator instead of a list", "A function that generates lists", "A comprehension using curly braces", "A built-in function"], 0,
      "Generator expressions use `()` instead of `[]`. They yield items lazily without storing all items in memory."),

    # ─── GENERAL ASSIGNMENT 1: Python Basics (module_id='1', 10 questions) ──────
    Q('1', 'Python', 'Basics',
      "What will `print(type(42))` output?",
      ["<class 'int'>", "<class 'number'>", "<class 'integer'>", "<type 'int'>"], 0,
      "In Python 3, type() returns the class type. For integer 42, it returns <class 'int'>."),

    Q('1', 'Python', 'Basics',
      "Which of the following is a valid Python variable name?",
      ["2myVar", "my-var", "_myVar", "my var"], 2,
      "Variable names can start with underscore or a letter, not a digit or hyphen, and spaces are not allowed."),

    Q('1', 'Python', 'Basics',
      "What does the `//` operator do in Python?",
      ["Regular division", "Floor division", "Power", "Modulo"], 1,
      "`//` is floor division — it divides and rounds down to the nearest integer. `7 // 2` = 3."),

    Q('1', 'Python', 'Basics',
      "What is the output of `bool('')`?",
      ["True", "False", "Error", "None"], 1,
      "Empty strings are falsy in Python. `bool('')` returns False."),

    Q('1', 'Python', 'Basics',
      "Which method adds an element to the end of a list?",
      ["add()", "insert()", "append()", "push()"], 2,
      "`list.append(item)` adds the item to the end of the list."),

    Q('1', 'Python', 'Basics',
      "What is the result of `3 ** 2`?",
      ["6", "9", "8", "Error"], 1,
      "`**` is the exponentiation operator. `3 ** 2` = 3² = 9."),

    Q('1', 'Python', 'Basics',
      "How do you create a tuple with a single element?",
      ["(1)", "(1,)", "[1]", "{1}"], 1,
      "A single-element tuple requires a trailing comma: `(1,)`. `(1)` is just the integer 1 in parentheses."),

    Q('1', 'Python', 'Basics',
      "What does `range(2, 10, 3)` generate?",
      ["2, 5, 8", "2, 4, 6, 8", "2, 3, 4, ... 9", "2, 10, 3"], 0,
      "`range(start, stop, step)` generates 2, 5, 8 (step of 3, stopping before 10)."),

    Q('1', 'Python', 'Basics',
      "Which of these is a mutable data type?",
      ["int", "tuple", "str", "list"], 3,
      "Lists are mutable (can be changed after creation). int, tuple, and str are immutable."),

    Q('1', 'Python', 'Basics',
      "What is the output of `'hello' * 2`?",
      ["hellohello", "hello 2", "hello*2", "Error"], 0,
      "String multiplication repeats the string: `'hello' * 2` = 'hellohello'."),

    # ─── GENERAL ASSIGNMENT 2: SQL Joins (module_id='2', 10 questions) ──────────
    Q('2', 'SQL', 'Joins',
      "Which JOIN returns all rows from both tables, with NULLs where no match?",
      ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], 3,
      "FULL OUTER JOIN returns all rows from both tables. Non-matching rows get NULL values."),

    Q('2', 'SQL', 'Joins',
      "What does an INNER JOIN return?",
      ["All rows from the left table", "All rows from both tables", "Only rows with matching values in both tables", "All rows from the right table"], 2,
      "INNER JOIN returns only the rows that have matching values in both tables."),

    Q('2', 'SQL', 'Queries',
      "Which clause filters rows AFTER grouping?",
      ["WHERE", "HAVING", "FILTER", "GROUP BY"], 1,
      "HAVING filters groups after GROUP BY. WHERE filters individual rows before grouping."),

    Q('2', 'SQL', 'Queries',
      "What does `SELECT DISTINCT name FROM users` do?",
      ["Selects all names", "Selects only unique names", "Deletes duplicate names", "Selects names alphabetically"], 1,
      "DISTINCT eliminates duplicate values from the result set."),

    Q('2', 'SQL', 'Joins',
      "What is the result of a LEFT JOIN when the right table has no match?",
      ["The row is excluded", "NULL is returned for right table columns", "An error occurs", "Zero is returned"], 1,
      "In a LEFT JOIN, all rows from the left table are included. Columns from the right table are NULL when there is no match."),

    Q('2', 'SQL', 'Queries',
      "Which aggregate function returns the number of rows?",
      ["SUM()", "AVG()", "COUNT()", "MAX()"], 2,
      "COUNT() counts the number of rows. COUNT(*) counts all rows; COUNT(column) counts non-NULL values."),

    Q('2', 'SQL', 'Queries',
      "What does `ORDER BY salary DESC` do?",
      ["Sorts salary ascending", "Sorts salary descending", "Filters salary", "Groups by salary"], 1,
      "DESC sorts in descending order (highest to lowest). ASC is the default (lowest to highest)."),

    Q('2', 'SQL', 'Queries',
      "Which SQL statement is used to retrieve data?",
      ["INSERT", "UPDATE", "SELECT", "DELETE"], 2,
      "SELECT is the DML statement for reading/retrieving data from a database."),

    Q('2', 'SQL', 'Joins',
      "A CROSS JOIN produces:",
      ["Rows with matching keys", "The Cartesian product of both tables", "Only NULL rows", "Only distinct rows"], 1,
      "A CROSS JOIN returns every combination of rows from both tables (Cartesian product). If table A has 3 rows and B has 4, result has 12 rows."),

    Q('2', 'SQL', 'Queries',
      "What does `GROUP BY department` do?",
      ["Sorts rows by department", "Filters departments", "Groups rows sharing the same department value for aggregation", "Joins tables on department"], 2,
      "GROUP BY groups rows with the same department value so aggregate functions (SUM, COUNT, AVG) can be applied per group."),

    # ─── GENERAL ASSIGNMENT 3: Data Structures (module_id='3', 10 questions) ────
    Q('3', 'Data Structures', 'Arrays',
      "What is the time complexity of accessing an element in an array by index?",
      ["O(n)", "O(log n)", "O(1)", "O(n²)"], 2,
      "Array access by index is O(1) — constant time — because arrays store elements in contiguous memory."),

    Q('3', 'Data Structures', 'Stacks',
      "A stack follows which principle?",
      ["FIFO", "LIFO", "FILO (same as FIFO)", "Random access"], 1,
      "Stack is Last In, First Out (LIFO). The last element pushed is the first one popped."),

    Q('3', 'Data Structures', 'Queues',
      "A queue follows which principle?",
      ["LIFO", "FIFO", "Random access", "Sorted order"], 1,
      "Queue is First In, First Out (FIFO). Elements are dequeued in the order they were enqueued."),

    Q('3', 'Data Structures', 'Linked Lists',
      "What is the main advantage of a linked list over an array?",
      ["Faster random access", "O(1) insertion/deletion at head", "Less memory usage", "Better cache performance"], 1,
      "Linked lists allow O(1) insertion and deletion at the head because you just update pointers, without shifting elements."),

    Q('3', 'Data Structures', 'Trees',
      "In a binary search tree (BST), where are smaller values stored relative to a node?",
      ["To the right", "To the left", "Above the node", "Below the node"], 1,
      "In a BST, values smaller than the node go in the left subtree; larger values go in the right subtree."),

    Q('3', 'Data Structures', 'Trees',
      "What is the time complexity of searching in a balanced BST?",
      ["O(n)", "O(1)", "O(log n)", "O(n log n)"], 2,
      "A balanced BST halves the search space at each step, giving O(log n) search time."),

    Q('3', 'Data Structures', 'Hash Tables',
      "What is a hash collision?",
      ["When a hash function returns a negative value", "When two different keys hash to the same index", "When the hash table is full", "When a key is deleted"], 1,
      "A collision occurs when two different keys produce the same hash index. Resolved via chaining or open addressing."),

    Q('3', 'Data Structures', 'Graphs',
      "BFS (Breadth-First Search) uses which data structure?",
      ["Stack", "Priority Queue", "Queue", "Array"], 2,
      "BFS explores nodes level by level using a Queue (FIFO) to track which nodes to visit next."),

    Q('3', 'Data Structures', 'Graphs',
      "DFS (Depth-First Search) can be implemented using:",
      ["Queue", "Stack or recursion", "Hash table", "Heap"], 1,
      "DFS uses a Stack (or the call stack via recursion) to go deep before backtracking."),

    Q('3', 'Data Structures', 'Sorting',
      "What is the average time complexity of QuickSort?",
      ["O(n)", "O(n²)", "O(n log n)", "O(log n)"], 2,
      "QuickSort averages O(n log n). Its worst case is O(n²) when the pivot is always the smallest or largest element."),

    # ─── GENERAL ASSIGNMENT 4: Aptitude (module_id='4', 10 questions) ───────────
    Q('4', 'Aptitude', 'Number Series',
      "What is the next number in the series: 2, 6, 12, 20, 30, ?",
      ["40", "42", "44", "36"], 1,
      "Differences: 4, 6, 8, 10, 12. Next term = 30 + 12 = 42."),

    Q('4', 'Aptitude', 'Percentages',
      "If a shirt costs Rs 500 and is sold at 20% discount, what is the selling price?",
      ["Rs 400", "Rs 450", "Rs 480", "Rs 420"], 0,
      "Discount = 20% of 500 = 100. Selling price = 500 - 100 = Rs 400."),

    Q('4', 'Aptitude', 'Ratios',
      "Ratio of 15 to 25 in simplest form is:",
      ["3:4", "3:5", "5:3", "1:2"], 1,
      "GCD of 15 and 25 is 5. 15/5 = 3, 25/5 = 5. Ratio = 3:5."),

    Q('4', 'Aptitude', 'Time & Work',
      "A can do work in 10 days, B in 20 days. Together they finish in how many days?",
      ["6.67 days", "15 days", "30 days", "5 days"], 0,
      "A's rate = 1/10, B's rate = 1/20. Combined = 1/10 + 1/20 = 3/20. Days = 20/3 ≈ 6.67 days."),

    Q('4', 'Aptitude', 'Speed & Distance',
      "A train travels 300 km in 5 hours. What is its speed?",
      ["50 km/h", "60 km/h", "55 km/h", "65 km/h"], 1,
      "Speed = Distance / Time = 300 / 5 = 60 km/h."),

    Q('4', 'Aptitude', 'Profit & Loss',
      "If cost price is Rs 200 and selling price is Rs 250, what is the profit percentage?",
      ["20%", "25%", "50%", "10%"], 1,
      "Profit = 250 - 200 = 50. Profit% = (50/200) × 100 = 25%."),

    Q('4', 'Aptitude', 'Ages',
      "Ravi is twice as old as Sita. In 10 years, Ravi will be 1.5 times Sita's age. What is Ravi's current age?",
      ["20 years", "30 years", "40 years", "25 years"], 0,
      "Let Sita = x, Ravi = 2x. In 10 years: 2x+10 = 1.5(x+10) → 2x+10 = 1.5x+15 → x=10. Ravi = 20 years."),

    Q('4', 'Aptitude', 'Logical Reasoning',
      "All roses are flowers. Some flowers fade quickly. Therefore:",
      ["All roses fade quickly", "Some roses may fade quickly", "No roses fade quickly", "Roses never fade"], 1,
      "Since only 'some flowers' fade, and roses are a subset of flowers, we can only conclude some roses may fade. Not a certainty."),

    Q('4', 'Aptitude', 'Probability',
      "What is the probability of getting a head when flipping a fair coin?",
      ["1/4", "1/3", "1/2", "2/3"], 2,
      "A fair coin has 2 equally likely outcomes (H, T). P(Head) = 1/2."),

    Q('4', 'Aptitude', 'Permutations',
      "In how many ways can 3 books be arranged on a shelf?",
      ["3", "6", "9", "12"], 1,
      "Number of arrangements = 3! = 3 × 2 × 1 = 6."),

    # ─── GENERAL ASSIGNMENT 5: JavaScript (module_id='5', 10 questions) ─────────
    Q('5', 'JavaScript', 'Basics',
      "Which keyword declares a block-scoped variable in JavaScript?",
      ["var", "let", "define", "set"], 1,
      "`let` declares a block-scoped variable. `var` is function-scoped (older approach)."),

    Q('5', 'JavaScript', 'Basics',
      "What does `typeof null` return?",
      ["'null'", "'undefined'", "'object'", "'boolean'"], 2,
      "This is a well-known JavaScript quirk. `typeof null` returns `'object'` (a historical bug in the language)."),

    Q('5', 'JavaScript', 'Functions',
      "What is an arrow function?",
      ["A function with a loop", "A concise function syntax using =>", "A recursive function", "A function that returns arrays"], 1,
      "Arrow functions use the `=>` syntax: `const add = (a, b) => a + b`. They also do not have their own `this`."),

    Q('5', 'JavaScript', 'DOM',
      "Which method selects an element by its ID?",
      ["document.querySelector('.id')", "document.getElement('id')", "document.getElementById('id')", "document.select('#id')"], 2,
      "`document.getElementById('id')` returns the element with the matching id attribute."),

    Q('5', 'JavaScript', 'Async',
      "What does `async/await` simplify?",
      ["Synchronous loops", "Working with Promises", "DOM manipulation", "Array methods"], 1,
      "`async/await` provides syntactic sugar over Promises, making asynchronous code look and behave more like synchronous code."),

    Q('5', 'JavaScript', 'Arrays',
      "Which array method creates a new array with transformed elements?",
      ["filter()", "reduce()", "forEach()", "map()"], 3,
      "`map()` returns a new array with each element transformed by the callback function."),

    Q('5', 'JavaScript', 'Basics',
      "What is the result of `'5' + 3` in JavaScript?",
      ["8", "'53'", "Error", "15"], 1,
      "JavaScript uses type coercion. `+` with a string converts the number to a string, resulting in concatenation: `'53'`."),

    Q('5', 'JavaScript', 'Objects',
      "How do you access the property `name` of object `user`?",
      ["user->name", "user::name", "user.name", "user[name]"], 2,
      "Dot notation `user.name` and bracket notation `user['name']` both work. The dot notation is more common for string keys."),

    Q('5', 'JavaScript', 'Basics',
      "What is `===` in JavaScript?",
      ["Assignment operator", "Strict equality (value and type)", "Loose equality", "Not equal"], 1,
      "`===` is strict equality — checks both value and type. `5 === '5'` is false because types differ."),

    Q('5', 'JavaScript', 'Events',
      "Which method attaches an event listener to an element?",
      ["element.on('click', fn)", "element.listen('click', fn)", "element.addEventListener('click', fn)", "element.bindEvent('click', fn)"], 2,
      "`addEventListener` is the standard DOM method for attaching event handlers to elements."),
]


def seed():
    with app.app_context():
        print("Clearing existing assignment data...")
        AssignmentAttempt.query.delete()
        AssignmentQuestion.query.delete()
        db.session.commit()

        db.session.add_all(QUESTIONS)
        db.session.commit()

        total = AssignmentQuestion.query.count()
        print(f"Seeded {total} assignment questions total\n")

        # Print breakdown by module
        from sqlalchemy import func
        counts = (
            db.session.query(AssignmentQuestion.module_id, func.count(AssignmentQuestion.id))
            .group_by(AssignmentQuestion.module_id)
            .all()
        )
        for module_id, count in sorted(counts):
            print(f"  {module_id}: {count} questions")


if __name__ == '__main__':
    seed()
