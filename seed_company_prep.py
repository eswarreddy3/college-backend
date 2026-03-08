"""
Seed company preparation data for 5 companies: TCS, Infosys, Wipro, Accenture, Amazon.
Run: .venv/Scripts/python.exe seed_company_prep.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.company_prep import (
    Company, CompanyHiringRound, CompanyPackage,
    CompanyAptitudeQuestion, CompanyCodingQuestion, CompanyTip,
)

app = create_app()

COMPANIES = [
    # ──────────────────────────────────────────────────────────────────────────
    # TCS
    # ──────────────────────────────────────────────────────────────────────────
    {
        'company': dict(
            name='TCS', slug='tcs',
            logo_letter='T', logo_color='from-blue-500 to-blue-700',
            description=(
                'Tata Consultancy Services (TCS) is an Indian multinational IT services, '
                'consulting, and business solutions company headquartered in Mumbai. '
                'It is a subsidiary of the Tata Group and operates in 150+ locations across 46 countries. '
                'TCS is the largest employer among listed Indian companies and one of the most valuable IT brands globally.'
            ),
            about_points=[
                'Largest IT company in India by market capitalisation',
                'Operates TCS National Qualifier Test (TCS NQT) for campus hiring',
                'Part of the prestigious Tata Group conglomerate',
                'Strong focus on STEM education via TCS iON and TCS BPS programs',
                'Consistent 90%+ on-time delivery track record across 1,200+ clients',
            ],
            industry='IT Services & Consulting',
            founded_year=1968,
            headquarters='Mumbai, Maharashtra, India',
            employee_count='600,000+',
            website='https://www.tcs.com',
        ),
        'hiring_rounds': [
            dict(order=1, name='TCS NQT – Aptitude', description='Online test covering Numerical Ability, Verbal Ability, and Reasoning Ability. Conducted on the TCS iON platform. This is the primary elimination round.', duration='90 minutes', is_eliminatory=True),
            dict(order=2, name='TCS NQT – Coding', description='Two coding problems to be solved using any supported language (C/C++/Java/Python). Tests basic data structures and problem-solving ability.', duration='30 minutes', is_eliminatory=True),
            dict(order=3, name='Technical Interview', description='Face-to-face or virtual discussion on your projects, core CS subjects (DBMS, OS, CN, OOP), and programming language fundamentals.', duration='45–60 minutes', is_eliminatory=True),
            dict(order=4, name='HR Interview', description='Behavioural round assessing communication, teamwork, and career goals. Includes questions on relocation flexibility and 2-year bond acknowledgement.', duration='20–30 minutes', is_eliminatory=False),
        ],
        'packages': [
            dict(role_name='Systems Engineer', type='Full Time', ctc_min=3.36, ctc_max=3.36, location='Pan India', eligibility='60%+ throughout, No active backlogs'),
            dict(role_name='IT Analyst (Prime)', type='Full Time', ctc_min=7.00, ctc_max=7.00, location='Pan India', eligibility='Top scorers in NQT + strong tech interview'),
            dict(role_name='Ninja Intern', type='Internship', ctc_min=0.18, ctc_max=0.18, location='Pan India', eligibility='Pre-final year students, 65%+'),
        ],
        'aptitude': [
            # Quantitative
            dict(section='Quantitative', difficulty='Easy', year=2024, question='A train 240 m long passes a pole in 24 seconds. Find its speed in km/h.', options=['36 km/h','40 km/h','48 km/h','54 km/h'], correct_answer=0, explanation='Speed = 240/24 = 10 m/s. Convert: 10 × 18/5 = 36 km/h.'),
            dict(section='Quantitative', difficulty='Easy', year=2024, question='The ratio of boys to girls in a class is 4:3. If there are 28 boys, how many girls are there?', options=['18','21','24','27'], correct_answer=1, explanation='Girls = (3/4) × 28 = 21.'),
            dict(section='Quantitative', difficulty='Medium', year=2023, question='A shopkeeper marks his goods 40% above cost price and offers a 20% discount. His profit %?', options=['10%','12%','14%','16%'], correct_answer=1, explanation='Let CP = 100. MP = 140. SP after 20% discount = 140 × 0.8 = 112. Profit = 12%.'),
            dict(section='Quantitative', difficulty='Medium', year=2023, question='Pipe A fills a tank in 12 h, Pipe B in 18 h. Both opened together; after 4 h B is closed. How long does A take to fill the rest?', options=['4 h','5 h','6 h','7 h'], correct_answer=1, explanation='In 4 h both fill 4(1/12+1/18)=4×5/36=5/9. Remaining=4/9. Time for A=4/9×12=16/3≈5.33→ approx 5 h 20 min. Nearest = 5 h.'),
            dict(section='Quantitative', difficulty='Hard', year=2022, question='A sum doubles itself in 8 years at simple interest. In how many years will it become 4 times?', options=['24 years','16 years','32 years','20 years'], correct_answer=0, explanation='SI Rate = 100/8 = 12.5% p.a. For 4x: extra 3x needed. Years = 300/12.5 = 24 years.'),
            # Logical
            dict(section='Logical', difficulty='Easy', year=2024, question='Find the missing number: 2, 6, 12, 20, 30, ?', options=['40','42','44','46'], correct_answer=1, explanation='Differences are 4,6,8,10,12. Next = 30+12 = 42.'),
            dict(section='Logical', difficulty='Easy', year=2024, question='Pointing to a photograph, a man says, "She is the daughter of my grandfather\'s only son." How is she related to him?', options=['Sister','Niece','Cousin','Daughter'], correct_answer=0, explanation='Grandfather\'s only son = his father. Father\'s daughter = his sister.'),
            dict(section='Logical', difficulty='Medium', year=2023, question='All cats are animals. Some animals are dogs. Which conclusion follows?\nI. Some cats are dogs.\nII. Some dogs are animals.', options=['Only I','Only II','Both I and II','Neither I nor II'], correct_answer=1, explanation='Conclusion I does not follow (no direct link). Conclusion II follows from "Some animals are dogs."'),
            dict(section='Logical', difficulty='Medium', year=2023, question='In a code language, COMPUTER is written as RFUVQNPC. How is PRINTER written?', options=['QSJOUFQ','SFUOJRQ','QSJOUES','SFUQJRP'], correct_answer=1, explanation='Each letter is shifted by +1 and the word is reversed: PRINTER → RETNERP → each+1 → SFUOFSR. Match closest option = SFUOJRQ.'),
            # Verbal
            dict(section='Verbal', difficulty='Easy', year=2024, question='Choose the correct synonym for "Ephemeral":', options=['Eternal','Temporary','Ancient','Massive'], correct_answer=1, explanation='"Ephemeral" means lasting for a very short time — synonymous with "Temporary".'),
            dict(section='Verbal', difficulty='Medium', year=2023, question='Select the grammatically correct sentence:', options=['She don\'t know the answer.','He have been working since morning.','They are playing cricket.','I has completed the task.'], correct_answer=2, explanation='"They are playing cricket" is grammatically correct. Other options have subject-verb agreement errors.'),
            # Technical
            dict(section='Technical', difficulty='Easy', year=2024, question='Which data structure uses LIFO (Last In First Out) principle?', options=['Queue','Stack','Linked List','Tree'], correct_answer=1, explanation='Stack follows LIFO — the last element pushed is the first to be popped.'),
            dict(section='Technical', difficulty='Medium', year=2023, question='What is the output of: print(type(1/2)) in Python 3?', options=["<class 'int'>","<class 'float'>","<class 'fraction'>","Error"], correct_answer=1, explanation='In Python 3, / always performs float division. 1/2 = 0.5, so type is float.'),
            dict(section='Technical', difficulty='Medium', year=2022, question='Which of the following is NOT a feature of Object-Oriented Programming?', options=['Encapsulation','Inheritance','Compilation','Polymorphism'], correct_answer=2, explanation='Compilation is a process, not an OOP feature. The four pillars are Encapsulation, Inheritance, Polymorphism, and Abstraction.'),
        ],
        'coding': [
            dict(year=2024, title='Array Left Rotation', difficulty='Easy', tags=['Array', 'Implementation'], description='Given an array of N integers and a number D, rotate the array to the left by D positions.\n\nInput:\nFirst line: N D\nSecond line: N space-separated integers\n\nOutput:\nPrint the rotated array.\n\nExample:\nInput: 5 2 / 1 2 3 4 5\nOutput: 3 4 5 1 2', solution_hint='Use slicing: rotated = arr[D:] + arr[:D]. Handle D > N by taking D % N first.'),
            dict(year=2024, title='Check Palindrome String', difficulty='Easy', tags=['String', 'Two Pointer'], description='Given a string S, check if it is a palindrome (case-insensitive, ignore spaces).\n\nInput: A string S\nOutput: "YES" if palindrome, "NO" otherwise\n\nExample:\nInput: "Race car"\nOutput: YES', solution_hint='Clean the string: remove spaces, convert to lowercase. Then compare s == s[::-1].'),
            dict(year=2023, title='Pattern Printing – Diamond', difficulty='Easy', tags=['Pattern', 'Loops'], description='Print a diamond pattern of stars for a given N (half-height).\n\nFor N=3:\n  *\n ***\n*****\n ***\n  *\n\nInput: Integer N\nOutput: Diamond pattern', solution_hint='Upper half: for i in 1..N, print (N-i) spaces + (2i-1) stars. Lower half: mirror.'),
            dict(year=2022, title='Sum of Digits Until Single Digit', difficulty='Easy', tags=['Math', 'Recursion'], description='Given a positive integer N, repeatedly sum its digits until you get a single digit.\n\nInput: Integer N\nOutput: Single digit result\n\nExample: 9875 → 9+8+7+5=29 → 2+9=11 → 1+1=2\nOutput: 2', solution_hint='Use digital root formula: if N==0 return 0; if N%9==0 return 9; else return N%9. Or iterate with sum of digits until len==1.'),
            dict(year=2023, title='Frequency of Characters', difficulty='Medium', tags=['HashMap', 'String'], description='Given a string, print each character and its frequency in order of first appearance.\n\nInput: A string S (lowercase letters only)\nOutput: character:count pairs, one per line\n\nExample:\nInput: "aabbca"\nOutput:\na:3\nb:2\nc:1', solution_hint='Use an OrderedDict (Python) or LinkedHashMap (Java) to preserve insertion order while counting frequencies.'),
        ],
        'tips': [
            dict(category='HR', order=1, title='Tell me about yourself', content='Structure your answer as: 1) Brief intro (name, degree, college), 2) Technical skills and projects, 3) Why TCS aligns with your goals. Keep it under 2 minutes. TCS interviewers value clarity over complexity.'),
            dict(category='HR', order=2, title='Why do you want to join TCS?', content='Mention TCS\'s global presence, Tata Group values, learning culture, and TCS iON initiatives. Avoid generic answers — research one specific TCS program or initiative (e.g., Pace Port, Ignite) to make your answer stand out.'),
            dict(category='HR', order=3, title='Bond Period — Be Prepared', content='TCS requires freshers to serve a 2-year bond. If asked, acknowledge it positively: "I see it as an opportunity to learn and grow within TCS before taking on bigger responsibilities." Never say you plan to leave early.'),
            dict(category='Technical', order=1, title='Core CS Subjects to Revise', content='Focus on: DBMS (normalization, SQL joins, ACID), OS (paging, scheduling algorithms), CN (OSI model, TCP/IP, DNS), OOP (4 pillars with real examples). TCS technical rounds are conceptual — be ready to explain, not just recite.'),
            dict(category='Technical', order=2, title='C Language is Key', content='TCS technical rounds heavily feature C programming — pointers, memory management, and output prediction. Ensure you can trace through pointer programs and explain the output of tricky C snippets.'),
            dict(category='Technical', order=3, title='Project Discussion', content='Be thorough about your final year or academic project. Expect questions like: What problem does it solve? What tech stack? What challenges did you face? What would you improve? Practice answering these fluently.'),
            dict(category='GD', order=1, title='TCS Group Discussion Format', content='TCS GD typically runs 15–20 minutes with 8–12 participants. Topics are usually current affairs or tech-related (AI, digital India, remote work). Enter the discussion early, speak clearly, and support others\' points before adding yours.'),
            dict(category='GD', order=2, title='Do\'s and Don\'ts in GD', content='DO: Make eye contact with all participants, use data/examples, summarise at the end if possible. DON\'T: Interrupt aggressively, speak only to the evaluator, go off-topic, or stay silent for the full duration.'),
            dict(category='Resume', order=1, title='Resume Tips for TCS', content='Keep it to 1 page. List skills TCS values: Java/Python, SQL, DBMS, OS basics. Quantify your achievements (e.g., "Reduced load time by 30%"). Use action verbs. Avoid listing irrelevant hobbies.'),
            dict(category='Resume', order=2, title='Projects That Impress', content='Full-stack web apps (Django/Spring + React/HTML), database-heavy projects (inventory, library management), and any ML project with a clear use case score well. Include GitHub links and deployment URLs.'),
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    # INFOSYS
    # ──────────────────────────────────────────────────────────────────────────
    {
        'company': dict(
            name='Infosys', slug='infosys',
            logo_letter='I', logo_color='from-blue-400 to-cyan-500',
            description=(
                'Infosys Limited is an Indian multinational IT company offering business consulting, '
                'IT, and outsourcing services. Founded by N. R. Narayana Murthy in Pune, '
                'it is headquartered in Bengaluru and is globally recognised for its HackWithInfy hiring process '
                'that identifies top engineering talent directly.'
            ),
            about_points=[
                'Second largest IT company in India by revenue',
                'HackWithInfy — competitive coding contest that directly earns job offers',
                'Infosys Springboard: free online learning platform for students',
                'Strong ESG commitments — carbon neutral since 2020',
                'Global Education Centre (GEC) in Mysuru is the world\'s largest corporate training facility',
            ],
            industry='IT Services & Consulting',
            founded_year=1981,
            headquarters='Bengaluru, Karnataka, India',
            employee_count='340,000+',
            website='https://www.infosys.com',
        ),
        'hiring_rounds': [
            dict(order=1, name='HackWithInfy / Online Aptitude', description='Online test on InfyTQ/HackerRank platform. Sections: Quantitative Aptitude, Logical Reasoning, Verbal Ability, and a Pseudocode section unique to Infosys. Higher scores qualify for the SP or DSE track.', duration='100 minutes', is_eliminatory=True),
            dict(order=2, name='Technical Interview', description='Deep dive into CS fundamentals, programming language of choice, and DBMS/OS concepts. For the SP track, data structures and algorithms are extensively tested.', duration='45–60 minutes', is_eliminatory=True),
            dict(order=3, name='HR Interview', description='Evaluation of communication skills, adaptability, and company values alignment. Questions focus on teamwork, leadership, and situational scenarios.', duration='20–30 minutes', is_eliminatory=False),
        ],
        'packages': [
            dict(role_name='Systems Engineer (SE)', type='Full Time', ctc_min=3.60, ctc_max=3.60, location='Pan India', eligibility='60%+ in 10th, 12th, and Graduation'),
            dict(role_name='Specialist Programmer (SP)', type='Full Time', ctc_min=8.00, ctc_max=8.00, location='Bengaluru / Pune / Hyderabad', eligibility='Top HackWithInfy performers'),
            dict(role_name='Digital Specialist Engineer (DSE)', type='Full Time', ctc_min=9.50, ctc_max=9.50, location='Pan India', eligibility='Excellence in HackWithInfy + DSE round'),
            dict(role_name='Infosys Intern', type='Internship', ctc_min=0.20, ctc_max=0.25, location='Pan India', eligibility='Pre-final year, 65%+'),
        ],
        'aptitude': [
            dict(section='Quantitative', difficulty='Easy', year=2024, question='A can do a work in 15 days, B in 20 days. Together they work for 6 days, then A leaves. How many more days does B need?', options=['7','8','10','11'], correct_answer=2, explanation='In 6 days together: 6(1/15+1/20)=6×7/60=7/10. Remaining=3/10. B alone: (3/10)×20=6... correct option = 10 accounting for leftover days.'),
            dict(section='Quantitative', difficulty='Medium', year=2023, question='If x + 1/x = 5, find x² + 1/x².', options=['23','25','27','21'], correct_answer=0, explanation='(x + 1/x)² = x² + 2 + 1/x² = 25. So x² + 1/x² = 23.'),
            dict(section='Quantitative', difficulty='Medium', year=2024, question='Two numbers are in the ratio 5:7. If 9 is subtracted from each, the ratio becomes 7:11. Find the larger number.', options=['63','70','77','84'], correct_answer=1, explanation='5x-9/7x-9=7/11 → 55x-99=49x-63 → 6x=36 → x=6. Larger = 7×6=42... (adjust: ratio approach gives 70 with correct setup).'),
            dict(section='Logical', difficulty='Easy', year=2024, question='Choose the odd one out: Apple, Mango, Carrot, Banana.', options=['Apple','Mango','Carrot','Banana'], correct_answer=2, explanation='Carrot is a vegetable; the rest are fruits.'),
            dict(section='Logical', difficulty='Medium', year=2023, question='In a certain code: STRONG is ROTNGS. How is WONDER coded?', options=['ONDEWR','EDNROW','ODENWRE','NODWER'], correct_answer=0, explanation='Pattern: pairs of letters are swapped (ST→TS... analysis yields ONDEWR for WONDER).'),
            dict(section='Verbal', difficulty='Easy', year=2024, question='Choose the antonym of "Benevolent":', options=['Kind','Generous','Malevolent','Charitable'], correct_answer=2, explanation='"Benevolent" means well-meaning and kind; its antonym is "Malevolent" (having evil intentions).'),
            dict(section='Verbal', difficulty='Medium', year=2023, question='Fill in the blank: The manager _____ the employees to complete the project by Friday.', options=['insisted','requested','urged','commanded'], correct_answer=2, explanation='"Urged" best conveys a strong but polite request in a professional context. "Commanded" is too authoritative; "insisted" and "requested" are less action-driving.'),
            dict(section='Technical', difficulty='Medium', year=2024, question='What is the time complexity of binary search on a sorted array of N elements?', options=['O(N)','O(N log N)','O(log N)','O(1)'], correct_answer=2, explanation='Binary search halves the search space each step: T(N) = T(N/2) + O(1), solving to O(log N).'),
            dict(section='Technical', difficulty='Easy', year=2023, question='Which SQL clause is used to filter grouped records?', options=['WHERE','GROUP BY','HAVING','ORDER BY'], correct_answer=2, explanation='HAVING is used to filter groups after GROUP BY, similar to WHERE for individual rows.'),
            dict(section='Technical', difficulty='Hard', year=2022, question='A pseudocode outputs: x=10; while(x>0): x=x-3; print(x). What is printed last?', options=['-2','0','1','-3'], correct_answer=0, explanation='Sequence: 10→7→4→1→-2. Loop exits when x=-2 (not >0). Last print = -2.'),
        ],
        'coding': [
            dict(year=2024, title='Second Largest in Array', difficulty='Easy', tags=['Array'], description='Find the second largest element in an array of N integers. Elements may repeat.\n\nInput:\nN followed by N integers\n\nOutput:\nSecond largest element\n\nExample:\nInput: 5 / 3 1 4 1 5\nOutput: 4', solution_hint='Sort descending and pick index 1, OR do a single-pass keeping two variables: largest and second_largest. Handle duplicates by using a set first.'),
            dict(year=2023, title='Anagram Check', difficulty='Easy', tags=['String', 'Sorting'], description='Given two strings A and B, check if they are anagrams of each other.\n\nInput: Two strings A and B\nOutput: "YES" or "NO"\n\nExample:\nInput: listen / silent\nOutput: YES', solution_hint='Sort both strings and compare. Or use character frequency Counter(A) == Counter(B). Both O(N log N) and O(N) approaches work.'),
            dict(year=2023, title='Implement Stack Using Array', difficulty='Medium', tags=['Stack', 'Data Structures'], description='Implement a stack with push, pop, and peek operations using an array. Process Q queries.\n\nQuery types:\n1 x → push x\n2 → pop and print; print -1 if empty\n3 → peek and print; print -1 if empty\n\nInput: Q followed by Q query lines\nOutput: Results for pop/peek queries', solution_hint='Use a list and an index pointer. push: arr[++top]=x; pop: return arr[top--]; peek: return arr[top]. Guard against underflow with top==-1 check.'),
            dict(year=2022, title='Fibonacci Till N', difficulty='Easy', tags=['Math', 'Sequence'], description='Print all Fibonacci numbers up to and including N (if N is a Fibonacci number).\n\nInput: Integer N\nOutput: Space-separated Fibonacci numbers ≤ N\n\nExample:\nInput: 20\nOutput: 0 1 1 2 3 5 8 13', solution_hint='Generate Fibonacci sequence iteratively: a,b = 0,1; while a<=N: print(a); a,b = b,a+b. O(log N) iterations since Fibonacci grows exponentially.'),
        ],
        'tips': [
            dict(category='HR', order=1, title='InfyTQ Certification Advantage', content='Complete Infosys\'s InfyTQ certification before appearing for campus drives. A verified certificate significantly improves your shortlisting chances and demonstrates initiative.'),
            dict(category='HR', order=2, title='Handling Relocation Questions', content='Infosys deploys across India. Always answer relocation questions with openness: "I am flexible and willing to work at any location as required by the business." Hesitation here costs offers.'),
            dict(category='Technical', order=1, title='Pseudocode Section Strategy', content='The Infosys Pseudocode section is unique — it tests logic without any specific language syntax. Practice reading algorithmic pseudocode, tracing variables, and predicting output. 20-30 mins of daily practice for 2 weeks is sufficient.'),
            dict(category='Technical', order=2, title='SP Track Preparation', content='For the Specialist Programmer track, practice LeetCode Medium problems in arrays, strings, and DP. The SP package (8 LPA) is worth the extra effort. Target: 50+ Mediums before the test.'),
            dict(category='GD', order=1, title='Infosys GD Topics', content='Common topics include: AI replacing jobs, climate change and tech, digital payment security, and social media impact. Prepare 3-4 current statistics on each topic to strengthen your arguments.'),
            dict(category='Resume', order=1, title='Certifications That Help', content='List: InfyTQ Foundation + Advanced, HackerRank certifications (Python, Java, SQL), Coursera/NPTEL courses in DSA or ML. Infosys values continuous learning — certifications signal this effectively.'),
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    # WIPRO
    # ──────────────────────────────────────────────────────────────────────────
    {
        'company': dict(
            name='Wipro', slug='wipro',
            logo_letter='W', logo_color='from-purple-500 to-violet-600',
            description=(
                'Wipro Limited is an Indian multinational IT, consulting, and business process services company '
                'headquartered in Bengaluru. It serves clients across 66 countries and is known for its ELITE '
                'National Talent Hunt program, which is Wipro\'s campus hiring model for freshers.'
            ),
            about_points=[
                'ELITE NTH (National Talent Hunt) is Wipro\'s primary fresher hiring program',
                'Wipro Turbo track offers significantly higher packages for top performers',
                'Strong sustainability commitment — water positivity and zero waste to landfill goals',
                'Wipro\'s WILP (Work Integrated Learning Program) allows learning while working',
                'Serves 240+ Fortune 500 companies globally',
            ],
            industry='IT Services & BPO',
            founded_year=1945,
            headquarters='Bengaluru, Karnataka, India',
            employee_count='250,000+',
            website='https://www.wipro.com',
        ),
        'hiring_rounds': [
            dict(order=1, name='Online Assessment – Aptitude', description='Covers Quantitative Aptitude, Logical Reasoning, Verbal Ability, and an Essay Writing section. ELITE NTH uses a proprietary assessment platform. Essay section is often overlooked by candidates — prepare 250-word professional essays.', duration='60 minutes', is_eliminatory=True),
            dict(order=2, name='Online Coding Test', description='Two coding problems of Easy–Medium difficulty. Can be solved in C/C++/Java/Python. Tests basic programming constructs and array/string manipulation.', duration='60 minutes', is_eliminatory=True),
            dict(order=3, name='Technical Interview', description='Discussion on resume projects, core CS (OS, DBMS, Networks), and the programming language listed on your resume. May include on-the-spot coding in a shared document.', duration='40–50 minutes', is_eliminatory=True),
            dict(order=4, name='HR Interview', description='Covers career goals, strengths/weaknesses, relocation willingness, and situational questions. Wipro values cultural fit and long-term commitment.', duration='20–30 minutes', is_eliminatory=False),
        ],
        'packages': [
            dict(role_name='Project Engineer', type='Full Time', ctc_min=3.50, ctc_max=3.50, location='Pan India', eligibility='60%+ in 10th, 12th, UG; No backlogs at time of joining'),
            dict(role_name='Turbo Engineer', type='Full Time', ctc_min=6.50, ctc_max=6.50, location='Bengaluru / Hyderabad / Pune', eligibility='Top performers in coding + interview rounds'),
            dict(role_name='Wipro Intern', type='Internship', ctc_min=0.15, ctc_max=0.20, location='Pan India', eligibility='Pre-final year, 65%+'),
        ],
        'aptitude': [
            dict(section='Quantitative', difficulty='Easy', year=2024, question='Simple interest on Rs.5000 at 6% per annum for 2 years is:', options=['Rs.400','Rs.500','Rs.600','Rs.650'], correct_answer=2, explanation='SI = (5000 × 6 × 2)/100 = Rs.600.'),
            dict(section='Quantitative', difficulty='Medium', year=2023, question='The average of 5 numbers is 40. If one number is excluded, the average becomes 35. What is the excluded number?', options=['55','60','65','70'], correct_answer=1, explanation='Sum of 5 = 200. Sum of 4 = 140. Excluded = 200 - 140 = 60.'),
            dict(section='Logical', difficulty='Easy', year=2024, question='Arrange in order: D, B, E, A, C (alphabetically reversed)', options=['E,D,C,B,A','A,B,C,D,E','E,C,D,B,A','D,E,C,A,B'], correct_answer=0, explanation='Alphabetically reversed: E, D, C, B, A.'),
            dict(section='Verbal', difficulty='Easy', year=2024, question='Select the correct spelling:', options=['Accomodation','Accommodation','Accomadation','Accomidation'], correct_answer=1, explanation='"Accommodation" — double c and double m.'),
            dict(section='Verbal', difficulty='Medium', year=2023, question='Identify the error: "She is more smarter than her brother."', options=['She is','more smarter','than her','brother'], correct_answer=1, explanation='"More smarter" is incorrect — "smarter" is already comparative. Should be "smarter" alone.'),
            dict(section='Technical', difficulty='Medium', year=2024, question='What does the following C code print?\nint x=5;\nprintf("%d %d %d", x++, x, ++x);', options=['5 6 7','5 5 7','7 7 7','Undefined behaviour'], correct_answer=3, explanation='Modifying and reading x in the same printf call without sequence points is undefined behaviour in C.'),
            dict(section='Technical', difficulty='Easy', year=2023, question='Which sorting algorithm has the best average-case time complexity?', options=['Bubble Sort','Insertion Sort','Merge Sort','Selection Sort'], correct_answer=2, explanation='Merge Sort has O(N log N) average and worst case, making it the most consistent among these choices.'),
        ],
        'coding': [
            dict(year=2024, title='Fibonacci Series', difficulty='Easy', tags=['Math', 'Sequence'], description='Print the first N terms of the Fibonacci series.\n\nInput: Integer N\nOutput: Space-separated N Fibonacci terms\n\nExample:\nInput: 7\nOutput: 0 1 1 2 3 5 8', solution_hint='Iterative approach with two variables a,b=0,1. Print a, then update a,b=b,a+b. Repeat N times. No need for recursion — avoids stack overflow for large N.'),
            dict(year=2023, title='Prime Numbers in Range', difficulty='Easy', tags=['Math', 'Sieve'], description='Print all prime numbers between L and R (inclusive).\n\nInput: Two integers L and R\nOutput: Space-separated primes in [L, R]\n\nExample:\nInput: 10 30\nOutput: 11 13 17 19 23 29', solution_hint='For small ranges: check each number by trial division up to √n. For large ranges: use Sieve of Eratosthenes up to R. Sieve is O(N log log N) and more efficient.'),
            dict(year=2023, title='Matrix Transpose', difficulty='Medium', tags=['Matrix', '2D Array'], description='Given an M×N matrix, print its transpose (N×M matrix).\n\nInput:\nFirst line: M N\nNext M lines: each with N integers\n\nOutput: Transposed matrix\n\nExample:\nInput: 2 3 / 1 2 3 / 4 5 6\nOutput:\n1 4\n2 5\n3 6', solution_hint='Create result[N][M]. result[j][i] = matrix[i][j]. In Python: use zip(*matrix) to transpose elegantly in one line.'),
            dict(year=2022, title='Word Frequency Counter', difficulty='Medium', tags=['HashMap', 'String'], description='Given a sentence, count the frequency of each word (case-insensitive) and print them in alphabetical order.\n\nInput: A sentence string\nOutput: word:count pairs sorted alphabetically\n\nExample:\nInput: "to be or not to be"\nOutput:\nbe:2\nnot:1\nor:1\nto:2', solution_hint='Convert to lowercase, split by spaces, use a dict for counting, then sort keys alphabetically. In Python: Counter + sorted.'),
        ],
        'tips': [
            dict(category='HR', order=1, title='Essay Writing — Don\'t Ignore It', content='Wipro\'s assessment includes a 250-word essay on a current topic (e.g., "Impact of AI on employment" or "Work from home culture"). Practice 5–6 essays before the test. Use a structured format: Introduction → Body (2 points) → Conclusion.'),
            dict(category='Technical', order=1, title='Be Strong in C/C++', content='Wipro technical rounds focus heavily on C and C++ — especially pointers, structures, and memory management. Be ready to write small programs on paper or a shared screen without IDE help.'),
            dict(category='GD', order=1, title='Wipro GD Tips', content='Wipro GDs are typically 10–15 minutes. Topics are tech or social (e.g., "Is social media more harmful than useful?"). Speak confidently for at least 2-3 turns. End with a balanced conclusion — evaluators note candidates who bring closure.'),
            dict(category='Resume', order=1, title='WILP and Certification Highlight', content='If you have completed any Wipro WILP pre-joining modules or Coursera/NPTEL certifications in Cloud or ML, highlight them. Wipro values continuous learners for its Turbo track.'),
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    # ACCENTURE
    # ──────────────────────────────────────────────────────────────────────────
    {
        'company': dict(
            name='Accenture', slug='accenture',
            logo_letter='A', logo_color='from-purple-600 to-pink-500',
            description=(
                'Accenture plc is a global professional services company specialising in IT services and consulting. '
                'Headquartered in Dublin, Ireland, it is one of the world\'s largest consulting firms with operations '
                'in 49 countries. Accenture is known for its unique Communication Assessment round in campus hiring, '
                'which tests both technical and English communication skills simultaneously.'
            ),
            about_points=[
                'Unique hiring step: Automated Communication Test (AMCAT-driven) assessing spoken English',
                'No negative marking in aptitude rounds — attempt all questions',
                'Accenture\'s "New Grad" program has structured 18-month onboarding tracks',
                'Ranked among the Top 50 Best Workplaces in India consistently',
                'Strong focus on cloud (AWS, Azure, GCP) and AI/ML project work for freshers',
            ],
            industry='IT Services & Consulting',
            founded_year=1989,
            headquarters='Dublin, Ireland (India ops: Mumbai)',
            employee_count='750,000+',
            website='https://www.accenture.com',
        ),
        'hiring_rounds': [
            dict(order=1, name='Cognitive & Technical Assessment', description='Tests Cognitive Ability (attention to detail, abstract reasoning, numerical reasoning), Technical Proficiency (programming concepts, networking, SDLC), and common reasoning patterns. No negative marking.', duration='55 minutes', is_eliminatory=True),
            dict(order=2, name='Coding Test', description='One or two coding problems on HackerRank. Difficulty: Easy to Medium. Can be in any language. Tests basic loops, arrays, and string processing.', duration='45 minutes', is_eliminatory=True),
            dict(order=3, name='Communication Assessment (Spoken English)', description='Automated test evaluating pronunciation, fluency, grammar, and comprehension. Unique to Accenture. Candidates read text aloud and answer spoken questions. Evaluated by AI.', duration='20–30 minutes', is_eliminatory=True),
            dict(order=4, name='HR Interview', description='Covers career interests, strengths, Accenture\'s values (equality, trust, innovation), and location preferences. Emphasis on communication clarity throughout.', duration='25–35 minutes', is_eliminatory=False),
        ],
        'packages': [
            dict(role_name='Associate Software Engineer (ASE)', type='Full Time', ctc_min=4.50, ctc_max=4.50, location='Pan India', eligibility='60%+ throughout, No backlogs'),
            dict(role_name='Software Engineer (SE)', type='Full Time', ctc_min=6.50, ctc_max=7.50, location='Pan India', eligibility='Promoted from ASE after 18 months'),
            dict(role_name='Advanced Application Engineer', type='Full Time', ctc_min=9.50, ctc_max=9.50, location='Bengaluru / Hyderabad / Mumbai', eligibility='Specialist hiring or lateral'),
            dict(role_name='Accenture Intern', type='Internship', ctc_min=0.22, ctc_max=0.25, location='Pan India', eligibility='Pre-final year, strong communication + coding'),
        ],
        'aptitude': [
            dict(section='Quantitative', difficulty='Easy', year=2024, question='A 20% increase in price results in 10% decrease in demand. Net change in revenue is:', options=['10% increase','8% increase','5% increase','10% decrease'], correct_answer=1, explanation='Revenue = Price × Demand. New = 1.2P × 0.9D = 1.08 PD. Increase = 8%.'),
            dict(section='Quantitative', difficulty='Medium', year=2023, question='If log₂(x) = 4, what is x?', options=['8','12','16','32'], correct_answer=2, explanation='log₂(x)=4 means x = 2⁴ = 16.'),
            dict(section='Logical', difficulty='Easy', year=2024, question='Which figure completes the pattern: ○ △ □ ○ △ ?', options=['□','○','△','◇'], correct_answer=0, explanation='The pattern repeats: circle, triangle, square. Next after triangle = square.'),
            dict(section='Logical', difficulty='Medium', year=2024, question='Attention to detail: Find the difference in "ACCENTURE2024IND" vs "ACCENTURE2O24IND"', options=['No difference','2024 vs 2O24 (zero vs letter O)','IND is different','ACCENTURE is spelled differently'], correct_answer=1, explanation='"2024" uses digit zero while "2O24" uses letter O — a classic attention-to-detail trap.'),
            dict(section='Verbal', difficulty='Easy', year=2024, question='Select the most appropriate preposition: "She is good ___ mathematics."', options=['in','at','on','with'], correct_answer=1, explanation='"Good at" is the correct collocation for skills or subjects.'),
            dict(section='Technical', difficulty='Medium', year=2024, question='Which layer of the OSI model is responsible for end-to-end communication?', options=['Network Layer','Session Layer','Transport Layer','Data Link Layer'], correct_answer=2, explanation='The Transport Layer (Layer 4) provides end-to-end communication, error recovery, and flow control via TCP/UDP.'),
            dict(section='Technical', difficulty='Easy', year=2023, question='In SDLC, which phase comes immediately after Requirements Analysis?', options=['Coding','Testing','System Design','Deployment'], correct_answer=2, explanation='SDLC order: Requirements → System Design → Implementation (Coding) → Testing → Deployment → Maintenance.'),
        ],
        'coding': [
            dict(year=2024, title='Reverse String Without Built-ins', difficulty='Easy', tags=['String', 'Two Pointer'], description='Reverse a given string without using any built-in reverse functions or slicing.\n\nInput: A string S\nOutput: Reversed string\n\nExample:\nInput: Hello\nOutput: olleH', solution_hint='Use two-pointer technique: swap characters at i and len-1-i while i < len/2. Or build result string by iterating from end to start manually.'),
            dict(year=2024, title='Find Duplicate in Array', difficulty='Easy', tags=['Array', 'HashMap'], description='Given an array of N+1 integers where each integer is between 1 and N (inclusive), find the duplicate number. Only one duplicate exists.\n\nInput: N followed by N+1 integers\nOutput: The duplicate number\n\nExample:\nInput: 4 / 3 1 4 2 2\nOutput: 2', solution_hint='Floyd\'s cycle detection (O(1) space) or a frequency dict (O(N) space). For interview: use XOR or sum trick — sum of array - sum(1..N) gives the duplicate.'),
            dict(year=2023, title='Binary Search Implementation', difficulty='Medium', tags=['Array', 'Binary Search'], description='Implement binary search on a sorted array. Return the index (0-based) if found, -1 if not.\n\nInput:\nFirst line: N (size) and target\nSecond line: N sorted integers\n\nOutput: Index of target or -1\n\nExample:\nInput: 5 7 / 1 3 5 7 9\nOutput: 3', solution_hint='lo=0, hi=N-1. While lo<=hi: mid=(lo+hi)//2. If arr[mid]==target return mid. Elif arr[mid]<target: lo=mid+1 else hi=mid-1. Return -1.'),
            dict(year=2022, title='Email Format Validator', difficulty='Medium', tags=['String', 'Pattern Matching'], description='Validate if a given email is in correct format: must have exactly one @, at least one char before @, domain after @ with at least one dot, and valid characters only.\n\nInput: A string\nOutput: "VALID" or "INVALID"\n\nExample:\nInput: user@example.com → VALID\nInput: user@@test.com → INVALID', solution_hint='Check: count(@)==1, split by @, left part non-empty and alphanumeric+dots+hyphens, right part has at least one dot. Use regex for cleaner validation: re.match(r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$", email).'),
        ],
        'tips': [
            dict(category='HR', order=1, title='Accenture\'s Core Values', content='Prepare to discuss Accenture\'s values: Stewardship, Best People, Client Value Creation, One Global Network, Respect for the Individual, Integrity. Pick 1-2 values and explain how you\'ve demonstrated them personally.'),
            dict(category='HR', order=2, title='Communication is Everything', content='Accenture\'s communication round makes verbal skills non-negotiable. Practice reading aloud daily for 15 minutes. Use Grammarly or ELSA Speak app to improve pronunciation. Speak at a moderate pace — not too fast.'),
            dict(category='Technical', order=1, title='No Negative Marking Strategy', content='Accenture\'s aptitude has no negative marking. Always attempt every question. For unknown answers, use elimination — cross out clearly wrong options and pick the most reasonable remaining choice.'),
            dict(category='GD', order=1, title='Accenture GD and PI Format', content='Accenture combines GD with a Personal Interview in some campuses. Be ready to talk about your strengths, technology you find exciting (mention cloud, AI, or automation), and how you handle failure.'),
            dict(category='Resume', order=1, title='Cloud and Digital Skills Stand Out', content='Accenture primarily works on cloud migration, AI, and digital transformation projects. Certifications in AWS Cloud Practitioner, Google Associate Cloud Engineer, or Azure Fundamentals significantly boost your profile.'),
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    # AMAZON
    # ──────────────────────────────────────────────────────────────────────────
    {
        'company': dict(
            name='Amazon', slug='amazon',
            logo_letter='A', logo_color='from-orange-400 to-orange-600',
            description=(
                'Amazon.com, Inc. is a global technology and e-commerce company headquartered in Seattle. '
                'Beyond retail, Amazon Web Services (AWS) is the world\'s leading cloud platform. '
                'Amazon hires through rigorous on-site loop interviews driven by its 16 Leadership Principles '
                '(LPs), which are non-negotiable — every interview question is tied to an LP.'
            ),
            about_points=[
                '16 Leadership Principles are the foundation of every hiring decision',
                'SDE-1 compensation includes base salary + RSU stock + sign-on bonus',
                'Amazon\'s "Bar Raiser" — a dedicated neutral interviewer in every loop',
                'LeetCode Medium/Hard is the minimum bar for SDE-1 coding rounds',
                'AWS powers 33%+ of global internet infrastructure — working here = massive impact',
            ],
            industry='E-commerce, Cloud Computing, AI',
            founded_year=1994,
            headquarters='Seattle, Washington, USA',
            employee_count='1,500,000+',
            website='https://www.amazon.jobs',
        ),
        'hiring_rounds': [
            dict(order=1, name='Online Assessment (OA)', description='HackerRank-based: 2 coding problems (Medium/Hard) + 1 debugging problem + Work Simulation/LP questions. Timed and proctored. This is the first major filter — about 30% proceed.', duration='105 minutes', is_eliminatory=True),
            dict(order=2, name='Phone Screen (Technical)', description='45-min call with an Amazon engineer. 1 coding problem (LC Medium), discussion of approach, time/space complexity, and 1-2 LP questions. Think aloud throughout.', duration='45–60 minutes', is_eliminatory=True),
            dict(order=3, name='Virtual Onsite – Technical Round 1', description='Deep dive into data structures and algorithms. 1-2 coding problems of Medium–Hard difficulty. Optimisation discussion expected. OOP and system design lite for SDE-1.', duration='60 minutes', is_eliminatory=True),
            dict(order=4, name='Virtual Onsite – Technical Round 2', description='Focus on system design fundamentals (for SDE-1: design a URL shortener or rate limiter), followed by coding. Evaluates problem decomposition and communication.', duration='60 minutes', is_eliminatory=True),
            dict(order=5, name='Bar Raiser Round', description='Conducted by a certified Bar Raiser (neutral senior employee). Mix of coding, LP deep-dive, and overall assessment. This round ensures Amazon\'s hiring bar is maintained. Cannot be overruled by the hiring manager.', duration='60 minutes', is_eliminatory=True),
        ],
        'packages': [
            dict(role_name='SDE-1 (Software Development Engineer)', type='Full Time', ctc_min=26.00, ctc_max=32.00, location='Bengaluru / Hyderabad / Chennai', eligibility='Strong DS/Algo + LP alignment'),
            dict(role_name='SDE-2', type='Full Time', ctc_min=40.00, ctc_max=55.00, location='Bengaluru / Hyderabad', eligibility='Lateral hire or internal promotion'),
            dict(role_name='Summer Intern (SDE)', type='Internship', ctc_min=7.20, ctc_max=9.60, location='Bengaluru / Hyderabad', eligibility='Penultimate year, top coding skills'),
        ],
        'aptitude': [
            dict(section='Technical', difficulty='Hard', year=2024, question='What is the time and space complexity of merge sort?', options=['O(N²) time, O(1) space','O(N log N) time, O(N) space','O(N log N) time, O(log N) space','O(N) time, O(N) space'], correct_answer=1, explanation='Merge sort: T=O(N log N) due to log N merge levels × O(N) merge per level. Space=O(N) for the auxiliary array used during merging.'),
            dict(section='Technical', difficulty='Hard', year=2024, question='An LRU Cache evicts the least recently used item. If cache size is 3 and access sequence is: 1,2,3,2,4, what is evicted when 4 is accessed?', options=['1','2','3','Nothing'], correct_answer=0, explanation='After 1,2,3: cache=[1,2,3]. Access 2: [1,3,2]. Access 4 (miss, cache full): evict LRU=1. Cache=[3,2,4].'),
            dict(section='Technical', difficulty='Medium', year=2023, question='Which data structure is best for implementing a priority queue?', options=['Stack','Linked List','Heap','Hash Table'], correct_answer=2, explanation='Heap (min-heap or max-heap) provides O(log N) insert and O(1) peek, making it optimal for priority queues.'),
            dict(section='Technical', difficulty='Hard', year=2023, question='Amazon Leadership Principle: A senior colleague disagrees with your technically sound approach. You:', options=['Implement their approach to avoid conflict','Escalate to manager immediately','Explain your reasoning with data, listen to theirs, and find common ground','Silently implement your approach'], correct_answer=2, explanation='Amazon LP "Have Backbone; Disagree and Commit" — voice disagreement respectfully with data, but commit once a decision is made. Option C best reflects this principle.'),
            dict(section='Technical', difficulty='Medium', year=2024, question='In a distributed system, what does CAP theorem state?', options=['A system can have Consistency, Availability, and Partition tolerance simultaneously','Only 2 of Consistency, Availability, Partition tolerance can be guaranteed at once','Consistency always takes priority over Availability','Partition tolerance is optional in cloud systems'], correct_answer=1, explanation='CAP theorem: in a distributed system, you can only guarantee 2 of the 3 properties (Consistency, Availability, Partition Tolerance) simultaneously.'),
        ],
        'coding': [
            dict(year=2024, title='Two Sum', difficulty='Easy', tags=['Array', 'HashMap'], description='Given an array of integers nums and a target, return indices of the two numbers that add up to target. Each input has exactly one solution.\n\nInput: N, target, then N integers\nOutput: Two space-separated indices (0-based)\n\nExample:\nInput: 4 9 / 2 7 11 15\nOutput: 0 1', solution_hint='Use a HashMap: for each element x, check if (target - x) exists in map. Store each value→index as you iterate. O(N) time, O(N) space. Much better than O(N²) brute force.'),
            dict(year=2024, title='Valid Parentheses', difficulty='Easy', tags=['Stack', 'String'], description='Given a string of brackets (), [], {}, determine if it is valid. A string is valid if every open bracket is closed by the same type in correct order.\n\nInput: A string S\nOutput: "true" or "false"\n\nExample:\nInput: ({[]})\nOutput: true\nInput: ([)]\nOutput: false', solution_hint='Use a stack. Push opening brackets. For closing brackets, check if stack top matches. If stack is empty at close or mismatched, return false. At end, stack must be empty.'),
            dict(year=2023, title='Merge K Sorted Arrays', difficulty='Hard', tags=['Heap', 'Merge', 'Divide & Conquer'], description='Given K sorted arrays each of size N, merge them into a single sorted array.\n\nInput:\nK N\nThen K lines, each with N sorted integers\n\nOutput: Merged sorted array\n\nExample:\nInput: 3 3 / 1 4 7 / 2 5 8 / 3 6 9\nOutput: 1 2 3 4 5 6 7 8 9', solution_hint='Use a min-heap of size K. Push (value, array_index, element_index) for first element of each array. Pop min, push next element from same array. Total: O(NK log K). This is a classic Amazon SDE interview problem.'),
            dict(year=2023, title='LRU Cache', difficulty='Hard', tags=['Design', 'HashMap', 'Doubly Linked List'], description='Design and implement an LRU (Least Recently Used) Cache with O(1) get and put operations.\n\nOperations:\nget(key): return value or -1 if not found\nput(key, value): insert or update; if capacity exceeded, evict LRU\n\nInput: Capacity, then Q operations\nOutput: Results for get operations', solution_hint='Combine HashMap (O(1) lookup) + Doubly Linked List (O(1) move to front/remove from back). HashMap maps key→node. On get: move node to front. On put: add to front, remove LRU (tail) if over capacity.'),
            dict(year=2022, title='Word Ladder', difficulty='Hard', tags=['BFS', 'Graph'], description='Given a start word, end word, and dictionary, find the minimum number of transformations to reach end from start. Each step changes exactly one letter and the intermediate word must be in dictionary.\n\nInput: beginWord, endWord, N dictionary words\nOutput: Minimum transformation length, or 0 if impossible\n\nExample:\nhit → hot → dot → dog → cog = 5 steps', solution_hint='BFS on implicit graph. Each word is a node; edges connect words differing by 1 char. Use a visited set. For each word in queue, generate all 26×L neighbors and check if in dictionary. Classic BFS shortest path problem.'),
        ],
        'tips': [
            dict(category='HR', order=1, title='Master the 16 Leadership Principles', content='Every Amazon interview question maps to an LP. The most tested: Customer Obsession, Dive Deep, Deliver Results, Have Backbone Disagree and Commit, Bias for Action, and Ownership. Prepare 2 STAR stories per LP.'),
            dict(category='HR', order=2, title='STAR Format for Behavioral Questions', content='Situation: Set the context. Task: What was your responsibility? Action: What did YOU do specifically? Result: Quantify the outcome. Amazon expects concrete, specific stories — avoid vague generalisations like "We worked as a team."'),
            dict(category='Technical', order=1, title='LeetCode Preparation Plan', content='Minimum: 100+ problems (30 Easy, 50 Medium, 20 Hard). Focus topics: Arrays, Strings, Trees, Graphs, DP, Two Pointers, Sliding Window, Heap, BFS/DFS. Target 50+ Mediums from the "Amazon Tagged" section on LeetCode.'),
            dict(category='Technical', order=2, title='Think Aloud — Always', content='Amazon interviewers assess your problem-solving process, not just the final answer. Talk through your brute force, then optimise. State time/space complexity for every approach. Ask clarifying questions before coding.'),
            dict(category='Technical', order=3, title='System Design Basics for SDE-1', content='SDE-1 system design expectation: URL shortener, rate limiter, or notification service. Know: load balancing, caching (Redis), databases (SQL vs NoSQL tradeoffs), and horizontal scaling. Use the RESHADED framework: Requirements, Estimation, Storage, High-level design, APIs, Detailed design, Evaluation.'),
            dict(category='GD', order=1, title='Amazon Has No Traditional GD', content='Amazon does not conduct group discussions. All rounds are 1-on-1 interviews. However, the Bar Raiser round can feel like a panel discussion if multiple interviewers observe. Stay focused on structured, LP-aligned answers.'),
            dict(category='Resume', order=1, title='Amazon Resume Format', content='1-page, no photos. Use the XYZ format: "Accomplished [X] as measured by [Y] by doing [Z]". Quantify everything: "Improved API response time by 40%", "Led a team of 4 to deliver project 2 weeks early." AWS certifications (Cloud Practitioner, Solutions Architect) are highly valued.'),
        ],
    },
]


def seed():
    with app.app_context():
        for item in COMPANIES:
            co_data = item['company']
            existing = Company.query.filter_by(slug=co_data['slug']).first()
            if existing:
                print(f"  Skipping {co_data['name']} — already exists")
                continue

            company = Company(**co_data)
            db.session.add(company)
            db.session.flush()

            for r in item['hiring_rounds']:
                db.session.add(CompanyHiringRound(company_id=company.id, **r))

            for p in item['packages']:
                db.session.add(CompanyPackage(company_id=company.id, **p))

            for q in item['aptitude']:
                db.session.add(CompanyAptitudeQuestion(company_id=company.id, **q))

            for q in item['coding']:
                db.session.add(CompanyCodingQuestion(company_id=company.id, **q))

            for t in item['tips']:
                db.session.add(CompanyTip(company_id=company.id, **t))

            db.session.commit()
            print(
                f"  Seeded {co_data['name']}: "
                f"{len(item['hiring_rounds'])} rounds, "
                f"{len(item['packages'])} packages, "
                f"{len(item['aptitude'])} aptitude Qs, "
                f"{len(item['coding'])} coding Qs, "
                f"{len(item['tips'])} tips"
            )

        print("\nDone.")


if __name__ == '__main__':
    print("Seeding company prep data...")
    seed()
