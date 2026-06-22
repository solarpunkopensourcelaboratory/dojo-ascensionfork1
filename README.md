# 🥋 DOJO ASCENSION v5.0

**A terminal-based learning system for practicing Python, Git, JSON, and code review through story-driven missions and deliberate practice.**

---

## 🎯 What Is This?

Dojo Ascension is not just a coding tutorial—it's a **learning operating system** that combines:

- **Mission-based progression** — Complete 10+ interconnected challenges
- **Competency tracking** — Master specific skills (Python, Git, JSON, Architecture, Code Review)
- **Reflection journal** — Optional Uta Hagen systems-thinking questions after each mission
- **Persistent saves** — All progress stored in human-readable JSON
- **Cross-disciplinary context** — Each mission connects code to philosophy, economics, and martial arts

### The Philosophy

Code is not syntax—it's a framework for thinking about systems. By mastering these crafts, you learn to:
- **Build resilient digital infrastructure** (Git, version control, deployment)
- **Design cooperative systems** (OOP, APIs, data interoperability)
- **Hold systems accountable** (Code review, testing, documentation)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- 2GB free disk space

### Installation

```bash
# 1. Clone this repo
git clone https://github.com/alucardzagreus-boop/dojo-ascension
cd dojo-ascension

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Dojo
python dojo_classroom.py
```

### First Time Setup

When you run the game, you'll be prompted to enter your name. The system will:
1. Check your environment (Python version, Git installation, disk space)
2. Create a save file at `~/.dojo_save.json`
3. Optionally create a journal at `~/.dojo_journal_data.json`

---

## 📖 Curriculum (10 Core Missions)

| # | Mission | Skill | Philosophy |
|---|---------|-------|------------|
| 1 | System Grounding | Git | Wu Wei: Your tools become extensions of your mind |
| 2 | Variables & Data Lineage | Python | Genealogy: Tracing lineage reveals identity |
| 3 | JSON — Data Language | JSON | Cornel West: Justice is cooperation in code |
| 4 | Functions & Jeet Kune Do | Python | Bruce Lee: Maximum efficiency with minimum effort |
| 5 | Git — Journalistic Integrity | Git | Activism: Git is an immutable ledger of truth |
| 6 | Git — Branching & Merging | Git | Wing Chun: Deflect and redirect, don't oppose |
| 7 | APIs & Digital Journalism | Architecture | Freedom of Information: Query the source directly |
| 8 | File I/O — Institutional Memory | Python | Bushido: Legacy ensures society can learn |
| 9 | OOP — Sociological Modeling | Architecture | Theatre: Roles and Actors in a cooperative |
| 10 | Code Review — Gentle Art | Review | BJJ: Testing each other's code before production |

---

## 🎮 How to Play

### Main Menu Options

1. **Start Next Mission** — Play the next incomplete mission in sequence
2. **Choose Specific Mission** — Jump to any mission you want
3. **View Progress Dashboard** — See your skill levels and rank
4. **Reflection Journal** — Review past journal entries and your practice chain
5. **VSCode Integration Guide** — Learn how to pair missions with VSCode
6. **Save Progress** — Manually save your state
7. **Exit** — Quit (progress is auto-saved)

### Mission Flow

Each mission teaches a concept through:

1. **Philosophical Anchor** — Connect code to a real-world principle
2. **Economic Parallel** — Understand the "cost" and "value" of the pattern
3. **Technical Concept** — Learn the actual code syntax
4. **Challenge** — Answer a question or write code
5. **Reflection** (optional) — Answer Uta Hagen's 9 systems-thinking questions

### Progression System

- **Honor Points** — Earned by completing missions (20-30 per mission)
- **Ranks** — Initiate → Apprentice → Practitioner → Adept → Expert → Co-Architect
- **Skills** — Track mastery: Python, Git, JSON, Architecture, Code Review (0-5 levels each)
- **Practice Chain** — Consecutive days of journaling (rewards deliberate practice, not perfection)

---

## 💾 Progress Saves

Your progress is stored in two JSON files:

### `~/.dojo_save.json` (Player State)
```json
{
  "name": "David",
  "honor": 150,
  "completed": ["git_system_grounding", "python_variables"],
  "skills": {
    "python": 2,
    "git": 3,
    "json": 1,
    "architecture": 0,
    "review": 0
  },
  "last_save": "2026-06-22T18:40:02Z"
}
```

### `~/.dojo_journal_data.json` (Reflection Entries)
```json
{
  "2026-06-22": {
    "timestamp": "2026-06-22T18:42:15Z",
    "mission_id": "python_variables",
    "mission_title": "Variables & Data Lineage",
    "player_rank": "Apprentice",
    "answers": {
      "Who am I in this circumstance?": "A programmer learning to think systematically...",
      "What do I want?": "To understand how data flows through systems..."
      ...
    }
  }
}
```

---

## 🔗 VSCode Integration

Pair each mission with VSCode for hands-on learning:

### One-Time Setup

1. Install [VSCode](https://code.visualstudio.com)
2. Install extensions:
   - **Python** (by Microsoft) — Run and debug Python code
   - **GitLens** — View Git history and blame
   - **Prettier** — Auto-format JSON
   - **Python Indent** — Smart indentation

### Workflow

```bash
# In VSCode terminal:
python dojo_classroom.py

# In another VSCode editor:
# 1. Complete a mission in the terminal
# 2. Open ~/dojo_demo.json or other files created by missions
# 3. Experiment and modify them
# 4. Run code with F5 to see results
```

### Official Tutorials to Pair With

- **Missions 1-4** → [Python Quick Start](https://code.visualstudio.com/docs/python/python-quick-start)
- **Missions 5-6** → [Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview)
- **Missions 7-8** → [Debugging](https://code.visualstudio.com/docs/python/debugging)
- **Missions 9-10** → [Testing](https://code.visualstudio.com/docs/python/testing)

---

## 📚 Architecture (v5.0)

### Data-Driven Missions

Missions are stored in `missions.json` as pure data:

```json
{
  "id": "git_system_grounding",
  "number": 1,
  "title": "System Grounding",
  "philosophy": "Like Tai Chi...",
  "economics": "Infrastructure is...",
  "tech_concept": "The terminal...",
  "challenge": "Type the command to clone a repository.",
  "answer": "git clone",
  "skill": "git",
  "honor_base": 20
}
```

This means:
- ✅ **Non-programmers can contribute missions** (educators, subject-matter experts)
- ✅ **Translators can localize content** without touching Python
- ✅ **Mission packs can be shared** and loaded dynamically
- ✅ **Save files are future-proof** (mission IDs never change)

### Engine Architecture

- `dojo_classroom.py` — Main game loop, mission loading, player management (v5.0 Dynamic Engine)
- `missions.json` — All mission data (externalized, data-driven)
- `~/.dojo_save.json` — Player progress (persistent)
- `~/.dojo_journal_data.json` — Reflection entries (persistent)

### Future Phases

- **Phase 1 (Current)** — 10 core Python/Git/JSON/CodeReview missions
- **Phase 2** — `dojo_ascension.py` — Advanced multi-week curriculum (Linux, security, quant)
- **Phase 3** — Mission packs: Journalism, Genealogy, Governance, AI Literacy
- **Phase 4** — Community: Shared mission packs, classroom dashboards, instructor tools

---

## 🤝 Contributing

### For Mission Writers

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick start:

1. Fork the repo
2. Add your mission(s) to `missions.json`
3. Test locally
4. Submit a pull request

### For Code Contributors

- Bug fixes and feature requests welcome
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup

---

## 📋 Project Status

**v5.0 (Current)**
- ✅ Dynamic mission engine (missions.json)
- ✅ Competency-based ranking
- ✅ Uta Hagen reflection journal (optional)
- ✅ Dashboard with skill specialization
- ✅ Persistent saves (JSON)
- 🔜 Mission packs (Journalism, Genealogy, Governance)
- 🔜 Classroom mode (instructor dashboard)

---

## 📖 License

[Add your license here — e.g., MIT, GPL, etc.]

## 🙏 Credits

Built by and for the SolarPunk community. Inspired by:
- **Uta Hagen's acting techniques** (systems thinking)
- **Cornel West's philosophy** (public justice)
- **Bruce Lee's martial philosophy** (efficiency)
- **Estonia's e-governance model** (resilience)
- **Brazilian Jiu-Jitsu** (collaborative learning)

---

## 🔗 Links

- [GitHub Repository](https://github.com/alucardzagreus-boop/dojo-ascension)
- [Contributing Guide](CONTRIBUTING.md)
- [Original SolarPunk Dojo Project](https://github.com/solarpunkopensourcelaboratory/dojo-ascension)

---

**Let us never stop learning from Galileo.** — SolarPunk HackNet
