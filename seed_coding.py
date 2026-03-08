"""
Update coding problems with proper stdin/stdout test cases and starter code.
Run: .venv/Scripts/python.exe seed_coding.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.coding_problem import CodingProblem

app = create_app()

PROBLEMS = [
    {
        'slug': 'two-sum',
        'title': 'Two Sum',
        'difficulty': 'Easy',
        'tags': ['Array', 'Hash Table'],
        'description': (
            'Given an array of integers and a target, return the indices of the two numbers that add up to the target.\n\n'
            'Input format:\n'
            '  Line 1: n (number of elements)\n'
            '  Line 2: n space-separated integers\n'
            '  Line 3: target integer\n\n'
            'Output: Two 0-based indices separated by a space (smaller index first).\n\n'
            'Exactly one solution exists. You may not use the same element twice.'
        ),
        'examples': [
            {'input': 'n=4, nums=[2,7,11,15], target=9', 'output': '0 1', 'explanation': 'nums[0]+nums[1]=9'},
            {'input': 'n=3, nums=[3,2,4], target=6',      'output': '1 2'},
            {'input': 'n=2, nums=[3,3], target=6',         'output': '0 1'},
        ],
        'constraints': '2 <= n <= 10^4\n-10^9 <= nums[i] <= 10^9',
        'starter_code': {
            'python': (
                'n = int(input())\n'
                'nums = list(map(int, input().split()))\n'
                'target = int(input())\n\n'
                '# Write your solution here\n'
                '# Print two indices separated by space\n'
            ),
            'javascript': (
                'const lines = require("fs").readFileSync(0, "utf8").trim().split("\\n");\n'
                'const n = parseInt(lines[0]);\n'
                'const nums = lines[1].split(" ").map(Number);\n'
                'const target = parseInt(lines[2]);\n\n'
                '// Write your solution here\n'
                '// console.log(i + " " + j);\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        int n = sc.nextInt();\n'
                '        int[] nums = new int[n];\n'
                '        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n'
                '        int target = sc.nextInt();\n'
                '        // Write your solution here\n'
                '        // System.out.println(i + " " + j);\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    int n; cin >> n;\n'
                '    vector<int> nums(n);\n'
                '    for (int i = 0; i < n; i++) cin >> nums[i];\n'
                '    int target; cin >> target;\n'
                '    // Write your solution here\n'
                '    // cout << i << " " << j << endl;\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': '4\n2 7 11 15\n9',   'expected': '0 1'},
            {'input': '3\n3 2 4\n6',       'expected': '1 2'},
            {'input': '2\n3 3\n6',         'expected': '0 1'},
            {'input': '5\n1 2 3 4 5\n9',   'expected': '3 4'},
            {'input': '4\n-1 -2 -3 -4\n-6', 'expected': '1 3'},
        ],
    },
    {
        'slug': 'valid-parentheses',
        'title': 'Valid Parentheses',
        'difficulty': 'Easy',
        'tags': ['String', 'Stack'],
        'description': (
            'Given a string containing only `(`, `)`, `{`, `}`, `[`, `]`, determine if it is valid.\n\n'
            'A string is valid if:\n'
            '- Open brackets are closed by the same type of bracket.\n'
            '- Open brackets are closed in the correct order.\n\n'
            'Input format: A single string of bracket characters.\n'
            'Output: `true` or `false`'
        ),
        'examples': [
            {'input': 's = "()"',     'output': 'true'},
            {'input': 's = "()[]{}"', 'output': 'true'},
            {'input': 's = "(]"',     'output': 'false'},
            {'input': 's = "([)]"',   'output': 'false'},
        ],
        'constraints': '1 <= s.length <= 10^4',
        'starter_code': {
            'python': (
                's = input().strip()\n\n'
                '# Write your solution here\n'
                '# Print true or false\n'
            ),
            'javascript': (
                'const s = require("fs").readFileSync(0, "utf8").trim();\n\n'
                '// Write your solution here\n'
                '// console.log("true" or "false")\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        String s = sc.nextLine().trim();\n'
                '        // Write your solution here\n'
                '        // System.out.println("true" or "false");\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    string s; cin >> s;\n'
                '    // Write your solution here\n'
                '    // cout << (valid ? "true" : "false") << endl;\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': '()',       'expected': 'true'},
            {'input': '()[]{}',   'expected': 'true'},
            {'input': '(]',       'expected': 'false'},
            {'input': '([)]',     'expected': 'false'},
            {'input': '{[]}',     'expected': 'true'},
            {'input': '',         'expected': 'true'},
            {'input': '(((',      'expected': 'false'},
        ],
    },
    {
        'slug': 'reverse-linked-list',
        'title': 'Reverse Array',
        'difficulty': 'Easy',
        'tags': ['Array'],
        'description': (
            'Given an array of integers, return the array reversed.\n\n'
            'Input format:\n'
            '  Line 1: n (number of elements)\n'
            '  Line 2: n space-separated integers\n\n'
            'Output: Space-separated integers in reversed order.'
        ),
        'examples': [
            {'input': 'n=5, nums=[1,2,3,4,5]', 'output': '5 4 3 2 1'},
            {'input': 'n=2, nums=[1,2]',        'output': '2 1'},
            {'input': 'n=1, nums=[1]',           'output': '1'},
        ],
        'constraints': '1 <= n <= 10^4',
        'starter_code': {
            'python': (
                'n = int(input())\n'
                'nums = list(map(int, input().split()))\n\n'
                '# Write your solution here\n'
                '# Print reversed array elements separated by spaces\n'
            ),
            'javascript': (
                'const lines = require("fs").readFileSync(0, "utf8").trim().split("\\n");\n'
                'const n = parseInt(lines[0]);\n'
                'const nums = lines[1].split(" ").map(Number);\n\n'
                '// Write your solution here\n'
                '// console.log(reversed.join(" "));\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        int n = sc.nextInt();\n'
                '        int[] nums = new int[n];\n'
                '        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n'
                '        // Write your solution here\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    int n; cin >> n;\n'
                '    vector<int> nums(n);\n'
                '    for (int i = 0; i < n; i++) cin >> nums[i];\n'
                '    // Write your solution here\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': '5\n1 2 3 4 5',  'expected': '5 4 3 2 1'},
            {'input': '2\n1 2',         'expected': '2 1'},
            {'input': '1\n42',          'expected': '42'},
            {'input': '4\n10 20 30 40', 'expected': '40 30 20 10'},
            {'input': '3\n-1 0 1',      'expected': '1 0 -1'},
        ],
    },
    {
        'slug': 'binary-search',
        'title': 'Binary Search',
        'difficulty': 'Easy',
        'tags': ['Array', 'Binary Search'],
        'description': (
            'Given a sorted array of distinct integers and a target, return the index of target or -1 if not found.\n\n'
            'Input format:\n'
            '  Line 1: n (number of elements)\n'
            '  Line 2: n sorted space-separated integers\n'
            '  Line 3: target integer\n\n'
            'Output: The 0-based index of target, or -1 if not found.'
        ),
        'examples': [
            {'input': 'n=6, nums=[-1,0,3,5,9,12], target=9', 'output': '4'},
            {'input': 'n=6, nums=[-1,0,3,5,9,12], target=2', 'output': '-1'},
        ],
        'constraints': '1 <= n <= 10^4\nAll values are distinct\nnums is sorted ascending',
        'starter_code': {
            'python': (
                'n = int(input())\n'
                'nums = list(map(int, input().split()))\n'
                'target = int(input())\n\n'
                '# Write your binary search here\n'
                '# Print the index, or -1 if not found\n'
            ),
            'javascript': (
                'const lines = require("fs").readFileSync(0, "utf8").trim().split("\\n");\n'
                'const n = parseInt(lines[0]);\n'
                'const nums = lines[1].split(" ").map(Number);\n'
                'const target = parseInt(lines[2]);\n\n'
                '// Write your binary search here\n'
                '// console.log(index);\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        int n = sc.nextInt();\n'
                '        int[] nums = new int[n];\n'
                '        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();\n'
                '        int target = sc.nextInt();\n'
                '        // Write your binary search here\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    int n; cin >> n;\n'
                '    vector<int> nums(n);\n'
                '    for (int i = 0; i < n; i++) cin >> nums[i];\n'
                '    int target; cin >> target;\n'
                '    // Write your binary search here\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': '6\n-1 0 3 5 9 12\n9',  'expected': '4'},
            {'input': '6\n-1 0 3 5 9 12\n2',  'expected': '-1'},
            {'input': '1\n5\n5',              'expected': '0'},
            {'input': '1\n5\n6',              'expected': '-1'},
            {'input': '5\n1 3 5 7 9\n7',      'expected': '3'},
            {'input': '5\n2 4 6 8 10\n1',     'expected': '-1'},
        ],
    },
    {
        'slug': 'longest-substring-without-repeating',
        'title': 'Longest Substring Without Repeating Characters',
        'difficulty': 'Medium',
        'tags': ['String', 'Sliding Window', 'Hash Table'],
        'description': (
            'Given a string, find the length of the longest substring without repeating characters.\n\n'
            'Input format: A single string (may contain spaces).\n'
            'Output: An integer — the length of the longest substring.'
        ),
        'examples': [
            {'input': 's = "abcabcbb"', 'output': '3', 'explanation': '"abc" has length 3'},
            {'input': 's = "bbbbb"',    'output': '1', 'explanation': '"b" has length 1'},
            {'input': 's = "pwwkew"',   'output': '3', 'explanation': '"wke" has length 3'},
        ],
        'constraints': '0 <= s.length <= 5*10^4\ns consists of printable ASCII characters',
        'starter_code': {
            'python': (
                's = input()\n\n'
                '# Write your solution here (sliding window recommended)\n'
                '# Print the length of the longest substring\n'
            ),
            'javascript': (
                'const s = require("fs").readFileSync(0, "utf8").trimEnd();\n\n'
                '// Write your solution here\n'
                '// console.log(length);\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        String s = sc.nextLine();\n'
                '        // Write your solution here\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    string s; getline(cin, s);\n'
                '    // Write your solution here\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': 'abcabcbb', 'expected': '3'},
            {'input': 'bbbbb',    'expected': '1'},
            {'input': 'pwwkew',   'expected': '3'},
            {'input': '',         'expected': '0'},
            {'input': 'abcdef',   'expected': '6'},
            {'input': 'dvdf',     'expected': '3'},
            {'input': 'aab',      'expected': '2'},
        ],
    },
    {
        'slug': 'merge-intervals',
        'title': 'Merge Intervals',
        'difficulty': 'Medium',
        'tags': ['Array', 'Sorting'],
        'description': (
            'Given a list of intervals, merge all overlapping intervals and return the resulting list.\n\n'
            'Input format:\n'
            '  Line 1: n (number of intervals)\n'
            '  Next n lines: two integers "start end" for each interval\n\n'
            'Output: Each merged interval on its own line as "start end", sorted by start.'
        ),
        'examples': [
            {'input': 'n=4, intervals=[[1,3],[2,6],[8,10],[15,18]]',
             'output': '1 6\n8 10\n15 18',
             'explanation': '[1,3] and [2,6] overlap → [1,6]'},
            {'input': 'n=2, intervals=[[1,4],[4,5]]',
             'output': '1 5'},
        ],
        'constraints': '1 <= n <= 10^4\n0 <= start <= end <= 10^4',
        'starter_code': {
            'python': (
                'n = int(input())\n'
                'intervals = []\n'
                'for _ in range(n):\n'
                '    a, b = map(int, input().split())\n'
                '    intervals.append([a, b])\n\n'
                '# Write your solution here\n'
                '# Print each merged interval as "start end"\n'
            ),
            'javascript': (
                'const lines = require("fs").readFileSync(0, "utf8").trim().split("\\n");\n'
                'const n = parseInt(lines[0]);\n'
                'const intervals = [];\n'
                'for (let i = 1; i <= n; i++) {\n'
                '    const [a, b] = lines[i].split(" ").map(Number);\n'
                '    intervals.push([a, b]);\n'
                '}\n\n'
                '// Write your solution here\n'
                '// console.log(start + " " + end) for each merged interval\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        int n = sc.nextInt();\n'
                '        int[][] intervals = new int[n][2];\n'
                '        for (int i = 0; i < n; i++) {\n'
                '            intervals[i][0] = sc.nextInt();\n'
                '            intervals[i][1] = sc.nextInt();\n'
                '        }\n'
                '        // Write your solution here\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    int n; cin >> n;\n'
                '    vector<pair<int,int>> intervals(n);\n'
                '    for (int i = 0; i < n; i++) cin >> intervals[i].first >> intervals[i].second;\n'
                '    // Write your solution here\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': '4\n1 3\n2 6\n8 10\n15 18', 'expected': '1 6\n8 10\n15 18'},
            {'input': '2\n1 4\n4 5',               'expected': '1 5'},
            {'input': '1\n1 1',                    'expected': '1 1'},
            {'input': '3\n1 2\n3 4\n5 6',          'expected': '1 2\n3 4\n5 6'},
            {'input': '3\n1 10\n2 3\n4 5',         'expected': '1 10'},
        ],
    },
    {
        'slug': 'trapping-rain-water',
        'title': 'Trapping Rain Water',
        'difficulty': 'Hard',
        'tags': ['Array', 'Two Pointers', 'Dynamic Programming'],
        'description': (
            'Given n non-negative integers representing an elevation map where the width of each bar is 1, '
            'compute how much water it can trap after raining.\n\n'
            'Input format:\n'
            '  Line 1: n (number of bars)\n'
            '  Line 2: n space-separated non-negative heights\n\n'
            'Output: Total units of water trapped.'
        ),
        'examples': [
            {'input': 'n=12, height=[0,1,0,2,1,0,1,3,2,1,2,1]',
             'output': '6'},
            {'input': 'n=6, height=[4,2,0,3,2,5]',
             'output': '9'},
        ],
        'constraints': '1 <= n <= 2*10^4\n0 <= height[i] <= 10^5',
        'starter_code': {
            'python': (
                'n = int(input())\n'
                'height = list(map(int, input().split()))\n\n'
                '# Write your solution here\n'
                '# Print total water trapped\n'
            ),
            'javascript': (
                'const lines = require("fs").readFileSync(0, "utf8").trim().split("\\n");\n'
                'const n = parseInt(lines[0]);\n'
                'const height = lines[1].split(" ").map(Number);\n\n'
                '// Write your solution here\n'
                '// console.log(water);\n'
            ),
            'java': (
                'import java.util.*;\n'
                'public class Solution {\n'
                '    public static void main(String[] args) {\n'
                '        Scanner sc = new Scanner(System.in);\n'
                '        int n = sc.nextInt();\n'
                '        int[] height = new int[n];\n'
                '        for (int i = 0; i < n; i++) height[i] = sc.nextInt();\n'
                '        // Write your solution here\n'
                '    }\n'
                '}\n'
            ),
            'cpp': (
                '#include <bits/stdc++.h>\n'
                'using namespace std;\n'
                'int main() {\n'
                '    int n; cin >> n;\n'
                '    vector<int> height(n);\n'
                '    for (int i = 0; i < n; i++) cin >> height[i];\n'
                '    // Write your solution here\n'
                '    return 0;\n'
                '}\n'
            ),
        },
        'test_cases': [
            {'input': '12\n0 1 0 2 1 0 1 3 2 1 2 1', 'expected': '6'},
            {'input': '6\n4 2 0 3 2 5',              'expected': '9'},
            {'input': '1\n5',                         'expected': '0'},
            {'input': '2\n1 2',                       'expected': '0'},
            {'input': '3\n3 0 3',                     'expected': '3'},
            {'input': '4\n1 0 1 0',                   'expected': '1'},
        ],
    },
]


def seed():
    with app.app_context():
        updated = 0
        for data in PROBLEMS:
            problem = CodingProblem.query.filter_by(slug=data['slug']).first()
            if not problem:
                problem = CodingProblem(slug=data['slug'])
                db.session.add(problem)

            problem.title = data['title']
            problem.difficulty = data['difficulty']
            problem.tags = data['tags']
            problem.description = data['description']
            problem.examples = data['examples']
            problem.constraints = data['constraints']
            problem.starter_code = data['starter_code']
            problem.test_cases = data['test_cases']
            problem.is_active = True
            updated += 1

        db.session.commit()
        print(f"Updated {updated} coding problems with test cases.")
        for p in PROBLEMS:
            print(f"  {p['slug']}: {len(p['test_cases'])} test cases")


if __name__ == '__main__':
    seed()
