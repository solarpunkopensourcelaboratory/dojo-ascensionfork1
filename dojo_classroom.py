#!/usr/bin/env python3
"""
DOJO ASCENSION v4.0 — The Outlier Qualification Classroom
A terminal RPG that teaches Python, Git, and JSON for SolarPunk contributor qualification.
Each "quest" is a VSCode-aligned tutorial lesson with a real coding challenge.
"""

import sys
import time
import os
import json
import platform
import shutil
import subprocess
import re
from pathlib import Path
from datetime import datetime

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class _Dummy:
        def __getattr__(self, name): return ""
    Fore = Style = Back = _Dummy()

# ─────────────────────────────────────────────
#  SAVE / LOAD SYSTEM (JSON — teaches JSON!)
# ─────────────────────────────────────────────
SAVE_FILE = Path.home() / ".dojo_save.json"

def save_progress(player):
    data = {
        "name": player.name,
        "level": player.level,
        "honor": player.honor,
        "completed": list(player.completed),
        "last_save": datetime.now().isoformat()
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"{Fore.GREEN}✓ Progress saved to {SAVE_FILE}{Style.RESET_ALL}")

def load_progress():
    if SAVE_FILE.exists():
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        print(f"{Fore.CYAN}✓ Save found! Welcome back, {data['name']}.{Style.RESET_ALL}")
        return data
    return None

# ─────────────────────────────────────────────
#  PLAYER CLASS
# ─────────────────────────────────────────────
class Player:
    def __init__(self, name, level=1, honor=0, completed=None):
        self.name = name
        self.level = level
        self.honor = honor
        self.completed = set(completed or [])

    def award_honor(self, points, reason=""):
        self.honor += points
        print(f"\n{Fore.YELLOW}⚡ +{points} HONOR{' — ' + reason if reason else ''}{Style.RESET_ALL}")

    @property
    def rank(self):
        ranks = [
            (0, "Initiate"), (50, "Apprentice"), (150, "Practitioner"),
            (300, "Adept"), (600, "Expert"), (1000, "Dojo Candidate")
        ]
        current = "Initiate"
        for threshold, title in ranks:
            if self.honor >= threshold:
                current = title
        return current

# ─────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, speed=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def divider(char="─", width=60, color=Fore.CYAN):
    print(f"{color}{char * width}{Style.RESET_ALL}")

def header(title, color=Fore.CYAN):
    divider("═", 60, color)
    print(f"{color}{Style.BRIGHT}  {title}{Style.RESET_ALL}")
    divider("═", 60, color)

def lesson_box(text):
    """Print a styled lesson/theory box."""
    lines = text.strip().split("\n")
    print(f"\n{Back.BLUE}{Fore.WHITE}{'  LESSON  ':^60}{Style.RESET_ALL}")
    for line in lines:
        print(f"  {Fore.CYAN}{line}{Style.RESET_ALL}")
    print()

def challenge_box(text):
    """Print a styled challenge/task box."""
    lines = text.strip().split("\n")
    print(f"\n{Back.GREEN}{Fore.BLACK}{'  CHALLENGE  ':^60}{Style.RESET_ALL}")
    for line in lines:
        print(f"  {Fore.GREEN}{line}{Style.RESET_ALL}")
    print()

def hint_box(text):
    print(f"\n  {Fore.YELLOW}💡 HINT: {text}{Style.RESET_ALL}\n")

def wait():
    input(f"\n{Fore.WHITE}[ Press ENTER to continue... ]{Style.RESET_ALL}")

# ─────────────────────────────────────────────
#  CURRICULUM MAP
# ─────────────────────────────────────────────
CURRICULUM = {
    1: {"title": "System Grounding",         "skill": "Python: Environment & Tools",   "outlier_tag": "Tools"},
    2: {"title": "Variables & Data Types",    "skill": "Python: Core Data Types",       "outlier_tag": "Python"},
    3: {"title": "JSON — The Data Language",  "skill": "JSON: Read, Write, Parse",      "outlier_tag": "JSON"},
    4: {"title": "Functions & Logic",         "skill": "Python: Functions & Control",   "outlier_tag": "Python"},
    5: {"title": "Git — Version Control",     "skill": "Git: Init, Add, Commit",        "outlier_tag": "Git"},
    6: {"title": "Git — Branching & Merge",   "skill": "Git: Branch, Merge, Rebase",    "outlier_tag": "Git"},
    7: {"title": "APIs & HTTP",               "skill": "Python: requests + JSON APIs",  "outlier_tag": "Python+JSON"},
    8: {"title": "File I/O & JSON Files",     "skill": "Python: File Handling + JSON",  "outlier_tag": "Python+JSON"},
    9: {"title": "OOP — Classes",             "skill": "Python: OOP & Classes",         "outlier_tag": "Python"},
   10: {"title": "Code Review Mastery",       "skill": "ModernTech: Review & Feedback",    "outlier_tag": "ModernTech"},
}

# ─────────────────────────────────────────────
#  MISSION IMPLEMENTATIONS
# ─────────────────────────────────────────────

def run_code_challenge(prompt, starter_code, validator_fn, hint=""):
    """Generic interactive code challenge runner with VSCode integration tip."""
    challenge_box(prompt)
    if hint:
        hint_box(hint)
    print(f"  {Fore.WHITE}TIP: You can also try this in VSCode — create a .py file and run it there!{Style.RESET_ALL}")
    print(f"\n  {Fore.YELLOW}→ Write your answer below, or type 'hint' for help, 'skip' to skip:{Style.RESET_ALL}\n")

    attempts = 0
    while True:
        try:
            user_input = input(f"  {Fore.GREEN}>>> {Style.RESET_ALL}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to menu...")
            return False

        if user_input.lower() == 'skip':
            print(f"  {Fore.YELLOW}Skipped. You can revisit this challenge later.{Style.RESET_ALL}")
            return False
        if user_input.lower() == 'hint':
            hint_box(hint or "Think about what the challenge is asking step by step.")
            continue

        result = validator_fn(user_input)
        attempts += 1

        if result is True:
            print(f"\n  {Fore.GREEN}{Style.BRIGHT}✓ CORRECT!{Style.RESET_ALL}")
            if attempts == 1:
                print(f"  {Fore.YELLOW}Bonus: First-try answer! +5 honor{Style.RESET_ALL}")
            return True
        else:
            print(f"\n  {Fore.RED}✗ Not quite. {result if isinstance(result, str) else 'Try again.'}{Style.RESET_ALL}")
            if attempts >= 3:
                print(f"  {Fore.YELLOW}Hint unlocked after 3 tries: {hint}{Style.RESET_ALL}")


def mission_1_system_grounding(player):
    header("MISSION 1: SYSTEM GROUNDING", Fore.YELLOW)
    lesson_box("""
What is Python?
Python is the #1 language for AI training work.
It reads almost like English and can do almost anything.

VSCode Quick Start:
1. Install VSCode: https://code.visualstudio.com
2. Install the Python extension (search 'Python' in Extensions)
3. Open a folder, create a .py file, and press F5 to run it

The Python REPL:
>>> print("Hello, World!")
Hello, World!

'print()' sends text to your screen. It's your most basic tool.
    """)

    print(f"\n  {Fore.CYAN}Running system diagnostic...{Style.RESET_ALL}\n")
    time.sleep(1)

    checks = []
    py_ver = platform.python_version()
    checks.append(("Python Version", py_ver, float(py_ver[:3]) >= 3.8))

    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    checks.append(("Free Disk Space", f"{free_gb}GB", free_gb >= 2))

    git_ok = subprocess.run(["git", "--version"], capture_output=True).returncode == 0
    checks.append(("Git Installation", "Installed" if git_ok else "NOT FOUND", git_ok))

    for name, val, ok in checks:
        color = Fore.GREEN if ok else Fore.RED
        symbol = "✓" if ok else "✗"
        print(f"  {color}{symbol} {name}: {val}{Style.RESET_ALL}")

    if not git_ok:
        print(f"\n  {Fore.YELLOW}⚠ Git not found! Install from: https://git-scm.com{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Git is required for Outlier's Git skill assessment!{Style.RESET_ALL}")

    wait()

    def validate_print(code):
        if 'print(' in code and ('"' in code or "'" in code):
            return True
        return "Use print() with a string inside quotes. Example: print('hello')"

    won = run_code_challenge(
        "Write a print() statement that outputs your name or any message.",
        "print('...')",
        validate_print,
        hint="print() takes a string (text in quotes) as its argument."
    )
    return 20 if won else 5


def mission_2_variables(player):
    header("MISSION 2: VARIABLES & DATA TYPES", Fore.BLUE)
    lesson_box("""
Variables store data. Python has 4 core types:

  name = "David"        # str  — text in quotes
  age  = 25             # int  — whole numbers
  gpa  = 3.8            # float — decimal numbers
  active = True         # bool — True or False

Python is DYNAMICALLY TYPED — you don't declare the type.
The type() function reveals what type a variable is:
  >>> type(name)
  <class 'str'>

For JSON work (critical for Outlier!):
  Python str  → JSON string   "value"
  Python int  → JSON number   42
  Python dict → JSON object   {}
  Python list → JSON array    []
  Python bool → JSON boolean  true/false
    """)

    def validate_vars(code):
        has_str = re.search(r'\w+\s*=\s*["\']', code)
        has_int = re.search(r'\w+\s*=\s*\d+', code)
        if has_str and has_int:
            return True
        return "Create at least one string variable AND one integer variable."

    won1 = run_code_challenge(
        "Create 3 variables: a name (string), an age (integer), and a score (float).\nType all 3 assignment statements.",
        "name = ...\nage = ...\nscore = ...",
        validate_vars,
        hint="String: name = 'Alice'  |  Integer: age = 30  |  Float: score = 9.5"
    )

    print(f"\n{Fore.CYAN}  BONUS — f-strings (used everywhere in Python):{Style.RESET_ALL}")
    print("""
  name = "David"
  level = 5
  print(f"Player {name} is at level {level}")
  → Player David is at level 5
    """)

    def validate_fstring(code):
        if 'f"' in code or "f'" in code:
            if '{' in code and '}' in code:
                return True
        return "Use an f-string: f'Hello {name}' where name is a variable."

    won2 = run_code_challenge(
        "Write an f-string that combines two variables in a sentence.",
        "print(f'...')",
        validate_fstring,
        hint="Example: city = 'SLC'  →  print(f'I live in {city}')"
    )

    return (25 if won1 else 5) + (15 if won2 else 0)


def mission_3_json(player):
    header("MISSION 3: JSON — THE DATA LANGUAGE", Fore.MAGENTA)
    lesson_box("""
JSON (JavaScript Object Notation) is the universal data format.
Outlier uses JSON everywhere: task payloads, responses, configs.

Python's json module:

  import json

  # Python dict → JSON string (serializing)
  data = {"name": "David", "level": 5, "skills": ["Python", "Git"]}
  text = json.dumps(data, indent=2)
  print(text)

  # JSON string → Python dict (parsing)
  loaded = json.loads(text)
  print(loaded["name"])  # David

  # Write to file
  with open("data.json", "w") as f:
      json.dump(data, f, indent=2)

  # Read from file
  with open("data.json", "r") as f:
      loaded = json.load(f)

Key rules:
  • JSON keys MUST be strings (double quotes)
  • Use None in Python (json converts to null automatically)
  • indent=2 makes output human-readable
    """)

    demo_path = Path.home() / "dojo_demo.json"
    demo_data = {
        "player": player.name,
        "level": player.level,
        "honor": player.honor,
        "skills": ["Python", "JSON", "Git"],
        "active": True
    }
    with open(demo_path, "w") as f:
        json.dump(demo_data, f, indent=2)

    print(f"  {Fore.GREEN}✓ Created demo JSON file at: {demo_path}{Style.RESET_ALL}")
    print(f"\n  {Fore.CYAN}Contents:{Style.RESET_ALL}")
    print(json.dumps(demo_data, indent=2))
    print(f"\n  {Fore.WHITE}Open this file in VSCode to see JSON syntax highlighting!{Style.RESET_ALL}")
    wait()

    def validate_json_keys(code):
        if '[' in code and ('"' in code or "'" in code):
            return True
        if '.get(' in code:
            return True
        return "Access a JSON/dict value using bracket notation: data['key']"

    won = run_code_challenge(
        'Given this dict:\n  data = {"name": "David", "score": 100}\nHow do you access the "name" value?',
        "data[...]",
        validate_json_keys,
        hint="Dictionary access: data['name']  — the key goes inside brackets with quotes."
    )

    print(f"\n{Fore.CYAN}  OUTLIER SKILL: Identifying valid vs invalid JSON{Style.RESET_ALL}")
    invalid_jsons = [
        ("{name: 'David'}", "Keys must be double-quoted strings: {\"name\": \"David\"}"),
        ('{"active": True}', "Python True/False → JSON true/false (lowercase)"),
        ('{"count": ,}', "Missing value after colon"),
    ]
    for snippet, explanation in invalid_jsons:
        print(f"\n  Is this valid JSON?  {Fore.YELLOW}{snippet}{Style.RESET_ALL}")
        input("  (Press enter to reveal answer): ")
        print(f"  {Fore.RED}INVALID — {explanation}{Style.RESET_ALL}")

    return (30 if won else 10) + 10


def mission_4_functions(player):
    header("MISSION 4: FUNCTIONS & LOGIC", Fore.GREEN)
    lesson_box("""
Functions are reusable code blocks. Outlier tasks often ask you
to write or evaluate functions — this is core Python.

  def greet(name):
      return f"Hello, {name}!"

  result = greet("David")
  print(result)  # Hello, David!

Key concepts:
  • def keyword defines a function
  • Parameters go in parentheses
  • return sends a value back
  • Indentation (4 spaces) defines the function body

List comprehensions (very Pythonic):
  squares = [x**2 for x in range(10)]
  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

Control flow:
  if score >= 90: grade = "A"
  elif score >= 80: grade = "B"
  else: grade = "C"
    """)

    def validate_function(code):
        if 'def ' in code and 'return' in code:
            return True
        return "Write a complete function with 'def' and 'return'."

    won1 = run_code_challenge(
        "Write a function called 'double' that takes a number and returns it multiplied by 2.",
        "def double(n):\n    return ...",
        validate_function,
        hint="def double(n):  and then  return n * 2"
    )

    def validate_comprehension(code):
        if '[' in code and 'for' in code and 'in' in code:
            return True
        return "Write a list comprehension: [expression for item in iterable]"

    won2 = run_code_challenge(
        "Write a list comprehension that gives squares of 1 through 5: [1, 4, 9, 16, 25]",
        "[... for x in range(1, 6)]",
        validate_comprehension,
        hint="[x**2 for x in range(1, 6)]  — ** is the power operator"
    )

    return (25 if won1 else 5) + (25 if won2 else 5)


def mission_5_git_basics(player):
    header("MISSION 5: GIT — VERSION CONTROL", Fore.RED)
    lesson_box("""
Git is how professional developers track code changes.
ModernTech's Git skill assessment tests these exact commands.

CORE WORKFLOW:
  git init              # Start a new repo
  git status            # See what changed
  git add .             # Stage ALL changes
  git add filename.py   # Stage ONE file
  git commit -m "msg"   # Save a snapshot
  git log --oneline     # See commit history

REMOTE (GitHub):
  git clone <url>       # Download a repo
  git push origin main  # Upload your commits
  git pull              # Download latest changes

IMPORTANT for ModernTech:
  Good commit: "Add JSON parser for user profiles"
  Bad commit:  "fix stuff" or "update"
  Use present tense: "Add feature" not "Added feature"
    """)

    demo_dir = Path.home() / "dojo_git_demo"
    print(f"\n  {Fore.CYAN}Creating a live Git practice repo at ~/dojo_git_demo...{Style.RESET_ALL}")
    try:
        demo_dir.mkdir(exist_ok=True)
        subprocess.run(["git", "init"], cwd=demo_dir, capture_output=True)
        (demo_dir / "hello.py").write_text('print("Hello from Dojo!")\n')
        subprocess.run(["git", "add", "."], cwd=demo_dir, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit: add hello.py"],
            cwd=demo_dir, capture_output=True, text=True,
            env={**os.environ,
                 "GIT_AUTHOR_NAME": "Dojo Student",
                 "GIT_AUTHOR_EMAIL": "student@dojo.io",
                 "GIT_COMMITTER_NAME": "Dojo Student",
                 "GIT_COMMITTER_EMAIL": "student@dojo.io"}
        )
        print(f"  {Fore.GREEN}✓ Git repo created! Try: cd ~/dojo_git_demo && git log --oneline{Style.RESET_ALL}")
    except Exception as e:
        print(f"  {Fore.YELLOW}⚠ Git demo skipped: {e}{Style.RESET_ALL}")

    wait()

    questions = [
        ("What command stages ALL changes for commit?",
         ["git add .", "git add -a", "git add --all"],
         "It's 'git add' followed by a dot"),
        ("What command saves a staged snapshot with a message?",
         ["git commit -m", "git commit"],
         "git commit with the -m flag for message"),
        ("What command shows uncommitted changes in your working directory?",
         ["git status", "git stat"],
         "git status"),
    ]

    score = 0
    for q_text, answers, explanation in questions:
        print(f"\n  {Fore.WHITE}Q: {q_text}{Style.RESET_ALL}")
        ans = input(f"  {Fore.GREEN}→ {Style.RESET_ALL}").strip().lower()
        if any(ans in correct.lower() for correct in answers):
            print(f"  {Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
            score += 1
        else:
            print(f"  {Fore.RED}✗ Answer: {answers[0]}{Style.RESET_ALL}")
            hint_box(explanation)

    return 15 * score + 10


def mission_6_git_branching(player):
    header("MISSION 6: GIT — BRANCHING & MERGING", Fore.RED)
    lesson_box("""
Branches let you work on features without breaking main code.
This is the #1 thing ModernTech tests in Git skill assessments.

BRANCH COMMANDS:
  git branch                  # List all branches
  git branch feature-x        # Create new branch
  git checkout feature-x      # Switch to branch
  git checkout -b feature-x   # Create AND switch (shortcut)
  git switch feature-x        # Modern syntax (Git 2.23+)

MERGING:
  git checkout main           # Switch back to main
  git merge feature-x         # Merge feature into main

REBASING (ModernTech loves this question):
  git rebase main             # Reapply commits on top of main
  # Rebase = cleaner history; merge = preserves full timeline

GitFlow Naming Conventions:
  feature/add-json-parser
  fix/null-pointer-exception
  hotfix/security-patch
  release/v2.0.0
    """)

    questions = [
        ("What command creates AND switches to a new branch in one step?",
         ["git checkout -b", "git switch -c"],
         "Combines create + checkout in one command"),
        ("In GitFlow, what prefix do bug fix branches use?",
         ["fix/", "bugfix/", "hotfix/"],
         "Common: fix/ or bugfix/ for regular fixes, hotfix/ for production"),
        ("Describe the key difference between merge and rebase:",
         None,
         "Merge preserves full history; rebase creates linear history"),
    ]

    score = 0
    for q_text, answers, explanation in questions:
        print(f"\n  {Fore.WHITE}Q: {q_text}{Style.RESET_ALL}")
        ans = input(f"  {Fore.GREEN}→ {Style.RESET_ALL}").strip().lower()
        if answers is None:
            if len(ans) > 10:
                print(f"  {Fore.GREEN}✓ Good! Key point: {explanation}{Style.RESET_ALL}")
                score += 1
            else:
                print(f"  {Fore.YELLOW}Explanation: {explanation}{Style.RESET_ALL}")
        elif any(a.lower() in ans for a in answers):
            print(f"  {Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
            score += 1
        else:
            print(f"  {Fore.RED}✗ Answer: {answers[0]} — {explanation}{Style.RESET_ALL}")

    return 20 * score + 10


def mission_7_apis(player):
    header("MISSION 7: APIs & HTTP REQUESTS", Fore.BLUE)
    lesson_box("""
APIs are how programs talk to each other.
This builds directly on your existing Dojo Week 2!

  import requests

  response = requests.get("https://api.example.com/data")
  print(response.status_code)  # 200 = success
  data = response.json()        # Parse JSON response

Status codes:
  200 OK           — request succeeded
  201 Created      — resource created (POST)
  400 Bad Request  — your request has errors
  401 Unauthorized — need authentication
  404 Not Found    — resource doesn't exist
  500 Server Error — their problem

POST with JSON payload:
  payload = {"username": "david", "score": 100}
  response = requests.post(url, json=payload)

Always add error handling:
  try:
      response = requests.get(url, timeout=5)
      response.raise_for_status()
      data = response.json()
  except requests.exceptions.RequestException as e:
      print(f"Error: {e}")
    """)

    import urllib.request
    print(f"\n  {Fore.CYAN}Live API Demo — fetching Bitcoin price (your Week 2 mission!)...{Style.RESET_ALL}")
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        price = data['bitcoin']['usd']
        print(f"  {Fore.GREEN}✓ BTC Price: ${price:,}{Style.RESET_ALL}")
    except Exception as e:
        print(f"  {Fore.YELLOW}⚠ API unavailable: {e}{Style.RESET_ALL}")

    wait()

    questions = [
        ("What HTTP status code means the request succeeded?",
         ["200", "200 ok"], "200 is the universal success code"),
        ("What method parses a JSON response from the requests library?",
         ["response.json()", ".json()"], "response.json() converts JSON text to Python dict"),
        ("What parameter prevents requests.get() from hanging forever?",
         ["timeout", "timeout="], "Always set timeout=5 or similar"),
    ]

    score = 0
    for q_text, answers, explanation in questions:
        print(f"\n  {Fore.WHITE}Q: {q_text}{Style.RESET_ALL}")
        ans = input(f"  {Fore.GREEN}→ {Style.RESET_ALL}").strip().lower()
        if any(a.lower() in ans for a in answers):
            print(f"  {Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
            score += 1
        else:
            print(f"  {Fore.RED}✗ Answer: {answers[0]} — {explanation}{Style.RESET_ALL}")

    return 20 * score + 10


def mission_8_file_io(player):
    header("MISSION 8: FILE I/O & JSON FILES", Fore.MAGENTA)
    lesson_box("""
File I/O is how you persist data across program runs.
JSON is the standard format for ModernTech task data.

READING:
  with open("data.txt", "r") as f:
      content = f.read()        # All as string
      lines = f.readlines()     # List of lines

WRITING:
  with open("output.txt", "w") as f:  # "w" overwrites
      f.write("Hello!\n")
  with open("output.txt", "a") as f:  # "a" appends
      f.write("Another line\n")

JSON FILES:
  import json
  with open("config.json", "w") as f:
      json.dump({"key": "value"}, f, indent=2)
  with open("config.json", "r") as f:
      config = json.load(f)

PATHLIB (modern Python):
  from pathlib import Path
  p = Path("data") / "users.json"
  data = json.loads(p.read_text())
  p.write_text(json.dumps(data, indent=2))
    """)

    exercise_path = Path.home() / "dojo_exercise.json"
    practice_data = [
        {"id": 1, "task": "Review Python function", "quality": "good", "score": 8},
        {"id": 2, "task": "Evaluate Git commit", "quality": "needs_work", "score": 4},
        {"id": 3, "task": "Parse JSON payload", "quality": "excellent", "score": 10},
    ]
    with open(exercise_path, "w") as f:
        json.dump(practice_data, f, indent=2)
    print(f"  {Fore.GREEN}✓ Created practice file: {exercise_path}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}  Open in VSCode and filter tasks with score > 7!{Style.RESET_ALL}")
    wait()

    def validate_json_write(code):
        if 'open(' in code and ('json.dump' in code or 'write(' in code):
            return True
        if 'write_text(' in code and 'json' in code:
            return True
        return "Show how to write JSON to a file using open() + json.dump()"

    won = run_code_challenge(
        "Write the code to save {'name': 'David', 'level': 5} to 'data.json'",
        "with open('data.json', 'w') as f:\n    json.dump(..., f)",
        validate_json_write,
        hint="with open('data.json', 'w') as f:  →  json.dump({'name': 'David'}, f, indent=2)"
    )

    return 35 if won else 10


def mission_9_oop(player):
    header("MISSION 9: OOP — CLASSES & OBJECTS", Fore.CYAN)
    lesson_box("""
Object-Oriented Programming organizes code into classes.
ModernTech back-end dev assessments HEAVILY test OOP.

  class Player:
      def __init__(self, name):    # Constructor
          self.name = name         # Instance attribute
          self.level = 1

      def level_up(self):          # Method
          self.level += 1
          return f"{self.name} is now level {self.level}!"

      def __repr__(self):          # String representation
          return f"Player('{self.name}', level={self.level})"

  p = Player("David")
  print(p.level_up())  # David is now level 2!

INHERITANCE:
  class Expert(Player):
      def __init__(self, name, specialty):
          super().__init__(name)
          self.specialty = specialty

SOLID Principles (ModernTech code review favorites):
  S — Single Responsibility
  O — Open/Closed
  L — Liskov Substitution
  I — Interface Segregation
  D — Dependency Inversion
    """)

    questions = [
        ("What is the constructor method called in Python?",
         ["__init__"], "__init__ is called automatically when creating an instance"),
        ("What does 'super().__init__()' do in a child class?",
         ["calls parent", "parent constructor", "parent __init__"],
         "Calls the parent class's __init__ to set up inherited attributes"),
        ("What does 'self' refer to in a class method?",
         ["the instance", "current instance", "the object"],
         "self is the specific object instance the method is called on"),
    ]

    score = 0
    for q_text, answers, explanation in questions:
        print(f"\n  {Fore.WHITE}Q: {q_text}{Style.RESET_ALL}")
        ans = input(f"  {Fore.GREEN}→ {Style.RESET_ALL}").strip().lower()
        if any(a.lower() in ans for a in answers):
            print(f"  {Fore.GREEN}✓ Correct!{Style.RESET_ALL}")
            score += 1
        else:
            print(f"  {Fore.RED}✗ Answer: {answers[0]} — {explanation}{Style.RESET_ALL}")

    return 20 * score + 10


def mission_10_code_review(player):
    header("MISSION 10: CODE REVIEW MASTERY", Fore.YELLOW)
    lesson_box("""
This IS your job at ModernTech. You review AI-generated code
and provide structured, professional feedback.

THE OUTLIER REVIEW FRAMEWORK:
  1. Correctness  — Does it do what it should?
  2. Efficiency   — Is there a better algorithm?
  3. Readability  — Would another dev understand this?
  4. Best Practices — PEP8, SOLID, DRY, error handling?
  5. Edge Cases   — What breaks it? None, empty list, 0?

GOOD REVIEW (specific):
  "Line 12: O(n²) loop. Use a dict for O(1) lookup:
   scores = {u['id']: u['score'] for u in users}"

BAD REVIEW (vague):
  "This could be better" — too vague, not actionable
    """)

    review_cases = [
        {
            "code": """
def get_user(users, user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None""",
            "issues": [
                "O(n) linear scan — use a dict for O(1) lookup",
                "No input validation (users could be None)",
                "No type hints or docstring"
            ],
            "question": "What is the algorithmic performance concern?"
        },
        {
            "code": """
import json
def load_config():
    f = open("config.json")
    data = json.load(f)
    return data""",
            "issues": [
                "File not closed — use 'with open()' context manager",
                "No exception handling if file doesn't exist"
            ],
            "question": "What resource management bug exists here?"
        },
        {
            "code": """
def process(x):
    return x * 2 + 1""",
            "issues": [
                "No docstring describing what it does",
                "'x' is not a descriptive variable name",
                "No type hints: def process(value: int) -> int:"
            ],
            "question": "What readability improvements would you suggest?"
        },
    ]

    score = 0
    for i, case in enumerate(review_cases, 1):
        print(f"\n  {Fore.CYAN}REVIEW CASE {i}/{len(review_cases)}:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{case['code']}{Style.RESET_ALL}")
        print(f"\n  {Fore.WHITE}Q: {case['question']}{Style.RESET_ALL}")
        ans = input(f"  {Fore.GREEN}Your review: {Style.RESET_ALL}").strip()
        if len(ans) > 15:
            print(f"  {Fore.GREEN}✓ Good analysis! Expert notes:{Style.RESET_ALL}")
            score += 1
        else:
            print(f"  {Fore.YELLOW}Try to be more specific. Expert notes:{Style.RESET_ALL}")
        for issue in case["issues"]:
            print(f"    • {Fore.CYAN}{issue}{Style.RESET_ALL}")

    return 30 * score + 10


MISSIONS = {
    1: mission_1_system_grounding,
    2: mission_2_variables,
    3: mission_3_json,
    4: mission_4_functions,
    5: mission_5_git_basics,
    6: mission_6_git_branching,
    7: mission_7_apis,
    8: mission_8_file_io,
    9: mission_9_oop,
   10: mission_10_code_review,
}

# ─────────────────────────────────────────────
#  STATUS DASHBOARD
# ─────────────────────────────────────────────
def show_status(player):
    clear_screen()
    header("DOJO ASCENSION — ModernTech PREP DASHBOARD", Fore.CYAN)
    print(f"\n  {Fore.WHITE}Player : {Style.BRIGHT}{player.name}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Rank   : {Fore.YELLOW}{player.rank}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Honor  : {Fore.YELLOW}{player.honor} pts{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Level  : {player.level}/{len(CURRICULUM)}\n{Style.RESET_ALL}")
    divider()
    print(f"  {'#':<4} {'Mission':<30} {'Tag':<20} {'Status':<12}")
    divider("-", 60)
    for num, info in CURRICULUM.items():
        done = num in player.completed
        color = Fore.GREEN if done else (Fore.YELLOW if num <= player.level else Fore.RED)
        status = "✓ Done" if done else ("Available" if num <= player.level else "Locked")
        print(f"  {num:<4} {info['title']:<30} {info['outlier_tag']:<20} {color}{status}{Style.RESET_ALL}")

    skills = {CURRICULUM[n]["outlier_tag"] for n in player.completed}
    print(f"\n  {Fore.CYAN}Outlier Skills Covered: {Fore.GREEN}{', '.join(skills) or 'None yet'}{Style.RESET_ALL}")

    next_thresholds = [50, 150, 300, 600, 1000]
    for t in next_thresholds:
        if player.honor < t:
            bar = int((player.honor / t) * 30)
            print(f"\n  Next rank at {t} honor — need {t - player.honor} more")
            print(f"  [{'█' * bar}{'░' * (30 - bar)}] {player.honor}/{t}")
            break
    wait()


def show_vscode_guide():
    clear_screen()
    header("VSCODE INTEGRATION GUIDE", Fore.GREEN)
    print("""
  SETUP (one-time):
  ─────────────────
  1. Install VSCode: https://code.visualstudio.com
  2. Extensions (Ctrl+Shift+X): Install "Python" by Microsoft
  3. Install "GitLens" — Git superpowers in the editor
  4. Install "Prettier" — JSON auto-formatting
  5. Install "Python Indent" — auto-indentation

  OFFICIAL TUTORIALS (pair with Dojo missions):
  ───────────────────────────────────────────────
  Missions 1-4  → code.visualstudio.com/docs/python/python-quick-start
  Missions 5-6  → code.visualstudio.com/docs/sourcecontrol/overview
  Missions 7-8  → code.visualstudio.com/docs/python/debugging
  Missions 9-10 → code.visualstudio.com/docs/python/testing

  DAILY WORKFLOW:
  ───────────────
  1. Open your dojo-ascension folder in VSCode
  2. Open terminal (Ctrl+`) → python dojo_classroom.py
  3. Complete a mission in the terminal
  4. Open the ~/dojo_*.json files Dojo creates
  5. Experiment and modify them in VSCode

  KEY SHORTCUTS:
  ──────────────
  F5           → Run current Python file
  F9           → Toggle breakpoint (debugger)
  Ctrl+`       → Open integrated terminal
  Ctrl+Shift+P → Command palette
  Ctrl+Shift+G → Git panel (view changes, commits)
  Ctrl+Shift+X → Extensions marketplace
    """)
    wait()


# ─────────────────────────────────────────────
#  MAIN MENU & GAME LOOP
# ─────────────────────────────────────────────
def main_menu(player):
    clear_screen()
    header(f"DOJO OS v4.0 | {player.name} | {player.rank}", Fore.CYAN)
    print(f"\n  {Fore.YELLOW}⚡ Honor: {player.honor}  |  Level: {player.level}/{len(CURRICULUM)}{Style.RESET_ALL}\n")
    print(f"  {Fore.WHITE}1. Start/Continue Mission (Level {player.level}){Style.RESET_ALL}")
    print(f"  {Fore.WHITE}2. Choose a specific mission{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}3. View progress dashboard{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}4. VSCode integration guide{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}5. Save progress{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}6. Exit{Style.RESET_ALL}")
    return input(f"\n  {Fore.GREEN}root@dojo:~# {Style.RESET_ALL}").strip()


def run_mission(player, mission_num):
    if mission_num not in MISSIONS:
        print(f"{Fore.RED}Mission {mission_num} not yet available.{Style.RESET_ALL}")
        time.sleep(2)
        return
    fn = MISSIONS[mission_num]
    honor_gained = fn(player)
    player.completed.add(mission_num)
    player.award_honor(honor_gained, CURRICULUM[mission_num]["skill"])
    if mission_num >= player.level:
        player.level = mission_num + 1
        print(f"\n  {Fore.CYAN}{Style.BRIGHT}🎖 LEVEL UP! Now at Level {player.level}{Style.RESET_ALL}")
    print(f"\n  {Fore.YELLOW}Mission complete! +{honor_gained} honor{Style.RESET_ALL}")
    next_info = CURRICULUM.get(player.level, {})
    print(f"  {Fore.CYAN}Next: {next_info.get('title', 'All missions complete — ModernTech Candidate!')}{Style.RESET_ALL}")
    wait()


def game_loop():
    clear_screen()
    print_slow(f"{Fore.CYAN}{Style.BRIGHT}  DOJO ASCENSION v4.0{Style.RESET_ALL}", 0.03)
    print_slow(f"{Fore.WHITE}  ModernTech AI Qualification Training System{Style.RESET_ALL}", 0.02)
    print_slow(f"{Fore.YELLOW}  Python | Git | JSON | Code Review{Style.RESET_ALL}", 0.02)
    print()

    saved = load_progress()
    if saved:
        player = Player(saved["name"], saved["level"], saved["honor"], saved.get("completed", []))
    else:
        name = input(f"  {Fore.GREEN}Enter your name, Initiate: {Style.RESET_ALL}").strip() or "Initiate"
        player = Player(name)

    wait()

    while True:
        choice = main_menu(player)
        if choice == '1':
            lvl = player.level if player.level <= len(CURRICULUM) else len(CURRICULUM)
            run_mission(player, lvl)
        elif choice == '2':
            print(f"\n  Available missions (1-{len(CURRICULUM)}):")
            for num, info in CURRICULUM.items():
                print(f"    {num}. {info['title']}")
            try:
                num = int(input(f"\n  {Fore.GREEN}Choose: {Style.RESET_ALL}"))
                run_mission(player, num)
            except ValueError:
                pass
        elif choice == '3':
            show_status(player)
        elif choice == '4':
            show_vscode_guide()
        elif choice == '5':
            save_progress(player)
            time.sleep(1)
        elif choice == '6':
            save_progress(player)
            print_slow(f"\n  {Fore.CYAN}Disconnecting from Dojo OS... Progress saved.{Style.RESET_ALL}")
            sys.exit()


if __name__ == "__main__":
    game_loop()
